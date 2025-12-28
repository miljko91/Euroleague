import pandas as pd
import sys
from IPython.display import display

def print_data(value, position=None):
    if position is not None:
        print(f"\nAll {position}:")
        # join each team with a newline, prefixing with "-"
        output = "\n".join(f"- {v}" for v in value)
        return output
    else:
        print("Wrong position")
        sys.exit(1)

def team_selection(position=None):
    if position is not None:
        team_data = []
        print(f"{str(position).upper()} selection:")
        while True:
            team = input("Team name (or 'Q' to quit): ").strip()
            if team.upper() == 'Q':
                break
            team_data.append(team)
        return team_data
    else:
        print("Select players positions")
        sys.exit(1)

# Normalize opponent columns 
def get_opponent_stats(df, column):
    opponent_cols = [col for col in df.columns if "Opponent" in col]
    opponent_stats = {}

    for col in opponent_cols:
        cleaned = df[col].astype(str).str.replace("^@", "", regex=True).str.strip()
        for idx, opponent in cleaned.items():
            if opponent not in opponent_stats:
                opponent_stats[opponent] = {"count": 0, "points": 0}
            opponent_stats[opponent]["count"] += 1
            points = df.loc[idx, column] if pd.notna(df.loc[idx, column]) else 0
            opponent_stats[opponent]["points"] += points

    return opponent_stats

def final_print(position, matched_rows, position_name):
    print(print_data(position, position_name))

    # Map position_name to correct column
    position_column_map = {
        "guard teams": "Guard_Points",
        "forward teams": "Forwards_Points",
        "center teams": "Centers_Points"
    }

    # Normalize key
    key = position_name.lower()
    column = position_column_map.get(key)
    if column is None:
        print(f"\nInvalid position name: '{position_name}'")
        return

    # Match teams
    for pos in position:
        matches = fixtures[fixtures["Team"].str.contains(pos, case=False, na=False)]
        matched_rows = pd.concat([matched_rows, matches], ignore_index=True)
        if matches.empty:
            print(f"\nNo matches found for team: '{pos}'")

    print(f"\n{position_name}:")
    cols_to_hide = ["Guard_Points", "Forwards_Points", "Centers_Points"] 
    display(matched_rows.drop(columns=cols_to_hide))

    df = pd.DataFrame(matched_rows)

    # Run normalization with the chosen column
    opponent_counts = get_opponent_stats(df, column)

    # Print result
    print("\n")
    for team, data in sorted(opponent_counts.items(), key=lambda x: x[1]["count"], reverse=True):
        print(f"{team} {data['count']} {data['points']}")
        print("-" * 40)


# Helper function to set points
def set_points(team_name, points, column_name):
    fixtures.loc[fixtures["Team"].str.contains(team_name, case=False, na=False), f"{column_name}"] = points

# Load fixtures
fixtures = pd.read_csv("data/euroleague_round_19_22.csv")

# Add empty Points column
fixtures["Guard_Points"] = None
fixtures["Forwards_Points"] = None
fixtures["Centers_Points"] = None

# Example usage
# Anadolu Efes
set_points("Efes", 30.8, "Guard_Points")
set_points("Efes", 25.4, "Forwards_Points")
set_points("Efes", 38.1, "Centers_Points")

# Real Madrid
set_points("Real Madrid", 28.8, "Guard_Points")
set_points("Real Madrid", 23.5, "Forwards_Points")
set_points("Real Madrid", 15.5, "Centers_Points")

# Zalgiris Kaunas
set_points("Zalgiris Kaunas", 22.1, "Guard_Points")
set_points("Zalgiris Kaunas", 28.4, "Forwards_Points")
set_points("Zalgiris Kaunas", 35.2, "Centers_Points")

# Maccabi Tel Aviv
set_points("Maccabi Tel Aviv", 34.6, "Guard_Points")
set_points("Maccabi Tel Aviv", 20.8, "Forwards_Points")
set_points("Maccabi Tel Aviv", 25.6, "Centers_Points")

# Monaco
set_points("Monaco", 30.5, "Guard_Points")
set_points("Monaco", 16.7, "Forwards_Points")
set_points("Monaco", 31.7, "Centers_Points")

# Paris Basketball
set_points("Paris Basketball", 38.8, "Guard_Points")
set_points("Paris Basketball", 31.7, "Forwards_Points")
set_points("Paris Basketball", 42.1, "Centers_Points")

# Hapoel Tel Aviv
set_points("Hapoel Tel Aviv", 26, "Guard_Points")
set_points("Hapoel Tel Aviv", 15.4, "Forwards_Points")
set_points("Hapoel Tel Aviv", 23.4, "Centers_Points")

# ASVEL
set_points("ASVEL", 30.1, "Guard_Points")
set_points("ASVEL", 38.7, "Forwards_Points")
set_points("ASVEL", 35.1, "Centers_Points")

# Olympiacos
set_points("Olympiacos", 28.4, "Guard_Points")
set_points("Olympiacos", 25.8, "Forwards_Points")
set_points("Olympiacos", 26.8, "Centers_Points")

# Fenerbahçe
set_points("Fenerbahçe", 23.8, "Guard_Points")
set_points("Fenerbahçe", 19.2, "Forwards_Points")
set_points("Fenerbahçe", 24.5, "Centers_Points")

# Partizan Belgrade
set_points("Partizan Belgrade", 26.5, "Guard_Points")
set_points("Partizan Belgrade", 31.2, "Forwards_Points")
set_points("Partizan Belgrade", 59.1, "Centers_Points")

# Bayern Munich
set_points("Bayern Munich", 33.4, "Guard_Points")
set_points("Bayern Munich", 19.4, "Forwards_Points")
set_points("Bayern Munich", 29.5, "Centers_Points")

# Crvena Zvezda
set_points("Crvena Zvezda", 28.6, "Guard_Points")
set_points("Crvena Zvezda", 22.5, "Forwards_Points")
set_points("Crvena Zvezda", 37.1, "Centers_Points")

# Barcelona
set_points("Barcelona", 27, "Guard_Points")
set_points("Barcelona", 21.4, "Forwards_Points")
set_points("Barcelona", 28, "Centers_Points")

# Panathinaikos
set_points("Panathinaikos", 25.5, "Guard_Points")
set_points("Panathinaikos", 18.8, "Forwards_Points")
set_points("Panathinaikos", 32.5, "Centers_Points")

# Valencia Basket
set_points("Valencia Basket", 25, "Guard_Points")
set_points("Valencia Basket", 22.2, "Forwards_Points")
set_points("Valencia Basket", 45.01, "Centers_Points")

# Olimpia Milano
set_points("Olimpia Milano", 46.8, "Guard_Points")
set_points("Olimpia Milano", 24.3, "Forwards_Points")
set_points("Olimpia Milano", 22.2, "Centers_Points")

# Virtus Bologna
set_points("Virtus Bologna", 27.2, "Guard_Points")
set_points("Virtus Bologna", 27, "Forwards_Points")
set_points("Virtus Bologna", 48.8, "Centers_Points")

# Baskonia
set_points("Baskonia", 28.9, "Guard_Points")
set_points("Baskonia", 19.7, "Forwards_Points")
set_points("Baskonia", 24.8, "Centers_Points")

# Dubai Basketball
set_points("Dubai Basketball", 21.9, "Guard_Points")
set_points("Dubai Basketball", 27.9, "Forwards_Points")
set_points("Dubai Basketball", 28.1, "Centers_Points")

# Collect players by position
guards = team_selection(position="guards")
forwards = team_selection(position="forwards")
centers = team_selection(position="center")

matched_rows_guard = pd.DataFrame()
matched_rows_forward = pd.DataFrame()
matched_rows_center = pd.DataFrame()

if guards:
    final_print(guards,matched_rows_guard,"Guard Teams")
if forwards:
    final_print(forwards,matched_rows_forward,"Forward Teams")
if centers:
    final_print(centers,matched_rows_center,"Center Teams")