from scripts.cookbook_create import cookbook_create
from scripts.cookbook_parse import parse_cookbook
import pandas as pd

def run_parse(pdf_name):
    try:
        parse_cookbook(pdf_name)
        print("Cookbook parsed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

def run_create(pdf_name):
    try:
        df = cookbook_create(pdf_name)
        print("Cookbook created successfully!")
        print(df.head())  # Display the first few rows of the DataFrame
        df.to_csv(f"db/{pdf_name.split('.')[0]}.csv", index=False)
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    pdf_name = "TheFeluCookbook_V2.0.pdf"  # Replace with your actual PDF name
    # MAKE SURE THAT PDF IS IN THE COOKBOOKS/PDFS DIRECTORY
    run_parse(pdf_name)
    run_create(pdf_name)
