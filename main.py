from tools.data_loader import load_survey_data


print("Starting NPS Analyst")

df = load_survey_data()

print("\nFirst five rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)