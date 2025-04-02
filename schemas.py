import typing as T
from models import CharGuessMeta, CharGuessResult


class RandomGuessRequest(T.TypedDict):
    class Params(T.TypedDict):
        guess: str
        size: int
        seed: int

    params: Params
    body: T.Optional[T.Any]
    method: str
    url: str

    @classmethod
    def init(cls, params: Params, base_url: str):
        # Initializes the request with method 'GET' and a dynamic URL.
        return RandomGuessRequest(params=params, method="GET", url=f"{base_url}/random")


class RandomGuessResponse(T.TypedDict):
    status: int
    body: T.Optional[list[CharGuessMeta]]

    @classmethod
    def is_matched(cls, ref: "RandomGuessResponse"):
        # Checks if all guesses in the response are correct.
        if not ref["body"]:
            return False

        for result in ref["body"]:
            is_correct = CharGuessResult.is_correct(result["result"])
            if not is_correct:
                return False

        return True

    @classmethod
    def get_match_map(cls, ref: "RandomGuessResponse"):
        # Builds a string of matched characters, '?' for incorrect guesses.
        if not ref["body"]:
            return ""

        match_map = ""

        for result in ref["body"]:
            is_correct = CharGuessResult.is_correct(result["result"])
            char = result["guess"] if is_correct else "?"
            match_map += char

        return match_map
