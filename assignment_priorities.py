from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, normalize

# Let's load the CSV file the user has uploaded and process it directly
file_path = './Assignment Catchup.csv'

GRADE_WEIGHT = 1
DUE_DATE_WEIGHT = 1
DIFFICULTY_WEIGHT = .5


# Reading the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)


def calculate_grade_score(row, avg_pct):
    # return (row["Grade Percentage"] / 15)
    return row["Grade Percentage"]

def calculate_difficulty_score(row):
    return 2 - row["Difficulty Weight"]

# def calculate_due_date_score(row):
#     due_date_score = 1
#     days_until_due = row["Days Until Due"]
#     if days_until_due == 0:
#         due_date_score = 1
#     elif days_until_due < 0:
#         due_date_score = (abs(days_until_due) / 15) + 1
#     else:
#         due_date_score = 1 / days_until_due
#     return due_date_score
def calculate_due_date_score(df):
    values = df["Days Until Due"].values.reshape(-1,1)
    scaler = MinMaxScaler(feature_range=(0,2))
    normalized_values = scaler.fit_transform(values)
    normalized_array = normalized_values + (1- scaler.transform(np.array([[0]]))[0][0])
    return 2 - normalized_array



# Define the priority score formula
def calculate_priority(row):
    return (GRADE_WEIGHT * row["grade_score"] + DUE_DATE_WEIGHT * row["due_date_score"] + DIFFICULTY_WEIGHT * row["difficulty_score"]) / sum([GRADE_WEIGHT, DUE_DATE_WEIGHT, DIFFICULTY_WEIGHT])


def parse_date(row):
    return datetime.strptime(row["Due Date"], "%m/%d").replace(year=2024)

def format_date(row):
    return row["Due Date"].strftime("%m/%d")


# Convert 'Due Date' to datetime and calculate days until due date
today = datetime.today()
df["Due Date"] = df.apply(parse_date, axis=1)
df["Days Until Due"] = df.apply(lambda row: (row["Due Date"] - today).days + 1, axis=1)

# Apply the score calculations
avg_pct = df["Grade Percentage"].mean()


scaler = MinMaxScaler(feature_range=(0,2))

df["grade_score"] = scaler.fit_transform(df["Grade Percentage"].values.reshape(-1,1))

df["due_date_score"] = calculate_due_date_score(df)
df["difficulty_score"] = 2 - (scaler.fit_transform(df["Difficulty Weight"].values.reshape(-1,1)))
# df["grade_score"] = df.apply(calculate_grade_score, axis=1, avg_pct=avg_pct)
# df["due_date_score"] = df.apply(calculate_due_date_score, axis=1)
# df["difficulty_score"] = df.apply(calculate_difficulty_score, axis=1)

# Apply the priority score calculation
df["Priority Score"] = df.apply(calculate_priority, axis=1)

df["Due Date"] = df.apply(format_date, axis=1)

# Sort the assignments by priority score (descending order)
df_sorted = df.sort_values(by="Priority Score", ascending=False)

print("columns:", df_sorted.columns)


# Display dataframe in a table
print(df_sorted.loc[:,['Priority Score', 'Assignment', 'Due Date', 'Days Until Due', 'due_date_score', 'Grade Percentage','grade_score', 'Difficulty Weight', 'difficulty_score']].to_string(index=False))

