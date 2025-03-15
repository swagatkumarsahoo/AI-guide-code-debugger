import pandas as pd

# Read data from CSV file with error handling
try:
    df = pd.read_csv('simpsons_data.csv', parse_dates=['Month'])
except FileNotFoundError:
    print("Error: The file 'simpsons_data.csv' was not found.")
    exit(1)
except pd.errors.EmptyDataError:
    print("Error: The file 'simpsons_data.csv' is empty.")
    exit(1)
except pd.errors.ParserError:
    print("Error: The file 'simpsons_data.csv' could not be parsed.")
    exit(1)

# Display basic statistics with improved formatting
print("\nBasic Statistics:")
print(df.describe().to_string())

# Calculate additional statistics with user input
additional_stats = input("Would you like to calculate additional statistics? (yes/no): ")
if additional_stats.lower() == 'yes':

    max_value = df['the simpsons: (Worldwide)'].max()
    min_value = df['the simpsons: (Worldwide)'].min()
    average_value = df['the simpsons: (Worldwide)'].mean()

    print("\nAdditional Statistics:")
    print(f"Max Value: {max_value}")
    print(f"Min Value: {min_value}")
    print(f"Average Value: {average_value}")

    # More complex statistics
    median_value = df['the simpsons: (Worldwide)'].median()
    std_deviation = df['the simpsons: (Worldwide)'].std()
    variance = df['the simpsons: (Worldwide)'].var()

    print("\nMore Complex Statistics:")
    print(f"Median Value: {median_value}")
    print(f"Standard Deviation: {std_deviation}")
    print(f"Variance: {variance}")
else:
    print("Skipping additional statistics.")

# Plotting the data with enhancements
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
df.plot(x='Month', y='the simpsons: (Worldwide)', title='The Simpsons Google Trends', legend=True)
plt.xlabel('Month')
plt.ylabel('Worldwide Interest')
plt.grid()
plt.show()
