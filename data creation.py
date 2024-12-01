import axelrod as axl
import axelrod.interaction_utils as iu
import pandas as pd
import types

# Create a list of players (strategies)
players = [s() for s in list(axl.basic_strategies) if not isinstance(s, types.GeneratorType)]

# Initialize an empty list to store match data
match_data = []

# Run matches and store the player names, first player's moves, and the next move
for player1 in players:
    for player2 in players:
        match = axl.Match([player1, player2], turns=100)
        match.play()
        moves = match.result
        first_player_moves = [move[0] for move in moves]  # Extract only the first player's moves
        opponent_moves = [move[1] for move in moves]  # Extract only the opponent's moves
        cooperations = iu.compute_cooperations(moves)
        next_move = first_player_moves[-1] if first_player_moves else None  # Extract the last move of the first player
        match_data.append({
            'Players': f"{player1.__class__.__name__} vs {player2.__class__.__name__}",
            'Moves': first_player_moves[:-1],  # Exclude the last move
            'Opponent Moves': opponent_moves[:-1],
            'Next Move': next_move,
            'Cooperation Rate': cooperations[0]/len(moves),
            'Opponent Cooperation Rate': cooperations[1]/len(moves)
        })

# Create a DataFrame from the match data
match_table_df = pd.DataFrame(match_data)

# Add additional columns
match_table_df['Last Move'] = match_table_df['Moves'].apply(lambda x: x[-1] if x else None)
match_table_df['Opponent Last Move'] = match_table_df['Opponent Moves'].apply(lambda x: x[-1] if x else None)
match_table_df['Penultimate Move'] = match_table_df['Moves'].apply(lambda x: x[-2] if x else None)
match_table_df['Opponent Penultimate Move'] = match_table_df['Opponent Moves'].apply(lambda x: x[-2] if x else None)
match_table_df['Penultimate + 1 Move'] = match_table_df['Moves'].apply(lambda x: x[-3] if x else None)
match_table_df['Opponent Penultimate + 1 Move'] = match_table_df['Opponent Moves'].apply(lambda x: x[-3] if x else None)


def copied_opponent_last_move(row):
    moves = row['Moves']
    opponent_moves = row['Opponent Moves']
    copied_count = 0
    for i in range(1, len(moves)):
        if moves[i] == opponent_moves[i-1]:  # Player copied the opponent's last move
            copied_count += 1
    return copied_count / len(moves) if len(moves) > 0 else None

# Apply the function to calculate the copy rate
match_table_df['Copy Rate'] = match_table_df.apply(copied_opponent_last_move, axis=1)

#Save data as training and target csv files
match_table_df.drop(columns=['Moves', 'Opponent Moves','Next Move']).to_csv('training.csv')
match_table_df['Next Move'].to_csv('target.csv')