import reflex as rx


def base_page(*args) -> rx.Component:
    return rx.container(*args, id="my-base-container")
