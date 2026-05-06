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


def calculate_stats(sequence: str) -> dict:
    """Returns a dictionary of sequence statistics.
    Keys: 'A', 'C', 'G', 'T' (float values, %), 'GC' (float value, %)."""
    clean = [c for c in sequence if c.upper() in "ACGT"]
    total = len(clean)

    if total == 0:
        return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "GC": 0.0}

    counts = {"A": 0, "C": 0, "G": 0, "T": 0}
    for nucleotide in clean:
        counts[nucleotide.upper()] += 1

    stats = {base: round(counts[base] / total * 100, 2) for base in "ACGT"}
    stats["GC"] = round((counts["G"] + counts["C"]) / total * 100, 2)
    return stats


def insert_name(sequence: str, name: str) -> str:
    """Inserts a name at a random position in the sequence.
    Name is written in lowercase so it is visually distinguishable from nucleotides."""
    position = random.randint(0, len(sequence))
    return sequence[:position] + name.lower() + sequence[position:]


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


def find_motif(sequence: str, motif: str) -> list:
    """Searches for all occurrences of a motif in the sequence.
    Returns a list of positions (1-based indexing, biological convention)."""
    positions = []
    clean_seq = "".join(c for c in sequence if c.isupper())
    start = 0
    while True:
        pos = clean_seq.find(motif.upper(), start)
        if pos == -1:
            break
        positions.append(pos + 1)
        start = pos + 1
    return positions


def reverse_complement(sequence: str) -> str:
    """Returns the reverse complementary strand of a DNA sequence.
    Complement: A<->T, C<->G. Then reverse the result."""
    complement_map = {"A": "T", "T": "A", "C": "G", "G": "C"}
    complement = ""
    for base in sequence:
        if base.upper() in complement_map:
            comp = complement_map[base.upper()]
            complement += comp if base.isupper() else comp.lower()
        else:
            complement += base
    return complement[::-1]


def transcribe_to_mrna(sequence: str) -> str:
    """Performs in silico transcription: replaces T with U to get mRNA sequence.
    Lowercase letters (user name) are preserved as-is."""
    return sequence.replace("T", "U").replace("t", "u")


def main():
    """Main function - orchestrates user input, sequence generation, and output."""

    length = validate_positive_int("Enter sequence length: ")
    seq_id = validate_id("Enter sequence ID: ")
    description = input("Enter a description of the sequence: ")
    name = input("Enter your name: ")

    sequence = generate_sequence(length)
    sequence_with_name = insert_name(sequence, name)

    fasta_content = format_fasta(seq_id, description, sequence_with_name)
    filename = f"{seq_id}.fasta"

    with open(filename, "w") as f:
        f.write(fasta_content + "\n")

    print(f"Sequence saved to file: {filename}")

    stats = calculate_stats(sequence)
    print(f"\nSequence statistics (n={length}):")
    for base in ["A", "C", "G", "T"]:
        print(f"  {base}: {stats[base]:.2f}%")
    print(f"  GC-content: {stats['GC']:.2f}%")

    motif = input("\nEnter a motif to search for (e.g. ATG), or press Enter to skip: ").strip()
    if motif:
        positions = find_motif(sequence, motif)
        if positions:
            print(f"Motif '{motif.upper()}' found at positions: {positions}")
        else:
            print(f"Motif '{motif.upper()}' not found in the sequence.")

    print("\nGenerating complementary sequences...")
    rev_comp = reverse_complement(sequence)
    comp_fasta = format_fasta(seq_id + "_revcomp", "Reverse complement", rev_comp)

    with open(filename, "a") as f:
        f.write("\n" + comp_fasta + "\n")
    print(f"Reverse complement added to {filename}")

    mrna = transcribe_to_mrna(sequence)
    mrna_fasta = format_fasta(seq_id + "_mRNA", "mRNA transcript (T->U)", mrna)

    with open(filename, "a") as f:
        f.write("\n" + mrna_fasta + "\n")
    print(f"mRNA transcript added to {filename}")


if __name__ == "__main__":
    main()