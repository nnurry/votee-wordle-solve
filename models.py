import typing as T
from enum import Enum, auto
from constants import CHARS


class CharGuessResult(Enum):
    """
    Enum representing the result of a character guess in a word-guessing game.
    """
    absent = auto()
    present = auto()
    correct = auto()

    @classmethod
    def is_correct(cls, ref: str) -> bool:
        """Checks if the guess result is correct."""
        return ref == cls.correct.name

    @classmethod
    def is_present(cls, ref: str) -> bool:
        """Checks if the guess result is present but incorrect."""
        return ref == cls.present.name

    @classmethod
    def is_absent(cls, ref: str) -> bool:
        """Checks if the character is absent in the word."""
        return ref == cls.absent.name


class CharGuessMeta(T.TypedDict):
    """
    Typed dictionary that holds metadata for a character guess.
    """
    slot: int
    guess: str
    result: CharGuessResult


class Word(T.TypedDict):
    """
    Represents a word and associated metadata.
    """
    word: str
    contain: set[str]  # Set of characters contained in the word


class Dictionary(T.TypedDict):
    """
    Represents a dictionary that maps each character to a list of words containing that character.
    """
    count: int
    contain_map: dict[str, list[Word]]

    @classmethod
    def initialize(cls) -> 'Dictionary':
        """
        Initializes a new dictionary with a count of zero and empty contain_map.
        """
        return Dictionary(
            count=0,
            contain_map={char: [] for char in CHARS},
        )
