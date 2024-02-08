from csv import DictReader
from sys import argv, exit
from os import path
from typing import List, Dict


def get_database_rows(database_file: str) -> List[Dict: str]:
    """Get database data from csv file into a list of dicts"""

    if (not database_file.endswith(".csv") or not path.isfile(database_file)):
        print("Could not open csv file")
        return 1

    db_rows = []
    with open(database_file, "r") as file:
        reader = DictReader(file)
        for row in reader:
            db_rows.append(row)

    return db_rows


def get_dna_sequence(dna_file: str) -> str:
    """Get sequence data from txt file into a str"""

    if (not dna_file.endswith(".txt") or not path.isfile(dna_file)):
        print("Could not open txt file")
        return 1

    with open(dna_file, "r") as file:
        dna_sequence = file.read()

    return dna_sequence


def get_dna_profile(dna_sequence: str, sequence_list: List[str]) -> dict[str, str]:
    """Get dna profile from dna sequence"""

    dna_profile = {}
    for subsequence in sequence_list:
        dna_profile[subsequence] = str(
            longest_match(dna_sequence, subsequence))

    return dna_profile


def check_matching_profiles(db_rows: List[Dict: str], dna_profile: dict[str, str],
                            name_col: str, sequence_list: List[str]) -> None:
    """Check matching dna profiles for dna sequence"""

    for profile in db_rows:
        match_count = 0
        for subsequence in sequence_list:
            if profile[subsequence] == dna_profile[subsequence]:
                profile_name = profile[name_col]
                match_count += 1

        full_match = match_count == len(sequence_list)

        if full_match:
            print(profile_name)
            return

    print("No match")


def main() -> None:
    """Check matching dna profiles in the database for a given dna sequence file"""

    # Read command-line arguments

    if len(argv) != 3:
        print("Usage: python dna.py databases/small.csv sequences/1.txt")
        exit(1)

    database_file = argv[1]
    dna_file = argv[2]

    # Read database file into a variable

    db_rows = get_database_rows(database_file)

    # Read DNA sequence file into a variable
    dna_sequence = get_dna_sequence(dna_file)

    # Find longest match of each STR in DNA sequence
    name_col = "name"
    sequence_list = list(db_rows[0].keys())
    sequence_list.remove(name_col)
    dna_profile = get_dna_profile(dna_sequence, sequence_list)

    # Check database for matching profiles

    check_matching_profiles(db_rows, dna_profile, name_col, sequence_list)


def longest_match(sequence: str, subsequence: str) -> int:
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in sequence, return longest run found
    return longest_run


if __name__ == "__main__":
    main()
