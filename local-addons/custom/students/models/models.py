from odoo import models, fields, api
from odoo.addons.queue_job.job import job
import logging
from .books_oz import get_html, get_author_name, get_book_name, get_all_links, get_max_number_page

class Person(models.Model):
    _name = 'students.person'
    _logger = logging.getLogger('person_logger')

    name = fields.Char(string="Name", required=True)
    surname = fields.Char(string="Surname", required=True)
    age = fields.Integer(string="Age")
    book_count = fields.Integer(compute='count_of_books', string="Count of books", store=True)

    books = fields.Many2many('students.book', 'rel_book')

    @api.model
    def create(self, values):
        if values['age'] < 18:
            values['age'] = 18
        record = super(Person, self).create(values)
        return record

    @api.depends('books')
    def count_of_books(self):
        for item in self:
            name = len(self.books)
            item.book_count = name


class Book(models.Model):
    _name = "students.book"
    _logger = logging.getLogger('book_logger')

    url = "https://oz.by/books/bestsellers"

    name = fields.Char(string="Book Name", require=True)
    author = fields.Char(string="Book author")

    @api.multi
    def call_async_func(self):
        self.env['students.book'].with_delay().async_parse_bestsellers_oz()


    @api.multi
    @job
    def async_parse_bestsellers_oz(self):
        html = get_html(self.url)
        max_num_page = int(get_max_number_page(html))
        page = 1

        while page <= max_num_page:
            self.url += "?page=" + str(page)
            html = get_html(self.url)
            links = get_all_links(html)
            for link in links:
                book_name = get_book_name(link)
                book_author = get_author_name(link)
                self._logger.info(book_name + " --- " + book_author)
                self.env['students.book'].create({
                    'name': book_name,
                    'author': book_author
                })
            page += 1


    @api.multi
    def unlink(self):
        self.env['students.book'].unlink()

        # @job
        # def create_record(self, values):
        #     record = self.env['students.book'].create(values)
        #     return record