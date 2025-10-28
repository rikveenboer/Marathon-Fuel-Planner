import reflex as rx
import reflex_enterprise as rxe
from app.states.product_state import Product


@rx.memo
def product_card(product: Product) -> rx.Component:
    return rxe.dnd.draggable(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    product["name"], class_name="font-semibold text-gray-800 text-sm"
                ),
                rx.el.span(product["category"], class_name="text-xs text-gray-500"),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        f"{product['carbs']}g",
                        class_name="font-bold text-indigo-600 text-sm",
                    ),
                    rx.el.p("carbs", class_name="text-xs text-gray-500"),
                    class_name="text-center",
                ),
                rx.el.div(
                    rx.el.p(
                        f"${product['cost']:.2f}",
                        class_name="font-bold text-gray-700 text-sm",
                    ),
                    rx.el.p("cost", class_name="text-xs text-gray-500"),
                    class_name="text-center",
                ),
                class_name="flex gap-4",
            ),
            class_name="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200 shadow-sm cursor-grab active:cursor-grabbing",
        ),
        item=product,
        type="product",
    )