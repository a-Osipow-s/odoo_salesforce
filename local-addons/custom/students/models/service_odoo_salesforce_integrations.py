import requests

class Params:

    url = ""
    payload = {}
    headers = {}

class Token(Params):

    def get_token(self):
        self.url = "https://login.salesforce.com/services/oauth2/token"
        self.payload = {
            'grant_type': 'password',
            'client_id': '3MVG9KsVczVNcM8wtV5PGf__S88tyYMX8Yc.Fy.s34SZWXAt3INm2t3uVfwuP3auRPqfl72jODw==',
            'client_secret': '2070917178455743437',
            'redirect_url': 'https://www.thirdapp.com/api/callback/',
            'username': 'toni@mail.ru',
            'password': 'Vasykrab123spAsycjVt9iBA56mXwFxRuRoD'
        }
        self.headers = {
            'cache-control': "no-cache"
        }
        dict_response = requests.request("POST", self.url, data=self.payload, headers=self.headers).json()
        return dict_response['access_token']

class Sale(Params):

    def get_order(self, token):
        self.url = "https://na85.salesforce.com/services/data/v42.0"      # add url
        self.headers = {
            'Authorization': "Bearer " + token,
            'cache-control': "no-cache"
        }
        dict_response = requests.request("GET", self.url, headers=self.headers).json()
        return dict_response['']

    def get_customer(self, token):
        self.url = "https://na85.salesforce.com/services/data/v42.0"    # add url
        self.headers = {
            'Authorization': "Bearer " + token,
            'cache-control': "no-cache"
        }
        dict_response = requests.request("GET", self.url, headers=self.headers).json()
        return dict_response['']
