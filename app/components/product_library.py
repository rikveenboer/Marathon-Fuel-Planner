import reflex as rx
from app.states.product_state import ProductState
from app.components.product_card import product_card


def category_button(category: str) -> rx.Component:
    is_active = ProductState.filter_category == category
    return rx.el.button(
        category,
        on_click=lambda: ProductState.set_filter_category(category),
        class_name=rx.cond(
            is_active,
            "px-3 py-1 text-sm font-medium text-white bg-indigo-600 rounded-full",
            "px-3 py-1 text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-full",
        ),
    )


def product_library() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Fuel Library", class_name="text-lg font-bold text-gray-900"),
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                ),
                rx.el.input(
                    placeholder="Search products...",
                    on_change=ProductState.set_search_query,
                    class_name="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.foreach(
                    ["All", "Gel", "Chew", "Drink", "Real Food"], category_button
                ),
                class_name="flex flex-wrap gap-2 pt-4",
            ),
            class_name="p-4 border-b border-gray-200 sticky top-0 bg-gray-50/80 backdrop-blur-sm z-10",
        ),
        rx.el.div(
            rx.foreach(
                ProductState.filtered_products,
                lambda p: product_card(key=p["id"], product=p),
            ),
            class_name="flex flex-col gap-3 p-4 overflow-y-auto",
        ),
        class_name="flex flex-col h-full bg-gray-50 border-l border-gray-200",
    )