import json
import random
from datetime import datetime

from framework.constants.date_time_constants import TEST_TIME_FORMAT
from framework.utils.database_util import DatabaseUtil
from framework.utils.logger import Logger
from tests.config.browser import BrowserConfig
from tests.config.sql_params import SqlParams
from tests.test_data.sql_queries import SqlQueries
from tests.utils.db_string_data_generator import GenerateTestData


class ProjectDbUtil:
    my_sql_queries = SqlQueries()

    db_util = DatabaseUtil(host=SqlParams.host,
                           user=SqlParams.user,
                           password=SqlParams.db_password,
                           database=SqlParams.database_name)

    def get_status_from_db_table(self):
        Logger.info("Getting status from DB table")
        db_res = self.db_util.select_db_data(column_name="*",
                                             name="status")
        return dict(db_res)

    def get_correct_key_of_test_res(self):
        Logger.info("Getting correct key of test result from DB table")
        with open("test_results.json", "r") as file:
            file_data = dict(json.load(file))
        db_test_res = self.get_status_from_db_table()
        for db_key, db_value in db_test_res.items():
            for file_value in file_data.values():
                if str(db_value).upper() == str(file_value).upper():
                    return db_key

    def get_random_project_id(self):
        Logger.info("Getting random project_id from DB table")
        db_res = self.db_util.select_db_data(column_name="id",
                                             name="project")
        list_of_id = list()
        for keys in db_res:
            for values in keys:
                list_of_id.append(values)
        return random.choice(list_of_id)

    def get_random_session_id(self):
        Logger.info("Getting random session_id from DB table")
        db_res = self.db_util.select_db_data(column_name="session_id",
                                             name="test")
        list_of_id = list()
        for keys in db_res:
            for value in keys:
                list_of_id.append(value)
        return random.choice(list_of_id)

    def add_test_data_to_db_table(self, name_size, method_name_size, env_size):
        Logger.info("Adding test data to DB table")
        with open("test_results.json", "r") as file:
            file_data = dict(json.load(file))
            for key, value in file_data.items():
                if key == "test_start_time":
                    test_start_time = file_data[key]

        with open("test_results.json", "r") as file:
            file_data = dict(json.load(file))
            for key, value in file_data.items():
                if key == "test_end_time":
                    test_end_time = file_data[key]

        query = self.my_sql_queries.insert_data_to_test(GenerateTestData.generate_name_to_add(name_size),
                                                        self.get_correct_key_of_test_res(),
                                                        GenerateTestData.generate_method_name_to_add(method_name_size),
                                                        self.get_random_project_id(),
                                                        self.get_random_session_id(),
                                                        test_start_time,
                                                        test_end_time,
                                                        GenerateTestData.generate_env_to_add(env_size),
                                                        BrowserConfig.BROWSER)
        self.db_util.send_db_query(query, fetchall=False)

    def get_db_table_res_after_add(self):
        Logger.info("Getting DB table results after data adding")
        with open("test_results.json", "r") as file:
            file_data = dict(json.load(file))
            for key, value in file_data.items():
                if key == "test_end_time":
                    test_end_time = file_data[key]
        query = self.my_sql_queries.select_all_from_test_where_end_time(test_end_time)
        db_res = self.db_util.send_db_query(query, fetchall=True)
        return db_res

    def select_double_ids_test_nums(self):
        Logger.info("Selecting double id's test nums from DB table")
        db_res = self.db_util.select_db_data(column_name="id",
                                             name="test")
        list_of_id = list()
        set_of_double_ids = set()
        for keys in db_res:
            for value in keys:
                list_of_id.append(str(value))
        for item in list_of_id:
            if item == "333":
                pass
            else:
                int_list_of_num_digits = [int(int_digit) for int_digit in item.strip()]
                if len(int_list_of_num_digits) >= 2:
                    for digit in range(len(int_list_of_num_digits) - 1):
                        if int_list_of_num_digits[digit] == int_list_of_num_digits[digit + 1]:
                            if len(set_of_double_ids) < 10:
                                set_of_double_ids.add(item)
                            else:
                                break
        list_of_double_id_select_res = list()
        for double_id in list(set_of_double_ids):
            query = self.my_sql_queries.select_all_from_test_where_id(double_id)
            list_of_double_id_select_res.append(self.db_util.send_db_query(query, fetchall=True))
        return list_of_double_id_select_res

    def insert_data_to_table(self):
        Logger.info("Inserting data to DB table")
        dict_of_added_data_res = dict(id="",
                                      name="",
                                      status_id="",
                                      method_name="",
                                      project_id="",
                                      session_id="",
                                      start_time="",
                                      end_time="",
                                      env="",
                                      browser="",
                                      author_id="")
        list_of_dict_keys = list()
        list_of_dicts = list()
        list_of_double_id_select_res = self.select_double_ids_test_nums()
        for key in dict_of_added_data_res.keys():
            list_of_dict_keys.append(key)
        for result in list_of_double_id_select_res:
            for item in result:
                list_of_dicts.append(dict(zip(list_of_dict_keys, list(item))))

        for res in list_of_dicts:
            query = self.my_sql_queries.insert_data_to_test(str(res.get('name')),
                                                            str(res.get('status_id')),
                                                            str(res.get('method_name')),
                                                            str(res.get('project_id')),
                                                            str(res.get('session_id')),
                                                            str(res.get('start_time')),
                                                            str(res.get('end_time')),
                                                            str(res.get('env')),
                                                            str(res.get('browser')))
            self.db_util.send_db_query(query, fetchall=False)

    def get_inserted_data_res(self):
        Logger.info("Getting DB table results after inserting data")
        db_res_before_insert = self.db_util.select_db_data(column_name="*",
                                                           name="test")
        self.insert_data_to_table()
        db_res_after_insert = self.db_util.select_db_data(column_name="*",
                                                          name="test")
        list_of_inserted_data = list(set(db_res_after_insert) - set(db_res_before_insert))
        list_of_inserted_data_ids = list()
        for item in list_of_inserted_data:
            list_of_inserted_data_ids.append(item[0])
        return sorted(list_of_inserted_data_ids)

    def update_data_in_db_table(self, name_size, method_name_size, env_size, list_of_ids):
        Logger.info("Updating data in DB table")
        list_of_inserted_ids = list_of_ids
        for item in list_of_inserted_ids:
            now = datetime.now()
            name = GenerateTestData.generate_name_to_update(name_size),
            status_id = f"{random.randint(1, 3)}",
            method_name = GenerateTestData.generate_method_name_to_update(method_name_size),
            project_id = f"{self.get_random_project_id()}",
            session_id = f"{self.get_random_session_id()}",
            start_time = f"{str(now.strftime(f'{TEST_TIME_FORMAT}'))}",
            end_time = f"{str(now.strftime(f'{TEST_TIME_FORMAT}'))}",
            env = GenerateTestData.generate_env_to_add(env_size),
            browser = BrowserConfig.BROWSER
            query = self.my_sql_queries.update_test_data_in_table_where_id(name=name,
                                                                           status_id=status_id,
                                                                           method_name=method_name,
                                                                           project_id=project_id,
                                                                           session_id=session_id,
                                                                           test_start_time=start_time,
                                                                           test_end_time=end_time,
                                                                           env=env,
                                                                           browser=browser,
                                                                           id_el=item)
            self.db_util.send_db_query(query, fetchall=False)

    def get_uploaded_data_from_db_table(self, list_of_uploaded_data_ids):
        Logger.info("Getting uploaded data from DB table")
        list_of_res = list()
        for i in list_of_uploaded_data_ids:
            query = self.my_sql_queries.select_all_from_test_where_id(i)
            list_of_res.append(self.db_util.send_db_query(query, fetchall=True))
        return list_of_res

    def get_deletion_inserted_data_res(self, list_of_inserted_data_ids):
        Logger.info("Deleting inserted data and getting results")
        for i in list_of_inserted_data_ids:
            query = self.my_sql_queries.delete_from_test_where_id(i)
            self.db_util.send_db_query(query, fetchall=False)

    def check_deletion_of_inserted_data(self, list_of_inserted_data_ids):
        Logger.info("Checking for deletion of inserted data")
        list_of_db_res = list()
        for i in list_of_inserted_data_ids:
            query = self.my_sql_queries.select_all_from_test_where_id(i)
            list_of_db_res.append(self.db_util.send_db_query(query, fetchall=True))

        iter_of_null_elements_in_list = 0
        for item in list_of_db_res:
            if len(item) == 0:
                pass
            else:
                iter_of_null_elements_in_list += 1
        if iter_of_null_elements_in_list == 0:
            return True
