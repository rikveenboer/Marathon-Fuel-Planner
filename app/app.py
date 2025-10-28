import reflex as rx
import reflex_enterprise as rxe
from app.states.fuel_state import FuelState
from app.states.product_state import ProductState
from app.components.sidebar import sidebar
from app.components.input_form import input_form
from app.components.plan_display import plan_display
from app.components.product_library import product_library


def save_plan_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.el.div()),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(class_name="fixed inset-0 bg-black/50"),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Save Your Plan", class_name="text-lg font-bold"
                ),
                rx.radix.primitives.dialog.description(
                    "Give your fuel plan a name to save it for later.",
                    class_name="text-sm text-gray-500 mt-1 mb-4",
                ),
                rx.el.input(
                    placeholder="e.g., Chicago Marathon Fast Pace",
                    on_change=ProductState.set_new_plan_name,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-md",
                ),
                rx.el.div(
                    rx.radix.primitives.dialog.close(
                        rx.el.button("Cancel", variant="soft", color_scheme="gray")
                    ),
                    rx.el.button("Save Plan", on_click=ProductState.save_current_plan),
                    class_name="flex justify-end gap-4 mt-6",
                ),
                class_name="bg-white p-6 rounded-lg shadow-lg w-full max-w-md",
            ),
        ),
        open=ProductState.save_plan_modal_open,
        on_open_change=ProductState.set_save_plan_modal_open,
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            rx.el.div(
                rx.el.header(
                    rx.el.h1(
                        "Marathon Fuel Planner",
                        class_name="text-2xl font-bold tracking-tight text-gray-900",
                    ),
                    class_name="flex h-14 lg:h-[60px] items-center gap-4 border-b bg-gray-100/40 px-6 sticky top-0 z-20",
                ),
                rx.el.main(
                    input_form(),
                    rx.cond(
                        FuelState.plan_generated,
                        plan_display(),
                        rx.el.div(
                            rx.icon(
                                "clipboard-list", class_name="h-12 w-12 text-gray-400"
                            ),
                            rx.el.p(
                                "Your fuel plan will appear here.",
                                class_name="mt-4 text-sm text-gray-500",
                            ),
                            class_name="flex flex-col items-center justify-center p-12 mt-8 bg-white border-2 border-dashed border-gray-200 rounded-xl",
                        ),
                    ),
                    class_name="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-6",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            product_library(),
            class_name="grid grid-cols-[1fr_400px] h-screen overflow-hidden",
        ),
        save_plan_modal(),
        class_name="font-['Montserrat'] bg-gray-50 min-h-screen pl-64",
    )


app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)