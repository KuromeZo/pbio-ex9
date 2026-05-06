# Album number: s30068
# Date: 2026
# Description: Random DNA sequence generator in FASTA format with statistics,
#              motif search, complementary sequences, transcription, and GC sliding window.

import random
import csv


def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    """Gets an integer from the user in a specified range.
    Repeats the question if the input is invalid instead of raising an exception."""
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")
        except ValueError:
            print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")


def validate_id(prompt: str) -> str:
    """Gets a sequence ID from the user.
    The ID cannot contain whitespace - repeats the question if it does."""
    while True:
        seq_id = input(prompt)
        if seq_id and " " not in seq_id and "\t" not in seq_id:
            return seq_id
        else:
            print("Error: ID cannot be empty or contain whitespace.")


def generate_sequence(length: int) -> str:
    """Returns a random DNA sequence of the specified length.
    Uses only standard nucleotides: A, C, G, T."""
    nucleotides = ["A", "C", "G", "T"]
    return "".join(random.choice(nucleotides) for _ in range(length))


def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    """Returns a formatted FASTA record as a string.
    Header: >ID description
    Sequence is broken into lines of exactly line_width characters."""
    if description:
        header = f">{seq_id} {description}"
    else:
        header = f">{seq_id}"

    lines = [sequence[i:i + line_width] for i in range(0, len(sequence), line_width)]

    return header + "\n" + "\n".join(lines)


def main():
    """Main function - orchestrates user input, sequence generation, and output."""

    length = validate_positive_int("Enter sequence length: ")
    seq_id = validate_id("Enter sequence ID: ")
    description = input("Enter a description of the sequence: ")

    sequence = generate_sequence(length)

    fasta_content = format_fasta(seq_id, description, sequence)
    filename = f"{seq_id}.fasta"

    with open(filename, "w") as f:
        f.write(fasta_content + "\n")

    print(f"Sequence saved to file: {filename}")


if __name__ == "__main__":
    main()