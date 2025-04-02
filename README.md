# Wordle Solver

This repository contains a Python-based solver for a Wordle-like game. It makes random guesses and refines those guesses based on feedback received from an API that simulates a Wordle-style game hosted by Votee. The solver uses external API calls and filters possible words based on feedback, progressively narrowing down the correct word.


## Table of Contents

- [Installation](#installation)
- [Running the Solver](#running-the-solver)
- [Preprocessing the Word List](#preprocessing-the-word-list)
- [How It Works](#how-it-works)
- [Code Walkthrough](#code-walkthrough)
- [Example Output](#example-output)
- [Acknowledgements](#acknowledgements)

## Installation

To run the Wordle solver, you need to install the required dependencies. Use the following command:

```bash
pip install -r requirements.txt
```

Ensure that Python 3.7 or later is installed on your system (tested with Python 3.10.12, Python 3.12.3, recommended to use `virtualenv` for isolating environment of this script). 

## Running the Solver

To start the Wordle solver, run the `wordle_solver.py` script with the following command-line arguments:

```bash
python wordle_solver.py --size <word_size> --seed <seed_value>
```

### Arguments:
- `--size`: The number of characters in the word (e.g., `5` for a 5-letter word).
- `--seed`: A seed value used to initialize randomization in the solver.

### Example:

```bash
python wordle_solver.py --size 5 --seed 1234
```
This command will start the solver for a 5-letter word, using the seed value 1234.

## Preprocessing the Word List

Before running the solver, you need to preprocess the word list. This is done by running the `preprocess.py` script, which generates dictionaries of words by their length from multiple sources.

Run the script like this:

```bash
python preprocess.py
```
The script performs the following actions:
- Reads words from `data/words.txt` (sourced from the [dwyl/english-words](https://github.com/dwyl/english-words) repository).
- Pulls additional words from NLTK's Gutenberg and WordNet corpora.
- Filters out any invalid words (those containing characters outside the valid character set).
- Saves the processed dictionaries in pickle format (e.g., `dictionary-len_X.pkl`, where `X` is the word length).

### Notes:
- You need the `nltk` library to download corpora from NLTK (Gutenberg and WordNet). If they aren't already downloaded, the script will handle this automatically.
- If the target word is not in our corpus, the solver will **not** attempt to brute-force or generate permutations. Only words present in the preprocessed word list will be considered.

## How It Works

### Guessing:
The solver generates a set of initial possible characters based on the word size and a seed value. It then interacts with an external API to make guesses.

### Filtering Words:
After each guess, feedback from the API helps filter out words that do not match the known constraints (e.g., words that do not contain a correct character in a specific position).

### Matching:
The solver continues making guesses, adjusting each subsequent guess based on the feedback, until the correct word is found or all possibilities are exhausted. If the word is not in the preprocessed corpus, it will not attempt brute-force permutations.

## Docker Setup

The project can also be run in a Docker container for ease of use and portability. Below are the steps to build and execute the containerized application.

### Dockerfile

The provided `Dockerfile` sets up a lightweight Python environment for running the Wordle solver.

```dockerfile
# Use the official Python 3.12 Alpine image as the base image
FROM python:3.12-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file to leverage Docker's caching mechanism
COPY requirements.txt ./

# Install Python dependencies specified in requirements.txt
# --no-cache-dir: Avoid caching to reduce image size
RUN pip install --no-cache-dir --requirement requirements.txt

# Copy Python source files and the words.txt file into the container
COPY *.py words.txt ./
```
This `Dockerfile` does the following:

- Starts with a minimal Alpine-based Python 3.12 image.
- Sets `/app` as the working directory in the container.
- Copies the `requirements.txt` file and installs the required Python dependencies.
- Then, it copies all Python source files (`*.py`) and `words.txt` into the container's working directory.

## Execution Script

The `execute.bash` script automates building and running the Docker container. It provides flexibility to build the image and execute scripts within the container.

### Script Details

```bash
#!/bin/bash

# Exit script on error
set -e

# Define variables
IMAGE_NAME="votee-wordle-solver"
CONTAINER_NAME="votee-wordle-solver"

# Check if the first argument is '--build'
BUILD_IMAGE=false
if [ "$1" == "--build" ]; then
    BUILD_IMAGE=true
    shift # Remove the '--build' argument from the list
fi

# Step 1: Build the Docker image (if flagged)
if [ "$BUILD_IMAGE" = true ]; then
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME .
else
    echo "Skipping Docker image build..."
fi

# Step 2: Run the Docker container
echo "Running Docker container..."
docker run \
    --rm \
    --name $CONTAINER_NAME \
    --interactive \
    --volume $CONTAINER_NAME:/app \
    --tty \
    $IMAGE_NAME "$@"
```

This `Dockerfile` does the following:

- It defines variables for the image and container name.
- It checks if the first argument passed is --build. If so, it builds the Docker image; otherwise, it skips the build step.
- Then, it runs the Docker container with the specified arguments.

## Usage Examples

### Execute `wordle_solver.py` Without Rebuilding:

```bash
bash execute.bash python3 wordle_solver.py --size 6 --seed 8
```
### Execute `wordle_solver.py` With Rebuilding:

```bash
bash execute.bash --build python3 wordle_solver.py --size 6 --seed 8
```
### Execute `preprocess.py` With Rebuilding:

```bash
bash execute.bash --build python3 preprocess.py
```

## Example Output

When running the solver, you’ll see output like this:

```bash
(.venv) nnurry@wsl:~/Code/Votee$ python3.12 wordle_solver.py --size 22 --seed 3
Starting the guessing game with word size = 22 and seed = 3
Building possible characters...
Possible characters identified: {'n', 'g', 'y', 'a', 'e', 'c', 'o', 't', 'r', 'l', 'h', 'p'}
Total possible words to check: 1
Making guess number 1: electroencephalography
Making a guess: electroencephalography, size: 22, seed: 3
----------------------------------------------------------------
Guess no. 1:    electroencephalography -> MATCHED!!
----------------------------------------------------------------
Response details:
 [{'guess': 'e', 'result': 'correct', 'slot': 0},
  {'guess': 'l', 'result': 'correct', 'slot': 1},
  {'guess': 'e', 'result': 'correct', 'slot': 2},
  {'guess': 'c', 'result': 'correct', 'slot': 3},
  {'guess': 't', 'result': 'correct', 'slot': 4},
  {'guess': 'r', 'result': 'correct', 'slot': 5},
  {'guess': 'o', 'result': 'correct', 'slot': 6},
  {'guess': 'e', 'result': 'correct', 'slot': 7},
  {'guess': 'n', 'result': 'correct', 'slot': 8},
  {'guess': 'c', 'result': 'correct', 'slot': 9},
  {'guess': 'e', 'result': 'correct', 'slot': 10},
  {'guess': 'p', 'result': 'correct', 'slot': 11},
  {'guess': 'h', 'result': 'correct', 'slot': 12},
  {'guess': 'a', 'result': 'correct', 'slot': 13},
  {'guess': 'l', 'result': 'correct', 'slot': 14},
  {'guess': 'o', 'result': 'correct', 'slot': 15},
  {'guess': 'g', 'result': 'correct', 'slot': 16},
  {'guess': 'r', 'result': 'correct', 'slot': 17},
  {'guess': 'a', 'result': 'correct', 'slot': 18},
  {'guess': 'p', 'result': 'correct', 'slot': 19},
  {'guess': 'h', 'result': 'correct', 'slot': 20},
  {'guess': 'y', 'result': 'correct', 'slot': 21}]

```
The solver will continue making guesses and displaying feedback until it finds a match, or it will display an error message if it cannot guess the correct word.

## Acknowledgements

- The base word repository (`words.txt`) is sourced from the [dwyl/english-words](https://github.com/dwyl/english-words) GitHub repository.
- The Wordle-like API is used to simulate the guessing game and is provided by Votee. You can find its documentation [here](https://wordle.votee.dev:8000/redoc).
- This project leverages various resources, including the NLTK corpus, to enrich the word list.
- Special thanks to ChatGPT for assisting with generating code comments, prettifying the code, guiding through bash script and helping craft the README.
