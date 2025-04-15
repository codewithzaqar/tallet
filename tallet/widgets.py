from textual.app import ComposeResult
from textual.widgets import Static, Input, Button
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from rich.panel import Panel
from rich.text import Text
from .models import Board, TalletList, Card


class CardWidget(Static):
    """Widget to display a single card."""

    selected = reactive(False)

    def __init__(self, card: Card, **kwargs) -> None:
        super().__init__(**kwargs)
        self.card = card

    def render(self) -> Panel:
        border_style = "yellow" if self.selected else "green"
        return Panel(
            Text(self.card.title, style="bold"),
            title="Card",
            border_style=border_style,
            expand=False
        )
    

class ListWidget(Static):
    """Widget to display a Tallet list with cards."""

    selected = reactive(False)
    selected_card_index = reactive(-1)

    def __init__(self, tallet_list: TalletList, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tallet_list = tallet_list

    def compose(self) -> ComposeResult:
        yield Static(Text(self.tallet_list.name, style="bold cyan"))
        for i, card in enumerate(self.tallet_list.cards):
            yield CardWidget(card, id=f"card_{i}")
        yield Input(placeholder="New card title", id="new_card_input")
        yield Button("Add Card", id="add_card_button")

    def select_card(self, index: int) -> None:
        """Select a card by index."""
        if 0 <= index < len(self.tallet_list.cards):
            self.selected_card_index = index
            for i, card_widget in enumerate(self.query(CardWidget)):
                card_widget.selected = i == index


class BoardWidget(Static):
    """Widget to display the entire board."""

    selected_list_index = reactive(0)

    def __init__(self, board: Board, **kwargs) -> None:
        super().__init__(**kwargs)
        self.board = board

    def compose(self) -> ComposeResult:
        with Horizontal():
            for i, tallet_list in enumerate(self.board.lists):
                yield Vertical(
                    ListWidget(tallet_list, id=f"list_{i}"),
                    classes="list-container",
                )

    def select_list(self, index: int) -> None:
        """Select a list by index."""
        if 0 <= index < len(self.board.lists):
            self.selected_list_index = index
            for i, list_widget in enumerate(self.query(ListWidget)):
                list_widget.selected = i == index
                list_widget.select_card(-1)  # Reset card selection