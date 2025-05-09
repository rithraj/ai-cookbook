from pydantic import BaseModel, Field, model_validator
from typing import List, Literal
import re


class Ingredient(BaseModel):
    name: str = Field(..., description="Name of the ingredient", example="Flour")
    quantity: str = Field(..., description="Amount required (with units)", example="2 cups")

    @model_validator(mode="before")
    @classmethod
    def accept_string_or_dict(cls, value):
        if isinstance(value, str):

            match = re.match(r"^(\d+[^a-zA-Z]*)\s+(.*)", value.strip())
            if match:
                return {"quantity": match.group(1).strip(), "name": match.group(2).strip()}
            else:
                return {"quantity": "unknown", "name": value.strip()}
        if isinstance(value, dict):
            return value
        raise ValueError("Ingredient must be a string or a dictionary with 'name' and 'quantity'.")


class Instruction(BaseModel):
    step: str = Field(..., description="Cooking step")

    @model_validator(mode="before")
    @classmethod
    def accept_string_or_dict(cls, value):
        if isinstance(value, str):
            return {"step": value}
        if isinstance(value, dict) and "step" in value:
            return value
        raise ValueError("Instruction must be a string or a dictionary with 'step'.")


class Recipe(BaseModel):
    recipe_title: str = Field(..., description="Title of the recipe")
    ingredients: List[Ingredient] = Field(..., description="List of ingredients with quantities")
    instructions: List[Instruction] = Field(..., description="Step-by-step instructions")
    servings: int = Field(..., description="Number of servings")
    calories: int = Field(..., description="Calories per serving")
    carbs: int = Field(..., description="Carbohydrates per serving (g)")
    protein: int = Field(..., description="Protein per serving (g)")
    fat: int = Field(..., description="Fat per serving (g)")
    meal: Literal["breakfast", "lunch", "dinner"] = Field(..., description="Meal type")
