# Example usage
from utils.solar import get_solar_potential, calculate_solar_generation_gwh

state = "Maharashtra"
potential_mw = get_solar_potential(state)
generation_gwh = calculate_solar_generation_gwh(potential_mw)

print(f"{state} can generate {generation_gwh} GWh/year from {potential_mw} MW solar potential.")
