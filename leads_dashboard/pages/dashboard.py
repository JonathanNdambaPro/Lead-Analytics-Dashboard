import reflex as rx

from ..ui import area, bar, sidebar


def page_dashboard():
    return rx.hstack(sidebar.sidebar_v1(), area.areachart_v8(), bar.barchart_v5())
