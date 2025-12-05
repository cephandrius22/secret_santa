#!/usr/bin/env python3

from pathlib import Path
import random

import click

OUTPUT_DIR = "gift_recipients"


def generate_pairings(people: set[str], couples: set[tuple]) -> dict[str, str]:
    pairings = {}
    taken_targets = set()
    for person in people:
        # Invalid targets include self, already taken targets, and partners
        invalid_targets = {person} | taken_targets

        for couple in couples:
            if person in couple:
                invalid_targets.update(couple)

        valid_targets = people - invalid_targets

        if not valid_targets:
            raise ValueError(f"No valid targets available for {person}")

        # Pick random person from valid_targets. You could probably
        # just call pop() here instead of random.choice, but this makes
        # me feel better.
        target = random.choice(list(valid_targets))
        pairings[person] = target
        taken_targets.add(target)

    return pairings


def verify_pairings(pairings: dict[str, str], couples: set[tuple]) -> None:
    # Verify that no one is assigned to themselves or their partner
    recipients = set(pairings.values())

    for giver, receiver in pairings.items():
        if giver == receiver:
            raise ValueError(f"{giver} is assigned to themselves.")
        for couple in couples:
            if giver in couple and receiver in couple:
                raise ValueError(f"{giver} is assigned to their partner {receiver}.")

        recipients.discard(receiver)

    if recipients:
        raise ValueError(f"Some recipients were not assigned: {recipients}")


@click.command()
@click.option(
    "--people-file",
    "-p",
    type=click.Path(exists=True),
    required=True,
    help="Path to the file containing the list of people.",
)
@click.option(
    "--couples-file",
    "-c",
    type=click.Path(exists=True),
    required=True,
    help="Path to the file containing the list of couples.",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    default=OUTPUT_DIR,
    help="Directory to output gift recipient files.",
)
def main(people_file, couples_file, output_dir):
    # Load people from file.
    try:
        people = set(Path(people_file).read_text().strip().splitlines())
    except Exception as e:
        raise RuntimeError(f"Failed to read people file: {e}")

    # Couples file is expected to have one couple per line.
    try:
        couples_lines = Path(couples_file).read_text().strip().splitlines()
        couples = [tuple(line.split(",")) for line in couples_lines]
    except Exception as e:
        raise RuntimeError(f"Failed to read couples file: {e}")

    pairings = None

    # Keep trying until we get a valid set of pairings. Brute
    # force but whatever.
    while pairings is None:
        try:
            pairings = generate_pairings(people, couples)
        except ValueError:
            pairings = None

    verify_pairings(pairings, couples)
    Path(output_dir).mkdir(exist_ok=True)

    for giver, receiver in pairings.items():
        (Path(output_dir) / f"{giver}_gift_recipient.txt").write_text(
            f"Hello, {giver}. You will be giving a gift to {receiver}.\n"
        )


if __name__ == "__main__":
    main()
