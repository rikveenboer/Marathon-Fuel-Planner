import reflex as rx
from typing import TypedDict, Literal


class Product(TypedDict):
    id: str
    name: str
    category: Literal["Gel", "Chew", "Drink", "Real Food"]
    carbs: int
    calories: int
    sodium: int
    cost: float


class SavedPlan(TypedDict):
    name: str
    plan: list[dict]


class ProductState(rx.State):
    products: list[Product] = [
        Product(
            id="prod_01",
            name="GU Energy Gel",
            category="Gel",
            carbs=23,
            calories=100,
            sodium=55,
            cost=1.5,
        ),
        Product(
            id="prod_02",
            name="Maurten Gel 100",
            category="Gel",
            carbs=25,
            calories=100,
            sodium=35,
            cost=3.9,
        ),
        Product(
            id="prod_03",
            name="Clif Shot Bloks",
            category="Chew",
            carbs=24,
            calories=100,
            sodium=50,
            cost=2.2,
        ),
        Product(
            id="prod_04",
            name="Skratch Labs Chews",
            category="Chew",
            carbs=19,
            calories=80,
            sodium=40,
            cost=2.5,
        ),
        Product(
            id="prod_05",
            name="Gatorade Endurance",
            category="Drink",
            carbs=22,
            calories=90,
            sodium=310,
            cost=1.8,
        ),
        Product(
            id="prod_06",
            name="Tailwind Nutrition",
            category="Drink",
            carbs=25,
            calories=100,
            sodium=303,
            cost=2.0,
        ),
        Product(
            id="prod_07",
            name="Banana",
            category="Real Food",
            carbs=27,
            calories=105,
            sodium=1,
            cost=0.3,
        ),
        Product(
            id="prod_08",
            name="Pretzels (1oz)",
            category="Real Food",
            carbs=23,
            calories=110,
            sodium=322,
            cost=0.5,
        ),
    ]
    search_query: str = ""
    filter_category: str = "All"
    saved_plans: list[SavedPlan] = []
    save_plan_modal_open: bool = False
    new_plan_name: str = ""

    @rx.var
    def filtered_products(self) -> list[Product]:
        products = self.products
        if self.filter_category != "All":
            products = [p for p in products if p["category"] == self.filter_category]
        if self.search_query:
            products = [
                p for p in products if self.search_query.lower() in p["name"].lower()
            ]
        return products

    @rx.event
    def set_filter_category(self, category: str):
        self.filter_category = category

    @rx.event
    def open_save_plan_modal(self):
        self.save_plan_modal_open = True

    @rx.event
    def close_save_plan_modal(self):
        self.save_plan_modal_open = False
        self.new_plan_name = ""