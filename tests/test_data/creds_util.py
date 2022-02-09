import json
from tests.config.urls import Urls


def get_creds_json():
    with open("../tests/test_data/client_secret.json", "r") as json_file:
        data = json.load(json_file)
        json_file.close()
        return data


def get_value_from_creds_json(value: str):
    creds_json = get_creds_json()
    try:
        return creds_json["installed"][f"{value}"]
    except KeyError:
        raise KeyError("No such element in creds_file")


def get_redirect_uri():
    redirect_uris = get_value_from_creds_json("redirect_uris")
    for i in range(len(redirect_uris)):
        if "localhost" in redirect_uris[i]:
            return redirect_uris[i]


def get_endpoint_for_auth_page():
    client_id = get_value_from_creds_json("client_id")
    redirect_uri = get_redirect_uri()
    endpoint_for_auth_page = f"?client_id={client_id}&" \
                             f"response_type=code&" \
                             f"scope={Urls.GMAIL_SCOPE_URL}&" \
                             f"redirect_uri={redirect_uri}&" \
                             f"prompt=consent&" \
                             f"include_granted_scopes=true"
    return endpoint_for_auth_page
