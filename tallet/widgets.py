from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal, Vertical
from rich.panel import Panel
from rich.text import Text
from .models import Board, TalletList, Card


class CardWidget(Static):
    """Widget to display a single card."""

    def __init__(self, card: Card, **kwargs) -> None:
        super().__init__(**kwargs)
        self.card = card

    def render(self) -> Panel:
        return Panel(
            Text(self.card.title, style="bold"),
            title="Card",
            border_style="green",
            expand=False
        )
    

class ListWidget(Static):
    """Widget to display a Tallet list with cards."""

    def __init__(self, tallet_list: TalletList, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tallet_list = tallet_list

    def compose(self) -> ComposeResult:
        yield Static(Text(self.tallet_list.name, style="bold cyan"))
        for card in self.tallet_list.cards:
            yield CardWidget(card)


class BoardWidget(Static):
    """Widget to display the entire board."""

    def __init__(self, board: Board, **kwargs) -> None:
        super().__init__(**kwargs)
        self.board = board

    def compose(self) -> ComposeResult:
        with Horizontal():
            for tallet_list in self.board.lists:
                yield Vertical(
                    ListWidget(tallet_list),
                    classes="list-container",
                )