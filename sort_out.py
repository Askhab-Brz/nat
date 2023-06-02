import pandas as pd
df = pd.read_csv('natwest_res.csv')

# Drop rows with empty columns or "NO_DATA" values


# Drop rows with empty columns
df = df.dropna()   # Drop rows with empty columns
df = df[df != 'NO_DATA'].dropna()  # Drop rows without salary
# Write the updated DataFrame to a new CSV file
df.to_csv('natwest_with_salaries.csv', index=False)
