import reflex as rx
from reflex import Color
from reflex.experimental import ClientStateVar


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Dashboard", "layout-dashboard", "/#"),
        sidebar_item("Projects", "square-library", "/#"),
        sidebar_item("Analytics", "bar-chart-4", "/#"),
        sidebar_item("Messages", "mail", "/#"),
        spacing="1",
        width="100%",
    )


def sidebar_bottom_profile() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("Reflex", size="7", weight="bold"),
                    align="center",
                    justify="start",
                    padding_x="0.5rem",
                    width="100%",
                ),
                sidebar_items(),
                rx.spacer(),
                rx.vstack(
                    rx.vstack(
                        sidebar_item("Settings", "settings", "/#"),
                        sidebar_item("Log out", "log-out", "/#"),
                        spacing="1",
                        width="100%",
                    ),
                    rx.divider(),
                    rx.hstack(
                        rx.icon_button(
                            rx.icon("user"),
                            size="3",
                            radius="full",
                        ),
                        rx.vstack(
                            rx.box(
                                rx.text(
                                    "My account",
                                    size="3",
                                    weight="bold",
                                ),
                                rx.text(
                                    "user@reflex.dev",
                                    size="2",
                                    weight="medium",
                                ),
                                width="100%",
                            ),
                            spacing="0",
                            align="start",
                            justify="start",
                            width="100%",
                        ),
                        padding_x="0.5rem",
                        align="center",
                        justify="start",
                        width="100%",
                    ),
                    width="100%",
                    spacing="5",
                ),
                spacing="5",
                # position="fixed",
                # left="0px",
                # top="0px",
                # z_index="5",
                padding_x="1em",
                padding_y="1.5em",
                bg=rx.color("accent", 3),
                align="start",
                # height="100%",
                height="650px",
                width="16em",
            ),
        ),
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(rx.icon("align-justify", size=30)),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(rx.icon("x", size=30)),
                                width="100%",
                            ),
                            sidebar_items(),
                            rx.spacer(),
                            rx.vstack(
                                rx.vstack(
                                    sidebar_item(
                                        "Settings",
                                        "settings",
                                        "/#",
                                    ),
                                    sidebar_item(
                                        "Log out",
                                        "log-out",
                                        "/#",
                                    ),
                                    width="100%",
                                    spacing="1",
                                ),
                                rx.divider(margin="0"),
                                rx.hstack(
                                    rx.icon_button(
                                        rx.icon("user"),
                                        size="3",
                                        radius="full",
                                    ),
                                    rx.vstack(
                                        rx.box(
                                            rx.text(
                                                "My account",
                                                size="3",
                                                weight="bold",
                                            ),
                                            rx.text(
                                                "user@reflex.dev",
                                                size="2",
                                                weight="medium",
                                            ),
                                            width="100%",
                                        ),
                                        spacing="0",
                                        justify="start",
                                        width="100%",
                                    ),
                                    padding_x="0.5rem",
                                    align="center",
                                    justify="start",
                                    width="100%",
                                ),
                                width="100%",
                                spacing="5",
                            ),
                            spacing="5",
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="1.5em",
                        bg=rx.color("accent", 2),
                    ),
                    width="100%",
                ),
                direction="left",
            ),
            padding="1em",
        ),
    )


ACTIVE_ITEM = ClientStateVar.create("active_item", "")

SIDEBAR_CONTENT_ONE = [
    {"name": "Authentication"},
    {"name": "SMS Template"},
    {"name": "Email Templates"},
]

SIDEBAR_CONTENT_TWO = [
    {"name": "Sessions"},
    {"name": "JWT templates"},
    {"name": "Webhooks"},
    {"name": "Domains"},
    {"name": "Integrations"},
    {"name": "API Keys"},
]

SIDEBAR_CONTENT_THREE = [
    {"name": "Dashboard"},
    {"name": "Analytics"},
    {"name": "Users"},
    {"name": "Settings"},
    {"name": "Notifications"},
    {"name": "Logs"},
    {"name": "Roles & Permissions"},
    {"name": "Data Export"},
    {"name": "Security"},
    {"name": "Billing"},
    {"name": "Activity Feed"},
]


def create_divider():
    """Create a consistent divider."""
    return rx.divider(border_bottom=f"0.81px solid {rx.color('gray', 4)}", bg="transparent")


def create_sidebar_menu_items(routes: list[dict[str, str | Color]]):
    """Create menu items from routes."""

    def item(data):
        item_name = data["name"]
        return rx.hstack(
            rx.link(
                rx.text(
                    item_name,
                    _hover={"color": rx.color("slate", 12)},
                    color=rx.cond(
                        ACTIVE_ITEM.value == item_name,
                        rx.color("slate", 12),
                        rx.color("slate", 11),
                    ),
                    size="2",
                    font_weight=rx.cond(ACTIVE_ITEM.value == item_name, "semibold", "normal"),
                ),
                href=f"#{item_name}",
                text_decoration="none",
                on_click=ACTIVE_ITEM.set_value(item_name),
                width="100%",
                padding_left="10px",
            ),
            spacing="0",
            align_items="center",
            width="100%",
            border_left=rx.cond(
                ACTIVE_ITEM.value == item_name,
                f"1px solid {rx.color('blue', 10)}",
                f"0.81px solid {rx.color('gray', 4)}",
            ),
            height="25px",
        )

    return rx.vstack(rx.foreach(routes, item), spacing="0", width="100%")


def side_bar_wrapper(title: str, component: rx.Component):
    """Create a sidebar section."""

    return rx.vstack(
        rx.text(title, size="1", color=rx.color("slate", 12), weight="bold"),
        component,
        padding="1em",
    )


def sidebar_v1():
    content = rx.box(
        ACTIVE_ITEM,
        side_bar_wrapper("General", create_sidebar_menu_items(SIDEBAR_CONTENT_ONE)),
        create_divider(),
        side_bar_wrapper("Developers", create_sidebar_menu_items(SIDEBAR_CONTENT_TWO)),
        create_divider(),
        side_bar_wrapper("Personal", create_sidebar_menu_items(SIDEBAR_CONTENT_THREE)),
    )

    return rx.scroll_area(
        content,
        height="100vh",
        width="100%",
        max_width="240px",
    )
