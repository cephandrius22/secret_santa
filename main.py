#!/usr/bin/env python3

from pathlib import Path
import random


PEOPLE = {
    "Joe",
    "Emily",
    "Megan",
    "Marcus",
    "Jeremy",
    "Ben",
    "Rachel",
    "Alec",
    "Courtney"
}

COUPLES = {
    ("Joe", "Emily"),
    ("Megan", "Marcus"),
    ("Alec", "Courtney"),
}

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

def verifty_pairings(pairings: dict[str, str]) -> None:
    # Verify that no one is assigned to themselves or their partner
    recipients = set(pairings.values())

    for giver, receiver in pairings.items():
        if giver == receiver:
            raise ValueError(f"{giver} is assigned to themselves.")
        for couple in COUPLES:
            if giver in couple and receiver in couple:
                raise ValueError(f"{giver} is assigned to their partner {receiver}.")

        recipients.discard(receiver)

    if recipients:
        raise ValueError(f"Some recipients were not assigned: {recipients}")

def main():
    pairings = None

    # Keep trying until we get a valid set of pairings. Brute
    # force but whatever.
    while pairings is None:
        try:
            pairings = generate_pairings(PEOPLE, COUPLES)
        except ValueError:
            pairings = None

    verifty_pairings(pairings)

    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    for giver, receiver in pairings.items():
        (Path(OUTPUT_DIR) / f"{giver}_gift_recipient.txt").write_text(
            f"Hello, {giver}. You will be giving a gift to {receiver}.\n"
        )

if __name__ == "__main__":
    main()
