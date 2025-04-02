import argparse
import pickle
import requests
from schemas import RandomGuessRequest, RandomGuessResponse
from models import Dictionary, CharGuessResult
from constants import CHARS, MAX_SIZE
from pprint import pformat

BASE_URL = "https://wordle.votee.dev:8000"


def guess_random_word(guess: str, size: int, seed: int, verbose=True):
    """Makes a guess to the Wordle-like game API and returns the response."""
    if verbose:
        print(f"Making a guess: {guess}, size: {size}, seed: {seed}")

    # Prepare the request
    scheme = RandomGuessRequest.init(
        {"guess": guess, "seed": seed, "size": size}, BASE_URL
    )

    try:
        response = requests.request(
            scheme["method"],
            scheme["url"],
            params=scheme["params"],
            timeout=10,  # Adding a timeout to avoid hanging on bad network
        )
        status = response.status_code
        if status != 200:
            if verbose:
                print(f"Error: Received a non-200 response: {status}")
                print(response.content)
            return None

        body = response.json() if status == 200 else []
        final_response = RandomGuessResponse({"status": status, "body": body})
        return final_response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def build_keyword(size: int, seed: int):
    """Builds a set of possible characters by making guesses."""
    print("Building possible characters...")
    possible_chars = set()

    for idx in range(0, len(CHARS), size):
        if len(possible_chars) >= size:
            break

        chars = CHARS[idx : idx + size]
        word = "".join(chars)

        # Ensure the word length is consistent with 'size'
        if len(word) < size:
            word += "z" * (size - len(word))  # Pad the word with 'z' if needed

        resp = guess_random_word(word, size, seed, verbose=False)
        if resp is None:
            continue

        # Check if the guessed characters are present or correct
        for guess_meta in resp["body"]:
            result = guess_meta["result"]
            is_char_included = CharGuessResult.is_present(
                result
            ) or CharGuessResult.is_correct(result)
            if is_char_included:
                possible_chars.add(guess_meta["guess"])
                if len(possible_chars) >= size:
                    break

    print(f"Possible characters identified: {possible_chars}")
    return possible_chars


def process_dictionary(size: int, possible_chars: set[str]):
    """Load dictionary for given word size and filter possible words."""
    possible_words = set()
    try:
        with open(f"data/dictionary-len_{size}.pkl", "rb") as pkl_file:
            dictionary: Dictionary = pickle.load(pkl_file)
    except FileNotFoundError:
        print("WARN: Can't retrieve the corpus")
        print(
            "WARN: Reason:", 
            f"No dictionary for keywords this big (len={size} > len={MAX_SIZE - 1})" 
            if size > MAX_SIZE - 1 
            else f"No dictionary for keyword of this size (len={size})",
        )
    else:
        # Filter words based on the identified possible characters
        for possible_char in possible_chars:
            for word in dictionary["contain_map"].get(possible_char, []):
                is_diff = possible_chars != word["contain"]
                if not is_diff:
                    possible_words.add(word["word"])

    return possible_words


def play(size: int, seed: int):
    """Main game loop for guessing words."""
    possible_chars = build_keyword(size, seed)
    possible_words = process_dictionary(size, possible_chars)

    is_matched = False
    match_map = "?" * size

    print(f"Total possible words to check: {len(possible_words)}")

    for i, possible_word in enumerate(possible_words):
        print(f"Making guess number {i+1}: {possible_word}")
        response = guess_random_word(possible_word, size, seed)

        if response is None:
            continue

        is_matched = RandomGuessResponse.is_matched(response)
        match_map = RandomGuessResponse.get_match_map(response)
        output_str = f"Guess no. {i+1}: \t{match_map}"

        if is_matched:
            print("-" * 64)
            output_str = f"{output_str} -> MATCHED!!"
            print(output_str)
            print("-" * 64)
            print("Response details:\n", pformat(response["body"]))
            break
        else:
            print(output_str)

    if not is_matched:
        print("-" * 64)
        print("ERR: Can't guess the keyword from the corpus ...")
        print("-" * 64)

    return match_map, is_matched


def main():
    """Set up argument parsing and start the game."""
    parser = argparse.ArgumentParser(
        description="Play the random word guessing game with a specified size and seed."
    )

    # Define the command-line arguments
    parser.add_argument(
        "--size",
        type=int,
        required=True,
        help="The size of the word to guess (e.g., 5 for a 5-letter word).",
    )

    parser.add_argument(
        "--seed",
        type=int,
        required=True,
        help="The seed value to use for the randomization.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Starting message
    print(
        f"Starting the guessing game with word size = {args.size} and seed = {args.seed}"
    )

    # Call the play function
    play(args.size, args.seed)


if __name__ == "__main__":
    main()
