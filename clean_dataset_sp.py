import pandas as pd

def clean_solar_potential(input_path='data/solar_potential.csv', output_path='data/cleaned_solar_potential.csv'):
    try:
        df = pd.read_csv(input_path)
        print("CSV Columns:", df.columns.tolist())

        # Load the dataset
        df = pd.read_csv(input_path)

        # Strip whitespace and standardize casing for state names
        df['State'] = df['State'].astype(str).str.strip().str.title()

        # Ensure SolarPotentialMW is numeric
        df['SolarPotentialMW'] = pd.to_numeric(df['SolarPotentialMW'], errors='coerce')

        # Drop rows where SolarPotentialMW is missing or invalid
        df = df.dropna(subset=['SolarPotentialMW'])

        # Optional: Remove duplicates
        df = df.drop_duplicates(subset=['State'])

        # Save cleaned file
        df.to_csv(output_path, index=False)
        print(f"✅ Cleaned data saved to: {output_path}")

    except Exception as e:
        print(f"❌ Error cleaning solar potential dataset: {e}")

if __name__ == '__main__':
    clean_solar_potential()
