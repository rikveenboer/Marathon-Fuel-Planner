import reflex as rx
from typing import TypedDict, Literal, cast
from app.states.product_state import Product, SavedPlan
import asyncio
from app.utils.pdf_utils import generate_fuel_plan_pdf


class FuelIntake(TypedDict):
    time_minutes: int
    fuel_type: str
    amount: str
    carbs: int
    calories: int
    sodium: int
    cost: float
    product_id: str | None


class FormattedFuelIntake(FuelIntake):
    time_str: str
    calories: int
    sodium: int
    cost: float


class FuelState(rx.State):
    weight: float = 70.0
    weight_unit: Literal["kg", "lbs"] = "kg"
    target_hours: int = 4
    target_minutes: int = 0
    race_distance: Literal["marathon", "half"] = "marathon"
    experience: Literal["beginner", "intermediate", "advanced"] = "intermediate"
    plan_generated: bool = False
    fuel_plan: list[FuelIntake] = []

    @rx.var
    def weight_in_kg(self) -> float:
        return self.weight * 0.453592 if self.weight_unit == "lbs" else self.weight

    @rx.var
    def total_race_time_minutes(self) -> int:
        return self.target_hours * 60 + self.target_minutes

    @rx.var
    def carb_rate_per_hour(self) -> int:
        base_rate = 0
        if self.experience == "beginner":
            base_rate = 45
        elif self.experience == "intermediate":
            base_rate = 60
        else:
            base_rate = 75
        return base_rate + 15 if self.race_distance == "marathon" else base_rate

    @rx.var
    def total_carbs_in_plan(self) -> int:
        return sum((item.get("carbs", 0) for item in self.fuel_plan))

    @rx.var
    def total_calories_in_plan(self) -> int:
        return sum((item.get("calories", 0) for item in self.fuel_plan))

    @rx.var
    def total_sodium_in_plan(self) -> int:
        return sum((item.get("sodium", 0) for item in self.fuel_plan))

    @rx.var
    def total_cost_in_plan(self) -> float:
        return sum((item.get("cost", 0.0) for item in self.fuel_plan))

    @rx.var
    def hydration_rate_ml_per_hour(self) -> int:
        base_hydration = 500
        if self.experience == "intermediate":
            base_hydration = 650
        elif self.experience == "advanced":
            base_hydration = 800
        return base_hydration

    @rx.var
    def total_hydration_needed_ml(self) -> int:
        return int(self.hydration_rate_ml_per_hour / 60 * self.total_race_time_minutes)

    @rx.var
    def formatted_fuel_plan(self) -> list[FormattedFuelIntake]:
        formatted_plan = []
        for item in self.fuel_plan:
            if item["time_minutes"] < 0:
                time_str = f"{abs(item['time_minutes'])} mins before start"
            else:
                hours = item["time_minutes"] // 60
                minutes = item["time_minutes"] % 60
                time_str = f"{hours:02d}:{minutes:02d}"
            formatted_item = FormattedFuelIntake(
                time_minutes=item["time_minutes"],
                fuel_type=item["fuel_type"],
                amount=item["amount"],
                carbs=item["carbs"],
                calories=item["calories"],
                sodium=item["sodium"],
                cost=item["cost"],
                time_str=time_str,
                product_id=item["product_id"],
            )
            formatted_plan.append(cast(FormattedFuelIntake, formatted_item))
        return formatted_plan

    @rx.event
    def generate_plan(self, form_data: dict):
        self.weight = float(form_data["weight"])
        self.target_hours = int(form_data["target_hours"])
        self.target_minutes = int(form_data["target_minutes"])
        self.experience = form_data["experience"]
        self.race_distance = form_data["race_distance"]
        self.fuel_plan = []
        self.fuel_plan.append(
            FuelIntake(
                time_minutes=-15,
                fuel_type="Gel",
                amount="1 Gel",
                carbs=25,
                calories=100,
                sodium=50,
                cost=1.5,
                product_id=None,
            )
        )
        gel_interval = 45 if self.experience == "beginner" else 35
        num_gels = (self.total_race_time_minutes - 30) // gel_interval
        for i in range(1, num_gels + 1):
            intake_time = i * gel_interval
            if intake_time < self.total_race_time_minutes:
                self.fuel_plan.append(
                    FuelIntake(
                        time_minutes=intake_time,
                        fuel_type="Gel",
                        amount="1 Gel",
                        carbs=25,
                        calories=100,
                        sodium=50,
                        cost=1.5,
                        product_id=None,
                    )
                )
        water_interval = 20
        water_amount_per_intake = round(
            self.hydration_rate_ml_per_hour / 60 * water_interval
        )
        num_water_stops = self.total_race_time_minutes // water_interval
        for i in range(1, num_water_stops + 1):
            intake_time = i * water_interval
            if intake_time < self.total_race_time_minutes:
                self.fuel_plan.append(
                    FuelIntake(
                        time_minutes=intake_time,
                        fuel_type="Water",
                        amount=f"{water_amount_per_intake} ml",
                        carbs=0,
                        calories=0,
                        sodium=0,
                        cost=0.0,
                        product_id=None,
                    )
                )
        self.fuel_plan.sort(key=lambda x: x["time_minutes"])
        self.plan_generated = True

    @rx.event
    def set_weight_unit(self, unit: Literal["kg", "lbs"]):
        self.weight_unit = unit

    @rx.event
    def update_fuel_item(self, payload: dict):
        time_minutes = payload["time_minutes"]
        product = cast(Product, payload["product"])
        for i, item in enumerate(self.fuel_plan):
            if item["time_minutes"] == time_minutes:
                self.fuel_plan[i] = FuelIntake(
                    time_minutes=item["time_minutes"],
                    fuel_type=product["category"],
                    amount=product["name"],
                    carbs=product["carbs"],
                    calories=product["calories"],
                    sodium=product["sodium"],
                    cost=product["cost"],
                    product_id=product["id"],
                )
                break
        self.fuel_plan = self.fuel_plan

    @rx.event
    async def save_current_plan(self):
        from app.states.product_state import ProductState

        product_state = await self.get_state(ProductState)
        if not product_state.new_plan_name:
            yield rx.toast("Please enter a name for your plan.", duration=3000)
            return
        new_saved_plan = SavedPlan(
            name=product_state.new_plan_name, plan=self.fuel_plan
        )
        product_state.saved_plans.append(new_saved_plan)
        product_state.saved_plans = product_state.saved_plans
        yield product_state.close_save_plan_modal()
        yield rx.toast(f"Plan '{product_state.new_plan_name}' saved!", duration=3000)

    @rx.event
    def load_plan(self, plan_to_load: SavedPlan):
        self.fuel_plan = plan_to_load["plan"]
        self.plan_generated = True

    @rx.event
    async def export_plan_as_pdf(self) -> rx.event.EventSpec:
        runner_info = {
            "target_time": f"{self.target_hours}hr {self.target_minutes}min",
            "distance": self.race_distance.capitalize(),
            "weight": f"{self.weight:.1f}{self.weight_unit}",
        }
        loop = asyncio.get_running_loop()
        pdf_bytes = await loop.run_in_executor(
            None, generate_fuel_plan_pdf, self.formatted_fuel_plan, runner_info
        )
        return rx.download(data=pdf_bytes, filename=f"marathon-fuel-plan.pdf")