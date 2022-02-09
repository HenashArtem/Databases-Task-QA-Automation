# coding=utf-8

import string
from framework.utils.string_data_generator import StringDataGenerator
from tests.config.string_data import StringData


class GenerateTestData(object):

    @staticmethod
    def generate_name_to_add(length: int):
        if length < StringData.name_to_add_len:
            raise ValueError(f"Name length should be at least {StringData.name_to_add_len}")

        return StringDataGenerator.generate_random_string(
            length,
            string.ascii_lowercase,
        )

    @staticmethod
    def generate_method_name_to_add(length: int):
        if length < StringData.method_name_to_add_len:
            raise ValueError(f"Method name length should be at least {StringData.method_name_to_add_len}")

        return StringDataGenerator.generate_random_string(
            length,
            string.ascii_lowercase,
        )

    @staticmethod
    def generate_env_to_add(length: int):
        if length < StringData.env_to_add_len:
            raise ValueError(f"Env length should be at least {StringData.env_to_add_len}")

        return StringDataGenerator.generate_random_string(
            length,
            string.ascii_uppercase,
        )

    @staticmethod
    def generate_name_to_update(length: int):
        if length < StringData.name_to_update_len:
            raise ValueError(f"Name length should be at least {StringData.name_to_update_len}")

        return StringDataGenerator.generate_random_string(
            length,
            string.ascii_lowercase,
        )

    @staticmethod
    def generate_method_name_to_update(length: int):
        if length < StringData.method_name_to_update_len:
            raise ValueError(f"Method name length should be at least {StringData.method_name_to_update_len}")

        return StringDataGenerator.generate_random_string(
            length,
            string.ascii_lowercase,
        )

    @staticmethod
    def generate_env_to_update(length: int):
        if length < StringData.env_to_update_len:
            raise ValueError(f"Env length should be at least {StringData.env_to_update_len}")

        return StringDataGenerator.generate_random_string(
            length,
            string.ascii_uppercase,
        )
