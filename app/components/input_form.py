import reflex as rx
from app.states.fuel_state import FuelState


def form_input_group(
    label: str, name: str, input_type: str, default_value: str, placeholder: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label, htmlFor=name, class_name="text-sm font-medium text-gray-700"
        ),
        rx.el.input(
            id=name,
            name=name,
            type=input_type,
            default_value=default_value,
            placeholder=placeholder,
            class_name="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        ),
        class_name="flex-1",
    )


def form_select_group(
    label: str, name: str, options: list, default_value: str
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label, htmlFor=name, class_name="text-sm font-medium text-gray-700"
        ),
        rx.el.select(
            rx.foreach(
                options, lambda option: rx.el.option(option.capitalize(), value=option)
            ),
            id=name,
            name=name,
            default_value=default_value,
            class_name="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
        ),
        class_name="flex-1",
    )


def weight_input() -> rx.Component:
    return rx.el.div(
        rx.el.label("Weight", class_name="text-sm font-medium text-gray-700"),
        rx.el.div(
            rx.el.input(
                name="weight",
                type="number",
                default_value=FuelState.weight.to_string(),
                class_name="block w-full rounded-l-lg border-gray-300 shadow-sm focus:z-10 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm",
            ),
            rx.el.button(
                "kg",
                on_click=lambda: FuelState.set_weight_unit("kg"),
                class_name=rx.cond(
                    FuelState.weight_unit == "kg",
                    "relative -ml-px inline-flex items-center space-x-2 rounded-none border border-gray-300 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700 hover:bg-indigo-100 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500",
                    "relative -ml-px inline-flex items-center space-x-2 rounded-none border border-gray-300 bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500",
                ),
            ),
            rx.el.button(
                "lbs",
                on_click=lambda: FuelState.set_weight_unit("lbs"),
                class_name=rx.cond(
                    FuelState.weight_unit == "lbs",
                    "relative -ml-px inline-flex items-center space-x-2 rounded-r-lg border border-gray-300 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700 hover:bg-indigo-100 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500",
                    "relative -ml-px inline-flex items-center space-x-2 rounded-r-lg border border-gray-300 bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500",
                ),
            ),
            class_name="mt-1 flex rounded-lg shadow-sm",
        ),
        class_name="flex-1",
    )


def input_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Create Your Fuel Plan", class_name="text-xl font-bold text-gray-900 mb-4"
        ),
        rx.el.form(
            rx.el.div(
                weight_input(),
                rx.el.div(
                    rx.el.label(
                        "Target Time", class_name="text-sm font-medium text-gray-700"
                    ),
                    rx.el.div(
                        form_input_group(
                            "",
                            "target_hours",
                            "number",
                            FuelState.target_hours.to_string(),
                        ),
                        rx.el.span("hr", class_name="self-end pb-2 text-gray-500"),
                        form_input_group(
                            "",
                            "target_minutes",
                            "number",
                            FuelState.target_minutes.to_string(),
                        ),
                        rx.el.span("min", class_name="self-end pb-2 text-gray-500"),
                        class_name="flex items-center gap-2",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex flex-col md:flex-row gap-6 mb-6",
            ),
            rx.el.div(
                form_select_group(
                    "Race Distance",
                    "race_distance",
                    ["marathon", "half"],
                    FuelState.race_distance,
                ),
                form_select_group(
                    "Experience Level",
                    "experience",
                    ["beginner", "intermediate", "advanced"],
                    FuelState.experience,
                ),
                class_name="flex flex-col md:flex-row gap-6 mb-8",
            ),
            rx.el.button(
                rx.icon("zap", class_name="mr-2 h-5 w-5"),
                "Generate Plan",
                type="submit",
                class_name="w-full inline-flex justify-center items-center rounded-lg border border-transparent bg-indigo-600 px-6 py-3 text-base font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-transform hover:scale-[1.02]",
            ),
            on_submit=FuelState.generate_plan,
            reset_on_submit=False,
        ),
        class_name="bg-white p-8 rounded-xl shadow-sm border border-gray-200",
    )