import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request, redirect, url_for
from data import atp_table, wta_table, atp_df, wta_df, wta_stats, atp_stats, atp_graph_data, wta_graph_data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mpld3

app = Flask(__name__)

@app.route("/")
def home():
    # WTA graph
    fig, ax = plt.subplots(figsize=(8, 3.5))
    sns.lineplot(data=wta_graph_data, x="ranking_date", y="Points", hue="Player")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Player")
    ax.set_xlabel("Season to Date")
    ax.set_xticks([]) 
    fig.tight_layout()
    wta_graph_html=mpld3.fig_to_html(fig)
    plt.close(fig)

    # ATP graph
    fig, ax = plt.subplots(figsize=(8, 3.5))
    sns.lineplot(data=atp_graph_data, x="ranking_date", y="Points", hue="Player")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Player")
    ax.set_xlabel("Season to Date")
    ax.set_xticks([]) 
    fig.tight_layout()
    atp_graph_html=mpld3.fig_to_html(fig)
    plt.close(fig)

    return render_template("index.html", wta_html=wta_graph_html, atp_html=atp_graph_html)

@app.route("/wta")
def wta():
    return render_template("wta.html", table_html=wta_table)

@app.route("/atp")
def atp():
    return render_template("atp.html", table_html=atp_table)

@app.route("/player/<name>")
def player_name(name):
    name = name.replace("-", " ")
    
    player = wta_stats[(wta_stats["Name"].str.lower() == name.lower())]
    if player.empty:
        player = atp_stats[(atp_stats["Name"].str.lower() == name.lower())]
    
    player_info = player.to_dict(orient="records")[0]

    return render_template("player.html", player = player_info)

@app.route("/search")
def search():
    query = request.args.get("player", "").strip().lower()
    
    combined = pd.concat([atp_df, wta_df], ignore_index = True)
    match = combined[combined["Player"].str.lower().str.contains(query, na = False)]

    if not match.empty:
        player = match.iloc[0]
        name = f"{player['Player']}".replace(" ", "-")
        return redirect(url_for("player_name", name=name))
    return render_template("index.html", message=f"No player found.")

if __name__ == "__main__":
    app.run(debug=True)


