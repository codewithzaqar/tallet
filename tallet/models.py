from dataclasses import dataclass
from typing import List as PyList
import json
import os


@dataclass
class Card:
    title: str
    description: str = ""

    def to_dict(self):
        return {"title": self.title, "description": self.description}

    @classmethod
    def from_dict(cls, data):
        return cls(title=data["title"], description=data.get("description", ""))


@dataclass
class TalletList:
    name: str
    cards: PyList[Card]

    def to_dict(self):
        return {"name": self.name, "cards": [card.to_dict() for card in self.cards]}

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], cards=[Card.from_dict(c) for c in data.get("cards", [])])


@dataclass
class Board:
    name: str
    lists: PyList[TalletList]

    def to_dict(self):
        return {"name": self.name, "lists": [lst.to_dict() for lst in self.lists]}

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], lists=[TalletList.from_dict(l) for l in data.get("lists", [])])


def create_sample_board() -> Board:
    """Create a sample board if no saved data exists."""
    return Board(
        name="Sample Board",
        lists=[
            TalletList(
                name="To Do",
                cards=[Card(title="Task 1", description="Do something")],
            ),
            TalletList(
                name="In Progress",
                cards=[Card(title="Task 2", description="Work on this")],
            ),
        ],
    )


def load_board(filename: str = "board.json") -> Board:
    """Load board from JSON or return sample board."""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            return Board.from_dict(data)
    return create_sample_board()


def save_board(board: Board, filename: str = "board.json") -> None:
    """Save board to JSON."""
    with open(filename, "w") as f:
        json.dump(board.to_dict(), f, indent=2)