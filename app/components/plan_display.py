import reflex as rx
from app.states.fuel_state import FuelState
import reflex_enterprise as rxe


def timeline_icon(fuel_type: str) -> rx.Component:
    return rx.el.span(
        rx.icon(
            rx.match(
                fuel_type,
                ("Gel", "droplet"),
                ("Water", "glass-water"),
                ("Chew", "square-activity"),
                ("Drink", "cup-soda"),
                ("Real Food", "banana"),
                "zap",
            ),
            class_name="h-5 w-5 text-white",
        ),
        class_name=rx.match(
            fuel_type,
            (
                "Gel",
                "z-10 flex h-10 w-10 items-center justify-center rounded-full bg-yellow-500 ring-4 ring-white",
            ),
            (
                "Water",
                "z-10 flex h-10 w-10 items-center justify-center rounded-full bg-blue-500 ring-4 ring-white",
            ),
            (
                "Chew",
                "z-10 flex h-10 w-10 items-center justify-center rounded-full bg-pink-500 ring-4 ring-white",
            ),
            (
                "Drink",
                "z-10 flex h-10 w-10 items-center justify-center rounded-full bg-green-500 ring-4 ring-white",
            ),
            (
                "Real Food",
                "z-10 flex h-10 w-10 items-center justify-center rounded-full bg-orange-500 ring-4 ring-white",
            ),
            "z-10 flex h-10 w-10 items-center justify-center rounded-full bg-indigo-500 ring-4 ring-white",
        ),
    )


@rx.memo
def timeline_item(item: dict, index: int) -> rx.Component:
    drop_params = rxe.dnd.DropTarget.collected_params
    is_over = drop_params.is_over
    return rxe.dnd.drop_target(
        rx.el.li(
            rx.cond(
                index > 0,
                rx.el.div(class_name="absolute -left-2 mt-2 h-full w-0.5 bg-gray-200"),
                None,
            ),
            timeline_icon(item["fuel_type"]),
            rx.el.div(
                rx.el.p(item["amount"], class_name="font-semibold text-gray-800"),
                rx.el.div(
                    rx.el.span(
                        f"{item['carbs']}g c", class_name="text-sm text-gray-500"
                    ),
                    rx.el.span(
                        f" / {item['calories']} k", class_name="text-sm text-gray-500"
                    ),
                    rx.el.span(
                        f" / {item['sodium']}mg s", class_name="text-sm text-gray-500"
                    ),
                    class_name="flex gap-1",
                ),
                class_name="ml-4",
            ),
            rx.el.span(
                item["time_str"], class_name="ml-auto text-sm font-medium text-gray-600"
            ),
            class_name=rx.cond(
                is_over,
                "relative flex items-center space-x-3 p-2 rounded-lg bg-indigo-50 ring-2 ring-indigo-300 transition-all",
                "relative flex items-center space-x-3 p-2 rounded-lg bg-transparent transition-all",
            ),
        ),
        accept=["product"],
        on_drop=lambda dropped_product: FuelState.update_fuel_item(
            {"time_minutes": item["time_minutes"], "product": dropped_product}
        ),
    )


def summary_card(icon: str, title: str, value: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-6 w-6 {color}"),
            class_name="flex items-center justify-center h-12 w-12 rounded-lg bg-white shadow-sm",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-xl font-bold text-gray-900"),
            class_name="ml-4",
        ),
        class_name="flex items-center p-4 bg-gray-50 rounded-xl",
    )


from app.states.product_state import ProductState


def plan_display() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Your Fuel Plan", class_name="text-xl font-bold text-gray-900"),
            rx.el.p(
                f"For a {FuelState.race_distance} at {FuelState.target_hours}hr {FuelState.target_minutes}min",
                class_name="text-sm text-gray-500",
            ),
            rx.el.div(
                rx.el.button(
                    "Export PDF",
                    on_click=FuelState.export_plan_as_pdf,
                    class_name="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2",
                ),
                rx.el.button(
                    "Save Plan",
                    on_click=ProductState.open_save_plan_modal,
                    class_name="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2",
                ),
                class_name="absolute top-8 right-8 flex gap-2",
            ),
            class_name="mb-6 relative",
        ),
        rx.el.div(
            summary_card(
                "flame",
                "Total Carbs",
                f"{FuelState.total_carbs_in_plan} g",
                "text-orange-500",
            ),
            summary_card(
                "zap",
                "Total Calories",
                f"{FuelState.total_calories_in_plan} kCal",
                "text-green-500",
            ),
            summary_card(
                "gem",
                "Total Sodium",
                f"{FuelState.total_sodium_in_plan} mg",
                "text-blue-500",
            ),
            summary_card(
                "dollar-sign",
                "Est. Cost",
                f"${FuelState.total_cost_in_plan:.2f}",
                "text-purple-500",
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8",
        ),
        rx.el.h3(
            "Race Timeline", class_name="text-lg font-semibold text-gray-800 mb-4"
        ),
        rx.el.ol(
            rx.foreach(
                FuelState.formatted_fuel_plan,
                lambda item, index: timeline_item(
                    key=item["time_minutes"], item=item, index=index
                ),
            ),
            class_name="space-y-2",
        ),
        class_name="bg-white p-8 rounded-xl shadow-sm border border-gray-200 mt-8",
    )