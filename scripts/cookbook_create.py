from openai import OpenAI
import os
import json
from models.recipe import Recipe
import pandas as pd

def recipe_to_row(recipe: Recipe) -> pd.DataFrame:
    data = {
        "recipe_title": recipe.recipe_title,
        "servings": recipe.servings,
        "meal": recipe.meal,
        "calories": recipe.calories,
        "carbs": recipe.carbs,
        "protein": recipe.protein,
        "fat": recipe.fat,
        "ingredients": "; ".join([f"{ing.quantity} {ing.name}" for ing in recipe.ingredients]),
        "instructions": " | ".join([instr.step for instr in recipe.instructions]),
    }
    return pd.DataFrame([data])

def cookbook_create(pdf_name: str) -> pd.DataFrame:
    pdf_path = f"cookbooks/pdfs/{pdf_name}"
    name = pdf_name.split(".")[0]
    text_dir = f"cookbooks/txt/{name}"

    rows = []
    i = 1
    for filename in os.listdir(text_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(text_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                recipe_text = f.read()

            prompt = f"""
            Extract the following structured fields from the recipe below and return them as JSON:
            - recipe_title: string
            - ingredients: list of objects with 'name' and 'quantity'
            - instructions: list of steps with numbers, ex. 1. 2. etc.
            - servings: integer
            - calories: integer (per serving)
            - carbs: integer (grams per serving)
            - protein: integer (grams per serving)
            - fat: integer (grams per serving)
            - meal: one of ['breakfast', 'lunch', 'dinner']

            Here is the recipe text:

            {recipe_text}
            """

            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

            response = client.responses.create(
                model="gpt-4.1-nano",
                instructions="You are a helpful assistant that extracts structured data from recipe text.",
                input=prompt,
                temperature=0
            )

            response_text = response.output_text

            try:
                recipe_data = json.loads(response_text)
                recipe = Recipe(**recipe_data)
                df_row = recipe_to_row(recipe)
                rows.append(df_row)
                print(f"Recipe {i} completed successfully.")
                i += 1
            except Exception as e:
                print(f"Error parsing {filename}:", e)

    columns = [
    "recipe_title", "servings", "meal", 
    "calories", "carbs", "protein", "fat",
    "ingredients", "instructions"
    ]

    return pd.concat(rows, ignore_index=True)[columns] if rows else pd.DataFrame(columns=columns)

