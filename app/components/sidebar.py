import reflex as rx


def sidebar_item(icon: str, text: str, href: str, is_active: bool) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="w-5 h-5"),
        rx.el.span(text, class_name="font-medium"),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 rounded-lg bg-indigo-100 px-3 py-2 text-indigo-600 transition-all hover:text-indigo-600",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
        ),
    )


from app.states.product_state import ProductState
from app.states.fuel_state import FuelState


def saved_plan_item(plan: dict) -> rx.Component:
    return rx.el.a(
        rx.icon("file-text", class_name="w-5 h-5"),
        rx.el.span(plan["name"], class_name="font-medium"),
        href="#",
        on_click=lambda: FuelState.load_plan(plan),
        class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.a(
                rx.icon("zap", class_name="h-6 w-6 text-indigo-600"),
                rx.el.span("Fuel Planner", class_name="sr-only"),
                href="#",
                class_name="flex h-14 items-center justify-center rounded-lg bg-gray-100",
            ),
            rx.el.nav(
                sidebar_item("home", "Dashboard", "#", True),
                sidebar_item("file-plus-2", "New Plan", "#", False),
                sidebar_item("book-open", "Learn", "#", False),
                class_name="flex flex-col items-start gap-2 px-4 text-sm font-medium",
            ),
            rx.el.div(class_name="border-t my-4 mx-4"),
            rx.el.h3(
                "Saved Plans",
                class_name="px-4 text-xs font-semibold uppercase text-gray-400",
            ),
            rx.el.nav(
                rx.foreach(ProductState.saved_plans, saved_plan_item),
                class_name="flex flex-col items-start gap-2 px-4 text-sm font-medium mt-2",
            ),
            class_name="flex flex-col gap-2",
        ),
        rx.el.div(
            sidebar_item("settings", "Settings", "#", False),
            class_name="mt-auto flex flex-col items-start gap-2 px-4 text-sm font-medium",
        ),
        class_name="fixed inset-y-0 left-0 z-10 hidden w-64 flex-col border-r bg-white sm:flex",
    )