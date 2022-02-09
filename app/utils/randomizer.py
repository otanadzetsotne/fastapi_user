from string import digits, ascii_letters
from random import choice


# TODO: move to settings
REGISTRATION_CONFIRMATION_CODE_LENGTH = 8
LETTERS = digits + ascii_letters


class Randomizer:
    @staticmethod
    def registration_confirmation_code() -> str:
        """
        Generate random code from letters to user registration confirmation
        """

        return ''.join((
            choice(LETTERS)
            for _ in range(REGISTRATION_CONFIRMATION_CODE_LENGTH)
        ))
