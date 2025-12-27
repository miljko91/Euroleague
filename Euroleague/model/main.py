import pandas as pd
import sys

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
def get_opponent_stats(df): 
    opponent_cols = [col for col in df.columns if "Opponent" in col] 
    opponent_stats = {}
    for col in opponent_cols: 
        cleaned = df[col].astype(str).str.replace("^@", "", regex=True).str.strip() 
        for idx, opponent in cleaned.items(): 
            if opponent not in opponent_stats: opponent_stats[opponent] = {"count": 0, "points": 0} 
            opponent_stats[opponent]["count"] += 1 
            opponent_stats[opponent]["points"] += df.loc[idx, "Points"] if pd.notna(df.loc[idx, "Points"]) else 0 
    return opponent_stats

def final_print(position, matched_rows, position_name):
    print(print_data(position, position_name))
    for pos in position:
        matches = fixtures[fixtures["Team"].str.contains(pos, case=False, na=False)] 
        matched_rows = pd.concat([matched_rows, matches], ignore_index=True)
        if not matches.empty:
            pass
        else: 
            print(f"\nNo matches found for team: '{pos}'")
    print(f"\n{position_name}: ",matched_rows)
    df = pd.DataFrame(matched_rows)
    # Run normalization 
    opponent_counts = get_opponent_stats(df)
    # Print result
    print("\n")
    for team, data in sorted(opponent_counts.items(), key=lambda x: x[1]["count"], reverse=True): 
        print(f"{team} {data['count']} {data['points']}")
        print("-" * 40)

# Helper function to set points
def set_points(team_name, points):
    fixtures.loc[fixtures["Team"].str.contains(team_name, case=False, na=False), "Points"] = points

# Load fixtures
fixtures = pd.read_csv("data/euroleague_fixtures_rounds_18_20.csv")

# Add empty Points column
fixtures["Points"] = None

# Example usage
set_points("Efes", 36) 
set_points("Real Madrid", 40) 
set_points("Zalgiris", 33) 
set_points("Maccabi", 28) 
set_points("Monaco", 39) 
set_points("Paris", 27) 
set_points("Hapoel", 31) 
set_points("ASVEL", 22) 
set_points("Olympiacos", 34) 
set_points("Fenerbahçe", 29) 
set_points("Partizan", 37) 
set_points("Bayern", 25) 
set_points("Crvena", 32) 
set_points("Barcelona", 40) 
set_points("Panathinaikos", 30) 
set_points("Valencia", 26) 
set_points("Milano", 35) 
set_points("Virtus", 23) 
set_points("Baskonia", 38) 
set_points("Dubai", 21)

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