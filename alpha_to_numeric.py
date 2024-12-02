import pandas as pd

# Load the CSV file
training_data = pd.read_csv('training.csv')
target_data = pd.read_csv('target.csv')

# Replace 'C' with 1 and 'D' with 0 in the entire dataframe
training_data = training_data.replace({'C': 1, 'D': 0})
target_data = target_data.replace({'C': 1, 'D': 0})

# Save the binary CSV file back
training_data.to_csv('training_binary.csv', index=False)
target_data.to_csv('target_binary.csv', index=False)