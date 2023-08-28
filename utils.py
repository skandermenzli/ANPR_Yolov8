
import pandas as pd

# write in csv
def update_csv(entry):
    df = pd.read_csv('output.csv')
    # Check if the new entry's ID already exists in the DataFrame
    if entry['id'] in df['id'].values:
        # Find the index of the existing entry with the same ID
        index = df.index[df['id'] == entry['id']][0]

        # Compare scores and update if the new score is bigger
        if entry['score'] > df.loc[index, 'score']:
            df.loc[index, 'score'] = entry['score']
            df.loc[index, 'number'] = entry['number']
    else:
        # Append the new entry to the DataFrame
        df.loc[len(df)] = entry

        # Save the DataFrame back to the CSV file
    df.to_csv('output.csv', index=False)