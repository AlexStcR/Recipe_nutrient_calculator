# Recipe Nutrients Calculator

#### Description:
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

A command-line tool to calculate the nutritional content of recipes using the USDA Food Database.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [File Structure](#file-structure)
- [Design Choices](#design-choices)
- [How to Use](#how-to-use)


---

## Project Overview
This project simplifies nutrition tracking by allowing users to input ingredients and quantities, then calculates total calories, protein, carbohydrates, and fat. It uses a cleaned USDA food dataset to ensure accuracy and leverages fuzzy string matching to handle typos or variations in food names (e.g., "tomatos" vs. "tomato").

---

## Features
- **Fuzzy Matching**: Matches user inputs to the closest food name in the database with 80% confidence.
- **Dynamic Nutrient Scaling**: Converts nutrient values to user-specified gram amounts.
- **Error Handling**: Gracefully manages invalid inputs and missing matches.
- **User-Friendly CLI**: Includes emojis and clear prompts for an engaging experience.


---

## Dependencies

* [Python](https://www.python.org/) (3.6 or later)
* [pandas](https://pandas.pydata.org/)
* [rapidfuzz](https://github.com/rapidfuzz/RapidFuzz)
* [emoji](https://pypi.org/project/emoji/)

---

## File Structure
1. **`project.py`**
   The core script containing three key functions:
   - **`load_message_user()`**: Displays a welcome message with emojis.
   - **`load_food_database()`**:
     - Loads `cleaned_usda_foods.csv` (preprocessed USDA dataset).
     - Standardizes food names to lowercase and fills missing values with `0`.
   - **`nutrition_calculator()`**:
     - Guides users to input ingredients and amounts.
     - Uses `rapidfuzz` to find the closest food match.
     - Calculates and displays total nutrients.

2. **`cleaned_usda_foods.csv`**
   A cleaned USDA dataset containing:
   - `description`: Standardized food names (e.g., "banana").
   - `calories`, `protein`, `carbs`, `fat`: Nutrients per 100g.

---
## Data preparation

## Step-by-Step Process of Cleaning USDA Food Data for Nutritional Analysis

As a data professional, cleaning messy datasets is a critical step before analysis. Here’s a breakdown of how I cleaned the USDA food database to create a reliable dataset for nutritional insights:

---

### 1. **Loading & Initial Inspection**
**Datasets Involved**:
- `foods.csv` (food metadata)
- `nutrient.csv` (nutrient definitions)
- `food_nutrient.csv` (nutrient amounts per food)
- `food_portion.csv` (serving sizes)

**First Checks**:
- Printed column names and sample rows to understand structure.
- Identified inconsistencies (e.g., mixed data types in `food_nutrient.csv`).

---

### 2. **Cleaning Food Metadata**
- **Standardized Descriptions**:
  - Converted food names to lowercase and trimmed whitespace.
- **Removed Test Entries**:
  - Filtered out rows containing "test" in descriptions.
- **Deduplication**:
  - Dropped duplicates using `fdc_id` (unique food identifier).
- **Handling Missing Values**:
  - Removed rows with *all* NaN values.
  - Retained partial NaNs (e.g., `food_category_id`) where acceptable.

---

### 3. **Standardizing Serving Sizes**
- **Focused on Grams**:
  - Filtered `food_portion` data to use only gram-based measurements (`measure_unit_id = 1`).
- **Default Serving Size**:
  - Assigned **100g** as the default for foods lacking portion data.

---

### 4. **Identifying Key Nutrients**
- **Target Nutrients**: Energy (calories), protein, carbohydrates, and fat.
- **Mapped Nutrient IDs**:
  - Used exact names from `nutrient.csv` (e.g., `Energy`, `Total lipid (fat)`).

---

### 5. **Merging & Reshaping Data**
- **Linked Nutrients to Foods**:
  - Joined `food_nutrient` with `nutrient` to attach nutrient names to IDs.
- **Pivoted to Wide Format**:
  - Transformed data into one row per food (`fdc_id`) with nutrient columns.

---

### 6. **Final Adjustments**
- **Calculated per 100g Values**:
  - Formula: `(nutrient value) * (100 / serving size)`.
- **Renamed Columns**:
  - Simplified headers (e.g., `Energy` → `calories`).
- **Addressed Duplicates**:
  - Retained unique entries using `fdc_id` even if names overlapped (e.g., "banana").

---

### 7. **Output**
- Saved cleaned dataset as **`cleaned_usda_foods.csv`** with columns:
  - `description`, `calories`, `protein`, `carbs`, `fat`.

---

-
## Design Choices
1. **Fuzzy Matching with `rapidfuzz`**
   - **Why?** Users often mistype food names (e.g., "brocolli" vs. "broccoli").
   - **Implementation**: `extractOne` with `WRatio` scorer ensures flexible matching while filtering low-confidence matches (`score_cutoff=80`).

2. **Data Preprocessing**
   - **Lowercase Conversion**: Ensures case-insensitive matching (e.g., "Apple" vs. "apple").
   - **NaN Handling**: Missing values replaced with `0` to avoid calculation errors.

3. **Nutrient Scaling**
   - **Formula**: `(nutrient_per_100g / 100) * user_grams` allows dynamic adjustments.
   - **Default Serving Size**: 100g simplifies calculations if no portion data exists.

4. **User Experience**
   - **Emojis**: Added visual cues (✅, ❌) to make the CLI more engaging.
   - **Input Validation**: Prevents crashes from non-numeric inputs.

---
## Code Explanation

This Python script is a recipe nutrition calculator. It takes user input for food items and their amounts, then calculates the total calories, protein, carbs, and fat. Here's a breakdown:

**1. Imports:**

* `pandas`: Used for working with structured data in a DataFrame (like a table). It's excellent for reading and manipulating the food database.
* `rapidfuzz.fuzz` and `rapidfuzz.process.extractOne`: These are for "fuzzy matching." This means the program can find the closest match to what the user types, even if there are spelling errors or slight variations. `extractOne` finds the single best match. `fuzz.WRatio` is a specific algorithm within `rapidfuzz` that gives a similarity score.
* `emoji`: Used to include emojis in the program's output, making it more user-friendly.

**2. `load_message_user()` Function:**

* This function simply returns a formatted string that serves as a welcome message to the user.
* It includes emojis to make the greeting more engaging.

**3. `load_food_database()` Function:**

* Loads the food data from a CSV file named "cleaned_usda_foods.csv" into a pandas DataFrame.
* **Data Cleaning:**
    * Converts the 'description' column (which likely contains food names) to lowercase using `.str.lower()`. This ensures that the matching isn't case-sensitive (e.g., "apple" will match "Apple").
    * Fills any missing values (NaNs) in the DataFrame with 0 using `.fillna(0, inplace=True)`. This prevents errors if some food items don't have data for all nutrients.
    * Resets the DataFrame's index using `.reset_index(drop=True)`. This ensures the DataFrame has a clean, sequential index, which is important for accessing rows correctly.
* Returns the cleaned DataFrame.

**4. `nutrition_calculator(df)` Function:**

* This is the core of the program. It takes the food database DataFrame (`df`) as input.
* **Initialization:**
    * Creates a dictionary called `totals` to store the cumulative nutritional information (calories, protein, carbs, fat). It starts with 0 for each.
* **Main Loop:**
    * The `while True:` loop continues until the user enters "done".
    * **User Input:**
        * Prompts the user to enter a food item. `.strip()` removes extra spaces, and `.lower()` converts the input to lowercase.
    * **Fuzzy Matching:**
        * `extractOne(food_input, df['description'], scorer=fuzz.WRatio, score_cutoff=80)`: This is where the magic happens.
            * `food_input`: The user's typed input.
            * `df['description']`: The column in the DataFrame containing the food names to search within.
            * `scorer=fuzz.WRatio`: The fuzzy matching algorithm to use. `WRatio` is generally a good all-around choice.
            * `score_cutoff=80`: This is important! It means that `extractOne` will only return a match if it's at least 80% similar to the user's input. This helps to avoid incorrect matches.
        * If `extractOne` doesn't find a match above the score cutoff (i.e., `result` is None), the program prints an error message and goes back to the beginning of the loop (`continue`).
    * **Result Processing:**
        * `extractOne` returns a tuple: `(matched_string, score, index)`. The code unpacks this into the variables `matched_food`, `score`, and `index`.
    * **Confirmation:**
        * If the match score is less than 91, the program asks the user to confirm if the match is correct. If the user says no, it goes back to the beginning of the loop. This adds a safety check for potentially ambiguous matches.
    * **Nutrient Calculation:**
        * `food_row = df.iloc[index]`: This gets the row from the DataFrame that corresponds to the best match. `df.iloc[index]` is used because we have the *index* of the matched food.
        * The program asks the user for the amount of the food item in grams.
        * It then calculates the amount of each nutrient (calories, protein, etc.) based on the grams entered. It assumes the nutrient values in the database are per 100 grams.
        * The calculated nutrients are added to the `totals` dictionary.
    * **Display Results:**
        * After the user is done entering food items, the program prints the total nutritional values from the `totals` dictionary, formatted to two decimal places.

**5. `if __name__ == "__main__":` Block:**

* This is standard Python. It means that the code inside this block will only run when the script is executed directly (not when it's imported as a module into another script).
* It calls the `load_message_user()` and `nutrition_calculator(load_food_database())` functions to start the program.

## Data Source

The nutritional data is sourced from the "cleaned_usda_foods.csv" file. It is important to ensure this file is present in the same directory as the Python script. The data in this file is derived from the USDA FoodData Central database.

## Notes

* The accuracy of the calculations depends on the accuracy and completeness of the "cleaned_usda_foods.csv" file.
* The program uses fuzzy matching, so it can handle minor spelling errors, but it may not always find the correct match. It's always a good idea to double-check the matched food item.
* Consider adding more error handling.
* The program assumes that the nutritional values in the database are per 100 grams of food.

---

## How to Use



1.  **Run the script from the command line:**

    ```bash
    python project.py
    ```

2.  **Follow the prompts:**

    * Enter food items when asked.  The program will try to find the closest match in its database.
    * Enter the amount of each food item in grams.
    * Type "done" when you've entered all the ingredients.



## Example

```
Enter food item (or 'done'): apple
✅ Matched: apple, raw (confidence: 100.0%)
Enter grams for apple, raw: 150
Enter food item (or 'done'): chicken breast
✅ Matched: chicken, broilers or fryers, breast, skinless, boneless, raw (confidence: 95.9%)
Enter grams for chicken, broilers or fryers, breast, skinless, boneless, raw: 200
Enter food item (or 'done'): done

📊 Final Nutrition Totals:
Calories: 341.00 kcal
Protein: 54.00g
Carbs: 19.62g
Fat: 8.08g
