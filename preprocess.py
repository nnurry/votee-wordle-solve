import os
import pickle
import typing as T
from collections import defaultdict

import nltk
from nltk.corpus import gutenberg, wordnet
from models import Word, Dictionary
from constants import CHAR_SET, MAX_SIZE

# Download necessary NLTK resources if not already downloaded
nltk.download("gutenberg")
nltk.download("wordnet")

# Create directory for word repository
os.makedirs("data", mode=0o777, exist_ok=True)


def generate_words() -> T.Iterator[str]:
    """Generate words from multiple sources: a custom file, Gutenberg, and WordNet."""
    # From the local file
    with open("words.txt", "r") as txt_file:
        for word in txt_file:
            yield word.strip().lower()

    # From NLTK's Gutenberg corpus
    for word in gutenberg.words():
        yield word.strip().lower()

    # From NLTK's WordNet corpus
    for word in wordnet.words():
        yield word.strip().lower()


def initialize_size_dictionary() -> dict[int, Dictionary]:
    """Initialize a dictionary to store words by their length."""
    return {size: Dictionary.initialize() for size in range(1, MAX_SIZE)}


def process_word(word: str, size_dictionary: dict[int, Dictionary]) -> None:
    """Process a single word, updating dictionaries by word length and character set."""
    # Skip words containing characters not in the allowed CHAR_SET
    word_chars = set(word)
    if not CHAR_SET.issuperset(word_chars):
        return

    word_len = len(word)

    # Create a Word object to represent the word
    word_wrap = Word(
        {
            "word": word,
            "contain": word_chars,
        }
    )

    # Ensure that the dictionary for this word length exists
    dictionary = size_dictionary.get(word_len)
    if dictionary:
        contain_map = dictionary.get("contain_map")
        count = dictionary.get("count")

        # Update the contain_map with the new word
        for word_char in word_chars:
            contain_map[word_char].append(word_wrap)

        # Increment the count for this length of word
        dictionary["count"] = count + 1


def save_dictionary(size_dictionary: dict[int, Dictionary]) -> None:
    """Dump the dictionaries for each word length to disk."""
    for size, dictionary in size_dictionary.items():
        if not dictionary["count"]:
            continue

        filepath = f"data/dictionary-len_{size}.pkl"
        with open(filepath, "wb") as pkl_dict:
            print(f"Dumped {size}-character-long dictionary to {filepath}")
            pickle.dump(dictionary, pkl_dict)


def main():
    # Initialize the dictionary for word sizes (1-79 characters)
    size_dictionary = initialize_size_dictionary()

    # Process each word from the various sources
    for word in generate_words():
        # Process the word and update the size_dictionary
        process_word(word, size_dictionary)

    # Save the dictionaries to disk
    save_dictionary(size_dictionary)


if __name__ == "__main__":
    main()
