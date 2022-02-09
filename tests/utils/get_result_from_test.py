import json


def get_test_result():
    with open("test_results.json", "r") as file:
        file_data = dict(json.load(file))
        if file_data.get("test_result") is not None:
            return True
