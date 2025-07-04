# import pandas as pd

# def get_solar_potential(state: str, filepath='data/cleaned_solar_potential.csv') -> float:
#     df = pd.read_csv(filepath)
#     df['State'] = df['State'].str.strip().str.lower()

#     row = df[df['State'] == state.lower()]
#     if row.empty:
#         raise ValueError(f"Solar potential not found for state: {state}")

#     return float(row.iloc[0]['SolarPotentialMW'])

# def calculate_solar_generation_gwh(solar_potential_mw: float) -> float:
#     hours_per_day = 5
#     days_per_year = 365
#     performance_ratio = 0.75

#     generation_gwh = (solar_potential_mw * hours_per_day * days_per_year * performance_ratio) / 1000
#     return round(generation_gwh, 2)
import pandas as pd
import difflib

def get_solar_potential(state: str, filepath='data/cleaned_solar_potential.csv') -> float:
    df = pd.read_csv(filepath)
    df['State'] = df['State'].str.strip().str.lower()

    state = state.strip().lower()

    if state not in df['State'].values:
        closest = difflib.get_close_matches(state, df['State'].tolist(), n=1)
        suggestion = f" Did you mean '{closest[0]}'?" if closest else ""
        raise ValueError(f"Solar potential not found for state: '{state}'.{suggestion}")

    return float(df[df['State'] == state]['SolarPotentialMW'].iloc[0])

def calculate_solar_generation_gwh(solar_potential_mw: float) -> float:
    hours_per_day = 5
    days_per_year = 365
    performance_ratio = 0.75

    generation_gwh = (solar_potential_mw * hours_per_day * days_per_year * performance_ratio) / 1000
    return round(generation_gwh, 2)
