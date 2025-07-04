# import pandas as pd

# def get_state_data(state_name: str, filepath='data/final_consumption.csv') -> pd.DataFrame:
#     """
#     Loads and filters electricity consumption data for the given state.

#     Args:
#         state_name (str): Name of the state (case-insensitive)
#         filepath (str): Path to cleaned CSV (default: 'data/final_consumption.csv')

#     Returns:
#         pd.DataFrame: DataFrame with columns ['Year', 'Consumption'] for the state
#     """
#     try:
#         df = pd.read_csv(filepath)
#         df['State'] = df['State'].str.strip().str.title()

#         filtered_df = df[df['State'] == state_name.title()]

#         if filtered_df.empty:
#             raise ValueError(f"State '{state_name}' not found in dataset.")

#         return filtered_df[['Year', 'Consumption']].sort_values('Year')

#     except Exception as e:
#         raise RuntimeError(f"Error loading state data: {e}")

import pandas as pd
import difflib

def get_state_data(state_name: str, filepath='data/final_consumption.csv') -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath)
        df['State'] = df['State'].str.strip().str.lower()
        df = df.dropna(subset=['Consumption'])  # remove NaNs

        state_name = state_name.strip().lower()

        if state_name not in df['State'].values:
            closest = difflib.get_close_matches(state_name, df['State'].tolist(), n=1)
            suggestion = f" Did you mean '{closest[0]}'?" if closest else ""
            raise ValueError(f"State '{state_name}' not found in dataset.{suggestion}")

        filtered_df = df[df['State'] == state_name]
        return filtered_df[['Year', 'Consumption']].sort_values('Year')

    except Exception as e:
        raise RuntimeError(f"Error loading state data: {e}")
