import pytest
import csv
import pandas as pd
from unittest.mock import Mock, patch
from project import (
    load_message_user,
    load_food_database,
    nutrition_calculator
)


def test_load_message_user():
 
    message = load_message_user()
    assert "User" in message
    assert "Recipe" in message
    assert "Recipe Nutrition Calculator" in message
    assert "🥦" in message
    assert "🐍" in message
    assert "🚀" in message
    assert message.count("\n") == 4
@pytest.fixture
def load_csv_file():
    with open('cleaned_usda_foods.csv', mode='r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def test_load_food_database(load_csv_file):
    data = load_csv_file

    assert data[0]['calories'] == '867.0'
    assert data[1]['protein'] == '0.83'
    assert data[2]['carbs'] == '6.12'

    df = load_food_database()
    assert isinstance(df, pd.DataFrame)
    required_columns = {'description', 'calories', 'protein', 'carbs', 'fat'}
    assert all(col in df.columns for col in required_columns)
    assert not df['description'].isnull().any()




def test_nutrition_calculator(monkeypatch):
    # Mock Data
    mock_df = {
    'description': ['apple', 'banana', 'carrot'],
    'calories': [52, 89, 41],
    'protein': [0.3, 1.1, 0.9],
    'fat': [0.2, 0.3, 0.2],
    'carbohydrates': [14, 23, 9.6]
     }
    #https://www.geeksforgeeks.org/fixtures-in-pytest/
    #https://www.pythontutorial.net/python-unit-testing/python-patch/
    @pytest.fixture
    def mock_dataframe():
           #
           # Return a mock dataframe-like object for testing
        return mock_df
    def test_fuzzy_matching(mock_dataframe):
        # Test fuzzy matching logic
       result = process.extractOne('appl', mock_dataframe['description'], scorer=fuzz.WRatio)
       assert result[0] == 'apple'  # Matched food item
       assert result[1] >= 80       # Minimum score




     # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "banana")

    # go about using input() like you normally would:
    i = input("\nEnter food item (or 'done'): ")
    assert i == "banana"

    def test_nutrition_calculator_invalid_grams(monkeypatch, capsys):
        # Mock DataFrame

        df = pd.DataFrame({
        'description': ['apple'],
        'calories': [52],
        'protein': [0.3],
        'carbs': [14],
        'fat': [0.2]
    })

    # Mock user input: invalid grams, then 'done'
        inputs = iter(['apple', 'invalid', 'done'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        nutrition_calculator(df)

        captured = capsys.readouterr()
        assert "Invalid input - using 0 grams" in captured.out
        assert "Calories: 0.00 kcal" in captured.out
def test_nutrition_calculator_low_score_reject(monkeypatch, capsys):

    # Mock extractOne to return a low score (90)
    def mock_extract_one(*args, **kwargs):
        return ('apple pie', 90.0, 0)

    monkeypatch.setattr('rapidfuzz.process.extractOne', mock_extract_one)

    # Mock DataFrame
    mock_data = {'description': ['apple pie'], 'calories': [250], 'protein': [3], 'carbs': [35], 'fat': [10]}
    df = pd.DataFrame(mock_data)

    # Mock user input: reject match ('n'), then 'done'
    inputs = iter(['apple', 'n', 'done'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    nutrition_calculator(df)

    captured = capsys.readouterr()
    assert "Let's try again." in captured.out
    assert "Calories: 0.00 kcal" in captured.out  # No nutrients added
















