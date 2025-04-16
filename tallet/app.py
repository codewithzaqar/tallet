from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input
from textual.binding import Binding
from textual.message import Message
from .models import Board, TalletList, load_board, save_board
from .widgets import BoardWidget, ListWidget, CardWidget, Button, Card


class TalletTui(App):
    """Trello-like CLI TUI application."""

    CSS_PATH = "styles.css"
    TITLE = "Trello TUI v0.03"

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("left", "move_left", "Select Left List"),
        Binding("right", "move_right", "Select Right List"),
        Binding("up", "move_up", "Select Card Up"),
        Binding("down", "move_down", "Select Card Down"),
        Binding("delete", "delete_card", "Delete Selected Card"),
    ]

    def __init__(self):
        super().__init__()
        self.board = load_board()

    def compose(self) -> ComposeResult:
        yield Header()
        yield BoardWidget(self.board)
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

    def action_delete_card(self) -> None:
        """Delete the selected card."""
        board_widget = self.query_one(BoardWidget)
        list_widget = board_widget.query(ListWidget)[board_widget.selected_list_index]
        if list_widget.selected_card_index >= 0:
            list_widget.tallet_list.cards.pop(list_widget.selected_card_index)
            list_widget.select_card(-1)  # Deselect
            list_widget.refresh()
            save_board(self.board)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        board_widget = self.query_one(BoardWidget)
        if event.button.id == "add_card_button":
            list_widget = event.button.parent
            self._add_card(list_widget)
        elif event.button.id == "add_list_button":
            input_widget = self.query_one("#new_list_input", Input)
            name = input_widget.value.strip()
            if name:
                self.board.lists.append(TalletList(name=name, cards=[]))
                board_widget.refresh()
                input_widget.value = ""
                save_board(self.board)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key for inputs."""
        board_widget = self.query_one(BoardWidget)
        if event.input.id == "new_card_input":
            list_widget = event.input.parent
            self._add_card(list_widget)
        elif event.input.id == "edit_card_input":
            list_widget = event.input.parent
            title = event.input.value.strip()
            if title and list_widget.selected_card_index >= 0:
                list_widget.tallet_list.cards[list_widget.selected_card_index].title = title
                list_widget.refresh()
                event.input.value = ""
                save_board(self.board)
        elif event.input.id == "new_list_input":
            name = event.input.value.strip()
            if name:
                self.board.lists.append(TalletList(name=name, cards=[]))
                board_widget.refresh()
                event.input.value = ""
                save_board(self.board)

    def _add_card(self, list_widget: ListWidget) -> None:
        """Add a card to the list."""
        input_widget = list_widget.query_one("#new_card_input", Input)
        title = input_widget.value.strip()
        if title:
            list_widget.tallet_list.cards.append(Card(title=title))
            list_widget.refresh()
            input_widget.value = ""
            save_board(self.board)