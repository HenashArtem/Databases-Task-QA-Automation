class SqlQueries:

    @staticmethod
    def insert_data_to_test(name, status_id, method_name,
                            project_id, session_id, test_start_time,
                            test_end_time, env, browser):
        query = f"""insert into test(
            name, status_id, method_name, project_id, session_id, start_time, end_time, env, browser) 
            VALUES("{name}", "{status_id}", "{method_name}", "{project_id}", "{session_id}", "{test_start_time}", 
            "{test_end_time}", "{env}", "{browser}");"""
        return str(query)

    @staticmethod
    def select_all_from_test_where_end_time(test_end_time):
        query = f"select * from test where end_time='{test_end_time}';"
        return str(query)

    @staticmethod
    def update_test_data_in_table_where_id(name, status_id, method_name,
                                           project_id, session_id, test_start_time,
                                           test_end_time, env, browser, id_el):
        query = f"""UPDATE test SET name="{name}",
                                    status_id="{status_id}",
                                    method_name="{method_name}",
                                    project_id="{project_id}",
                                    session_id="{session_id}",
                                    start_time="{test_start_time}",
                                    end_time="{test_end_time}",
                                    env="{env}",
                                    browser="{browser}" 
                                    WHERE id="{str(id_el)}";"""
        return str(query)

    @staticmethod
    def select_all_from_test_where_id(el_id):
        query = f"select * from test where id='{el_id}'"
        return str(query)

    @staticmethod
    def delete_from_test_where_id(el_id):
        query = f"""delete from test where id="{el_id}";"""
        return str(query)
