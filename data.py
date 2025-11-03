import pandas as pd

# ATP data
atp_rankings_df = pd.read_csv("data/atp_rankings_current.csv")
atp_players_df = pd.read_csv("data/atp_players.csv", low_memory=False)
atp_match_df = pd.read_csv("data/atp_matches_2024.csv")

# WTA data
wta_rankings_df = pd.read_csv("data/wta_rankings_current.csv")
wta_players_df = pd.read_csv("data/wta_players.csv", low_memory=False)
wta_match_df = pd.read_csv("data/wta_matches_2024.csv")

def rankings_table(rankings_df, players_df):
    rankings_df = rankings_df.sort_values(by=["ranking_date", "rank"], ascending=[False, True])
    merged = pd.merge(rankings_df, players_df, left_on="player", right_on="player_id")
    merged["Player"] = merged["name_first"] + " " + merged["name_last"]
    merged = merged.rename(columns={"rank": "Ranking", "points": "Points"})
    merged = merged[["Player", "Ranking", "Points"]].head(32)
    merged["Player"] = merged["Player"].apply(lambda name: f'<a href="/player/{name.replace(" ", "-").lower()}">{name}</a>')
    return merged.to_html(classes="table table-striped", index=False, escape=False)

def rankings_df(rankings_df, players_df):
    rankings_df = rankings_df.sort_values(by=["ranking_date", "rank"], ascending=[False, True])
    merged = pd.merge(rankings_df, players_df, left_on="player", right_on="player_id")
    merged["Player"] = merged["name_first"] + " " + merged["name_last"]
    merged = merged.rename(columns={"rank": "Ranking", "points": "Points"})
    merged["dob"] = pd.to_datetime(merged["dob"], errors='coerce', format='%Y%m%d').dt.date
    merged = merged.head(32)
    return merged

def stats(match_df):
    winner_stats = match_df[['winner_name','w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon','w_SvGms', 'w_bpSaved', 'w_bpFaced']]
    winner_stats = winner_stats.rename(columns={'winner_name': 'Name', 'w_ace': 'Ace', 'w_df': 'Double_Faults', 'w_svpt': 'Total_Serve_Points_Played', 'w_1stIn': 'First_Serve_In', 'w_1stWon': 'First_Serve_Won', 'w_2ndWon': 'Second_Serve_Won', 'w_SvGms': 'Service_Games', 'w_bpSaved': 'Break_Points_Saved', 'w_bpFaced':'Break_Points_Faced'})
    loser_stats = match_df[['loser_name','l_ace', 'l_df', 'l_svpt','l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced']]
    loser_stats = loser_stats.rename(columns={'loser_name': 'Name', 'l_ace': 'Ace', 'l_df': 'Double_Faults', 'l_svpt': 'Total_Serve_Points_Played', 'l_1stIn': 'First_Serve_In', 'l_1stWon': 'First_Serve_Won', 'l_2ndWon': 'Second_Serve_Won', 'l_SvGms': 'Service_Games', 'l_bpSaved': 'Break_Points_Saved', 'l_bpFaced':'Break_Points_Faced'})
    player_stats = pd.concat([winner_stats, loser_stats])
    player_stats = player_stats.dropna()
    player_stats["First_Serve_Perc"] = player_stats["First_Serve_In"] / player_stats["Total_Serve_Points_Played"] 
    player_stats["First_Serve_Perc_Won"] = player_stats["First_Serve_Won"] / player_stats["First_Serve_In"]
    player_stats["Second_Serve_Perc_Won"] =  player_stats["Second_Serve_Won"] / (player_stats["Total_Serve_Points_Played"] - player_stats["First_Serve_In"] - player_stats["Double_Faults"])
    player_stats["Perc_Break_Points_Saved"] = player_stats["Break_Points_Saved"] / player_stats["Break_Points_Faced"]
    player_stats = player_stats.groupby("Name", as_index=False).mean().round(decimals=2)
    return player_stats


wta_table = rankings_table(wta_rankings_df, wta_players_df)
atp_table = rankings_table(atp_rankings_df, atp_players_df)
wta_df = rankings_df(wta_rankings_df, wta_players_df)
atp_df = rankings_df(atp_rankings_df, atp_players_df)
wta_stats = pd.merge(wta_df, stats(wta_match_df), how="inner", left_on="Player", right_on="Name")
atp_stats = pd.merge(atp_df, stats(atp_match_df), how="inner", left_on="Player", right_on="Name")

def graphing_data(rankings_df, players_df):
    merged = pd.merge(rankings_df, players_df, left_on="player", right_on="player_id")
    merged["Player"] = merged["name_first"] + " " + merged["name_last"]
    merged = merged.rename(columns={"rank": "Ranking", "points": "Points"})
    merged = merged[["ranking_date", "Player", "Ranking", "Points"]]
    merged = merged.sort_values(by=["ranking_date", "Ranking"], ascending=[True, True])
    merged["ranking_date"] = pd.to_datetime(merged["ranking_date"], errors='coerce', format='%Y%m%d').dt.date
    graph_data = merged.groupby("ranking_date", group_keys=False).head(8)
    return graph_data

atp_graph_data = graphing_data(atp_rankings_df, atp_players_df)
wta_graph_data = graphing_data(wta_rankings_df, wta_players_df)
