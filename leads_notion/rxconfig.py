import reflex as rx

config = rx.Config(
    app_name="leads_notion",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
