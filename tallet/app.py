from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from .models import create_sample_board
from .widgets import BoardWidget


class TalletTui(App):
    """Tallet CLI TUI application"""

    CSS_PATH = "styles.css"
    TITLE = "Tallet TUI v0.01"

    def compose(self) -> ComposeResult:
        yield Header()
        yield BoardWidget(create_sample_board())
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(Header).tall = True