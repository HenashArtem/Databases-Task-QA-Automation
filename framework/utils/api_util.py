import requests
from framework.utils.logger import Logger


class APIUtil:
    response = None

    def __init__(self, url):
        self.url = url

    def send_post_req(self, endpoint, post_data):
        Logger.info("Sending POST request")
        self.response = requests.post(f'{self.url}' + f'{endpoint}', data=post_data)
        return self.response

    def send_put_req(self, endpoint, put_data):
        Logger.info("Sending PUT request")
        self.response = requests.put(f'{self.url}' + f'{endpoint}', data=put_data)
        return self.response

    def send_get_req(self, endpoint, params=None):
        Logger.info("Sending GET request")
        self.response = requests.get(f'{self.url}' + f'{endpoint}', params=params)
        return self.response

    def send_delete_req(self, endpoint):
        Logger.info("Sending DELETE request")
        self.response = requests.delete(f'{self.url}' + f'{endpoint}')
        return self.response

    def send_get_req_by_post_num(self, num_of_post: int):
        Logger.info("Sending GET request by number of post")
        self.response = requests.get((f'{self.url}' + '/posts' + f'/{num_of_post}'))

    def get_status(self):
        Logger.info("Getting status")
        return self.response.status_code

    def response_to_json(self):
        Logger.info("Converting response to JSON")
        return self.response.json()

    def check_resp_is_json(self):
        Logger.info("Checking if the response is JSON")
        resp_content_type = self.response.headers.get('content-type')
        return "application/json" in resp_content_type

    def check_response_status(self, expected_status):
        Logger.info("Checking response status")
        status = self.get_status()
        if status == expected_status:
            Logger.info(f"Success! Received status: {status}")
            return True
        else:
            Logger.warning(f"Attention! Received status: {status}")
            return False
