from utils.cleaner import load_and_clean

df = load_and_clean('data/maharashtra.csv', 'Maharashtra')
print(df)