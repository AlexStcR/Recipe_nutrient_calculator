import pandas as pd
from rapidfuzz import fuzz
from rapidfuzz.process import extractOne
import emoji


#https://www.geeksforgeeks.org/fuzzywuzzy-python-library/
#https://blog.finxter.com/5-best-ways-to-do-fuzzy-matching-on-a-pandas-dataframe-column-using-python/
#https://www.geeksforgeeks.org/python-pandas-series-str-find/
#https://www.geeksforgeeks.org/pandas-tutorial/
#https://www.geeksforgeeks.org/how-to-do-fuzzy-matching-on-pandas-dataframe-column-using-python/

def load_message_user():

    message = (

    f"Hello, User! {emoji.emojize(':smiling_face_with_smiling_eyes:')}\n"
    f"Welcome to our Recipe Nutrition Calculator program! {emoji.emojize(':snake:')}\n"
    f"Enter your ingredients and their amounts to calculate the total nutrients in your recipe!{emoji.emojize(':broccoli:')}{emoji.emojize(':bread:')} \n"
    f"Feel free to experiment and enjoy the process! {emoji.emojize(':rocket:')}\n"

    )
    return message




def load_food_database():
    """Load and prepare the food database with proper indexing"""
    df = pd.read_csv("cleaned_usda_foods.csv")
    # Clean
    # Make all lower case (dataset all in lower already, just to make sure)
    df['description'] = df['description'].fillna('').str.lower()

    df.fillna(0, inplace=True)
    df = df.reset_index(drop=True)  # Ensure clean indexing

    #print(df[['description', 'calories', 'protein', 'carbs', 'fat']].head(20))
    return df

def nutrition_calculator(df):
    #start all nutrients as float zero
    totals = {'calories': 0.0, 'protein': 0.0, 'carbs': 0.0, 'fat': 0.0}

    while True:
        food_input = input("\nEnter food item (or 'done'): ").strip().lower()
        if food_input == 'done':
            break

        # Fuzzy match with score threshold
        #extractone  Finds the best match for the user's input in the database.
        #process.extractOne(query, choice, scorer): Extracts the only closest match from the choice list which matches the
        # given query and scorer is the optional parameter to make it use a particular scorer like fuzz.token_sort_ratio, fuzz.token_set_ratio
        result = extractOne(food_input,df['description'],scorer=fuzz.WRatio, score_cutoff=80)

        if not result:
            print(f"⚠️ No good match found for '{food_input}'. Try again.")

            continue


       # print(result)
        #result is a tuple

        lst=[]
        for i in result:
            lst.append(i)
        #print(lst)
        matched_food=lst[0]
        score=lst[1]
        index=lst[2]
        #print(matched_food)

        if score < 91:
            print(f"Is '{matched_food}' the right food?")
            user_input = input("Type y for yes, or n for no: ").strip().lower()

            if user_input == 'y':

                 pass
            else:
                print("Let's try again.")
                continue  # Go back to start of loop
        else:

            pass


        #using iloc, as we have the index
        food_row = df.iloc[index]

        print(f"✅ Matched: {food_row['description']} (confidence: {score:.1f}%)")

        try:
            amount = float(input(f"Enter grams for {food_row['description']}: "))
        except ValueError:
            print("❌ Invalid input - using 0 grams")
            amount = 0

        # Accumulate nutrients
        #loop trough totals adding the items

        for i in totals:
            totals[i] += (food_row[i] / 100) * amount

    # Display final results
    print("\n📊 Final Nutrition Totals:")

    #loops again trough totals in order to print the results
    for nutrient, value in totals.items():
        print(f"{nutrient.capitalize()}: {value:.2f}{'g' if nutrient != 'calories' else ' kcal'}")


if __name__ == "__main__":
    print(load_message_user())



    nutrition_calculator(load_food_database())




