from utils.cleaner import get_state_data
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_demand(state: str, year: int, filepath='data/final_consumption.csv') -> float:
    """
    Predicts electricity demand (GWh) for a given state and year using Linear Regression.

    Args:
        state (str): Name of the state (e.g., 'Maharashtra')
        year (int): Year to predict demand for (e.g., 2026)
        filepath (str): Path to cleaned dataset (default is final_consumption.csv)

    Returns:
        float: Predicted demand in GWh (rounded to 2 decimal places)
    """
    df = get_state_data(state, filepath)

    # Prepare training data
    X = df['Year'].values.reshape(-1, 1)
    y = df['Consumption'].values.reshape(-1, 1)

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Predict
    prediction = model.predict(np.array([[year]]))
    return round(prediction[0][0], 2)
