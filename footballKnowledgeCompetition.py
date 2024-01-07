# %% Imports and looking inside of csv files

import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
import seaborn as sns
import tkinter as tk
from tkinter import messagebox, simpledialog
import random

goalscorers_csv = pd.read_csv("goalscorers.csv")
results_csv = pd.read_csv("results.csv")
shootouts_csv = pd.read_csv("shootouts.csv")

print(goalscorers_csv.head())
print(results_csv.head())
print(shootouts_csv.head())

#%% 
print(goalscorers_csv.describe().T)
print(type(results_csv))
print(shootouts_csv.columns)


# %%

merge_triple = pd.merge(pd.merge(results_csv,shootouts_csv, how='left', on=['date', 'home_team', 'away_team']),
                        goalscorers_csv, how='left', on=['date', 'home_team', 'away_team']);print(merge_triple)
# %%
print(merge_triple["first_shooter"].isnull().sum())
# %%
def turkeysCondition():
    output = merge_triple[(merge_triple["home_team"]=="Turkey")|((merge_triple["away_team"]=="Turkey"))]
    return output
matches = turkeysCondition()  
print(matches)
# %%
print(matches.head(10))
# %%
print(merge_triple[lambda x : x["city"]=="Berlin"])
# %%
shootouts_csv.columns
first_shooter_ones = shootouts_csv[shootouts_csv['first_shooter'].notnull()]
first_shooter_ones['winner'].describe()

# %%
merge_triple.head(1)
# %%
cols_to_check = ['date', 'home_team', 'away_team']  # Replace with the column names you want to check

# Find duplicates based on specific columns
duplicates = merge_triple[merge_triple.duplicated(subset=cols_to_check, keep=False)]

# Display the duplicate rows based on specific columns
print("Duplicate Rows based on specific columns:")
print(duplicates)

# Count the number of duplicate rows based on specific columns
num_duplicates = len(duplicates)
print(f"Number of duplicate rows based on specific columns: {num_duplicates}")
# %%
unique_merged = merge_triple.drop_duplicates(subset=["date","home_team","away_team"],inplace=False)
print(unique_merged)
# %%
# Assuming 'unique_merged_data' is your DataFrame containing unique match entries
def get_match_result(row):
    home_score = row['home_score']
    away_score = row['away_score']
    
    if home_score > away_score:
        return row['home_team']
    elif home_score < away_score:
        return row['away_team']
    else:
        return 'Draw'

# Apply the function to create the 'match_result' column
unique_merged['match_result'] = unique_merged.apply(get_match_result, axis=1)

# Display the DataFrame with the new column
print(unique_merged[['home_team', 'away_team', 'home_score', 'away_score', 'match_result']])


# %%

def generate_questions(data):
    questions_list = []
    for index, row in data.iterrows():
        question = {
            "date": row['date'],
            "home_team": row['home_team'],
            "away_team": row['away_team'],
            "answer": row['match_result']  # Adjust with your column name containing correct answers
        }
        questions_list.append(question)
    return questions_list


def start_game(num_questions):
    global questions, score
    questions = generate_questions(unique_merged)
    random.shuffle(questions)  # Shuffle the questions for random selection
    score = 0
    update_scoreboard()
    next_question(num_questions)

def check_answer(answer):
    global score
    if answer == current_question['answer']:
        score += 1
        messagebox.showinfo("Result", "Correct!")
    else:
        score = max(0, score - 1)  # Score cannot be negative
        messagebox.showinfo("Result", f"Wrong! The correct answer is: {current_question['answer']}")
    update_scoreboard()
    next_question()

def update_scoreboard():
    scoreboard_label.config(text=f"Score: {score}")

def next_question(num_questions=10):
    global current_question
    if num_questions > 0 and questions:
        current_question = questions.pop(0)
        num_questions -= 1
        question_label.config(text=f"Date: {current_question['date']}\nHome Team: {current_question['home_team']}\nAway Team: {current_question['away_team']}")
        remaining_label.config(text=f"Remaining Questions: {num_questions}")
    else:
        messagebox.showinfo("End of Questions", f"Your final score: {score}")

def settings():
    num = simpledialog.askinteger("Settings", "Enter the number of questions:", initialvalue=10)
    if num:
        start_game(num)

def exit_game():
    root.destroy()

# Tkinter setup
root = tk.Tk()
root.title("Football Knowledge Test")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

play_menu = tk.Menu(menu_bar, tearoff=0)
play_menu.add_command(label="Play", command=lambda: start_game(10))
play_menu.add_command(label="Settings", command=settings)
play_menu.add_separator()
play_menu.add_command(label="Exit", command=exit_game)
menu_bar.add_cascade(label="Menu", menu=play_menu)

root.configure(bg='lightblue')  # Set background color

question_label = tk.Label(root, text="", font=("Arial", 12), bg='lightblue')
question_label.pack(pady=20)

button_frame = tk.Frame(root, bg='lightblue')
button_frame.pack(pady=10)

home_button = tk.Button(button_frame, text="Home Team", command=lambda: check_answer(current_question["home_team"]), bg='green', fg='white', width=15)
home_button.grid(row=0, column=0, padx=5)

away_button = tk.Button(button_frame, text="Away Team", command=lambda: check_answer(current_question["away_team"]), bg='blue', fg='white', width=15)
away_button.grid(row=0, column=1, padx=5)

draw_button = tk.Button(button_frame, text="Draw", command=lambda: check_answer("Draw"), bg='orange', width=15)
draw_button.grid(row=0, column=2, padx=5)

scoreboard_label = tk.Label(root, text="Score: 0", font=("Arial", 12), bg='lightblue')
scoreboard_label.pack(pady=10)

remaining_label = tk.Label(root, text="Remaining Questions: 10", font=("Arial", 12), bg='lightblue')
remaining_label.pack(pady=10)

root.mainloop()



# %%
