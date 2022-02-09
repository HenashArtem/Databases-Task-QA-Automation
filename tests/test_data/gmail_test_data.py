from tests.test_data.creds_util import get_endpoint_for_auth_page, get_value_from_creds_json, get_redirect_uri


email = ""
password = ""
endpoint_for_auth_page = str(get_endpoint_for_auth_page())
client_id = str(get_value_from_creds_json("client_id"))
client_secret = str(get_value_from_creds_json("client_secret"))
redirect_uri = str(get_redirect_uri())
