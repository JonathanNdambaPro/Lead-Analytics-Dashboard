"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from .pages import dashboard


class State(rx.State):
    """The app state."""

    label = "This is my label"

    def handle_title_input_change(self, new_value):
        self.label = new_value


app = rx.App()
app.add_page(dashboard.page_dashboard, route="/Dashboard")
