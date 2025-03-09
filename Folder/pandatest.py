import pandas as pd
import numpy as np

# Create a sample DataFrame
data = {'col1': [1, 2, 3, 4], 'col2': [5.0, 6.0, 7.0, 8.0], 'col3': ['a', 'b', 'c', 'd']}
df = pd.DataFrame(data)

# Basic operations
print("Original DataFrame:")
print(df)

print("\nData types:")
print(df.dtypes)

print("\nSummary statistics:")
print(df.describe())
# test comment
print("\nSelecting column 'col1':")
print(df['col1'])

print("\nFiltering rows where col2 > 6:")
print(df[df['col2'] > 6])

#Modifying data
df['col4'] = df['col1'] + df['col2']
print("\nDataFrame with new column 'col4':")
print(df)