from dataclasses import dataclass
from typing import List as PyList


@dataclass
class Card:
    title: str
    description: str = ""


@dataclass
class TalletList:
    name: str
    cards: PyList[Card]


@dataclass
class Board:
    name: str
    lists: PyList[TalletList]


def create_sample_board() -> Board:
    """Create a simple board for v0.01"""
    return Board(
        name="Simple Board",
        lists=[
            TalletList(
                name="To Do",
                cards=[Card(title="Task 1", description="Do something")],
            ),
            TalletList(
                name="In Progress",
                cards=[Card(title="Task 2", description="Work on this")]
            ),
        ],
    )