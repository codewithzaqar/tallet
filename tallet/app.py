from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input
from textual.binding import Binding
from textual.message import Message
from .models import create_sample_board
from .widgets import BoardWidget, ListWidget, CardWidget, Card


class TalletTui(App):
    """Tallet CLI TUI application"""

    CSS_PATH = "styles.css"
    TITLE = "Tallet TUI v0.02"

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("left", "move_left", "Select Left List"),
        Binding("right", "move_right", "Select Right List"),
        Binding("up", "move_up", "Select Card Up"),
        Binding("down", "move_down", "Select Card Down"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield BoardWidget(create_sample_board())
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(Header).tall = True
        self.query_one(BoardWidget).select_list(0)  # Select first list by default

    def action_move_left(self) -> None:
        """Move selection to the left list."""
        board_widget = self.query_one(BoardWidget)
        new_index = max(0, board_widget.selected_list_index - 1)
        board_widget.select_list(new_index)

    def action_move_right(self) -> None:
        """Move selection to the right list."""
        board_widget = self.query_one(BoardWidget)
        new_index = min(len(board_widget.board.lists) - 1, board_widget.selected_list_index + 1)
        board_widget.select_list(new_index)

    def action_move_up(self) -> None:
        """Move selection to the card above."""
        board_widget = self.query_one(BoardWidget)
        list_widget = board_widget.query(ListWidget)[board_widget.selected_list_index]
        new_index = max(-1, list_widget.selected_card_index - 1)
        list_widget.select_card(new_index)

    def action_move_down(self) -> None:
        """Move selection to the card below."""
        board_widget = self.query_one(BoardWidget)
        list_widget = board_widget.query(ListWidget)[board_widget.selected_list_index]
        new_index = min(len(list_widget.tallet_list.cards) - 1, list_widget.selected_card_index + 1)
        list_widget.select_card(new_index)

    def on_button_pressed(self, event: Button.Pressed):
        """Handle Add Card button press."""
        if event.button.id == "add_card_button":
            list_widget = event.button.parent
            input_widget = list_widget.query_one("#new_card_input", Input)
            title = input_widget.value.strip()
            if title:
                list_widget.tallet_list.cards.append(Card(title=title))
                list_widget.refresh()
                input_widget.value = ""