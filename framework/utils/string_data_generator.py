# coding=utf-8

import string
import random
from typing import List


class StringDataGenerator:

    @staticmethod
    def generate_random_string(length: int, *choices: str) -> str:
        """
        Generate a string of a given `length`.
        The result has at least one symbol from each of `choices` if `length` allows.
        Arguments:
            length -- Result string length.
            choices -- Strings with available symbols.
        """
        if not choices:

            choices = (string.ascii_letters,)

        all_choices = "".join(choices)
        result: List[str] = []
        choice_index = 0
        while len(result) < length:
            if choice_index < len(choices):
                symbol = random.choice(choices[choice_index])
                result.append(symbol)
                choice_index += 1
                continue

            symbol = random.choice(all_choices)
            result.append(symbol)

        random.shuffle(result)
        return "".join(result)
