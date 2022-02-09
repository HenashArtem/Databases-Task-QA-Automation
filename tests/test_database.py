from tests.utils.project_db_util import ProjectDbUtil
from tests import test_gmail_api_euronews
from tests.utils.get_result_from_test import get_test_result
from tests.test_data.db_test_data import DatabaseTestData


class TestDatabase(object):

    def test_gmail_api(self, create_browser):
        test_gmail_api = test_gmail_api_euronews.TestGmailApiEuronews()
        test_gmail_api.test_get_auth_code(create_browser)

    def test_add_test_result_data_to_db(self, set_setup_and_turndown_db_params):
        assert get_test_result() is True, "Test wasn't finished"

        proj_db_util = ProjectDbUtil()
        proj_db_util.add_test_data_to_db_table(DatabaseTestData.name_to_add_size,
                                               DatabaseTestData.method_name_to_add_size,
                                               DatabaseTestData.env_to_add_size)
        db_res_after_add = proj_db_util.get_db_table_res_after_add()
        assert len(db_res_after_add) != 0, "Test result wasn't added to the table"

    def test_working_with_test_data_in_db(self, set_setup_and_turndown_db_params):
        proj_db_util = ProjectDbUtil()
        list_of_inserted_ids = proj_db_util.get_inserted_data_res()
        proj_db_util.update_data_in_db_table(DatabaseTestData.name_to_update_size,
                                             DatabaseTestData.method_name_to_update_size,
                                             DatabaseTestData.env_to_update_size, list_of_inserted_ids)
        list_of_uploaded_res = proj_db_util.get_uploaded_data_from_db_table(list_of_inserted_ids)
        assert len(list_of_uploaded_res) != 0, "Data in database table wasn't uploaded"
        proj_db_util.get_deletion_inserted_data_res(list_of_inserted_ids)
        assert proj_db_util.check_deletion_of_inserted_data(list_of_inserted_ids) is True, "Inserted data to " \
                                                                                           "table wasn't deleted "
