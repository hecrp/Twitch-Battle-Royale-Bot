import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
from models import get_users, get_games, get_user_stats, get_recent_games

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#f8f9fa',
    'text': '#212529',
    'primary': '#007bff',
    'secondary': '#6c757d',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545'
}

graph_layout = {
    'plot_bgcolor': colors['background'],
    'paper_bgcolor': colors['background'],
    'font': {'color': colors['text']},
    'title': {'font': {'size': 20, 'color': colors['primary']}},
    'xaxis': {'title': {'font': {'size': 14, 'color': colors['secondary']}}},
    'yaxis': {'title': {'font': {'size': 14, 'color': colors['secondary']}}},
}

def create_header():
    return dbc.Row([
        dbc.Col(html.H1("Twitch Battle Royale Dashboard", className="text-center text-primary my-4"), width=12)
    ])
def create_graphs():
    user_stats = pd.DataFrame(get_user_stats())
    
    kills_graph = dcc.Graph(
        id='kills-graph',
        figure=px.bar(
            user_stats.sort_values('total_kills', ascending=False),
            x='username',
            y='total_kills',
            title='Total Kills by User',
            labels={'total_kills': 'Total Kills', 'username': 'Username'},
            hover_data=['games_played', 'wins']
        ).update_layout(graph_layout)
    )

    best_hit_graph = dcc.Graph(
        id='best-hit-graph',
        figure=px.bar(
            user_stats.sort_values('best_hit', ascending=False),
            x='username',
            y='best_hit',
            title='Best Hit by User',
            labels={'best_hit': 'Best Hit', 'username': 'Username'},
            hover_data=['total_kills', 'games_played']
        ).update_layout(graph_layout)
    )

    games_played_graph = dcc.Graph(
        id='games-played-graph',
        figure=px.bar(
            user_stats.sort_values('games_played', ascending=False),
            x='username',
            y='games_played',
            title='Games Played by User',
            labels={'games_played': 'Games Played', 'username': 'Username'},
            hover_data=['total_kills', 'wins']
        ).update_layout(graph_layout)
    )

    return dbc.Row([
        dbc.Col(kills_graph, width=12, lg=4, className="mb-4"),
        dbc.Col(best_hit_graph, width=12, lg=4, className="mb-4"),
        dbc.Col(games_played_graph, width=12, lg=4, className="mb-4")
    ])
def create_tables():
    return dbc.Row([
        dbc.Col([
            html.H3("User Statistics", className="text-center text-secondary mb-3", style={'font-family': 'Arial, sans-serif', 'font-weight': 'bold'}),
            dash_table.DataTable(
                id='user-stats-table',
                columns=[
                    {'name': 'Player', 'id': 'username'},
                    {'name': 'Battles Fought', 'id': 'games_played'},
                    {'name': 'Total Eliminations', 'id': 'total_kills'},
                    {'name': 'Highest Damage', 'id': 'best_hit'},
                    {'name': 'Victories', 'id': 'wins'}
                ],
                style_header={
                    'backgroundColor': colors['primary'],
                    'color': colors['background'],
                    'fontWeight': 'bold',
                    'font-family': 'Arial, sans-serif'
                },
                style_cell={
                    'backgroundColor': colors['background'],
                    'color': colors['text'],
                    'border': f'1px solid {colors["secondary"]}',
                    'font-family': 'Helvetica, sans-serif',
                    'textAlign': 'left'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f2f2f2'
                    },
                    {
                        'if': {'column_id': 'total_kills'},
                        'color': colors['danger']
                    },
                    {
                        'if': {'column_id': 'wins'},
                        'color': colors['success']
                    }
                ],
                style_table={'overflowX': 'auto'},
                sort_action='native',
                filter_action='native',
                page_action='native',
                page_current=0,
                page_size=10,
            )
        ], width=12, lg=6, className="mb-4"),
        dbc.Col([
            html.H3("Recent Games", className="text-center text-secondary mb-3", style={'font-family': 'Arial, sans-serif', 'font-weight': 'bold'}),
            dash_table.DataTable(
                id='recent-games-table',
                columns=[
                    {'name': 'Game ID', 'id': 'id'},
                    {'name': 'Date', 'id': 'created_at'},
                    {'name': 'Champion', 'id': 'winner'},
                    {'name': 'Participants', 'id': 'total_participants'}
                ],
                style_header={
                    'backgroundColor': colors['primary'],
                    'color': colors['background'],
                    'fontWeight': 'bold',
                    'font-family': 'Arial, sans-serif'
                },
                style_cell={
                    'backgroundColor': colors['background'],
                    'color': colors['text'],
                    'border': f'1px solid {colors["secondary"]}',
                    'font-family': 'Helvetica, sans-serif',
                    'textAlign': 'left'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f2f2f2'
                    },
                    {
                        'if': {'column_id': 'winner'},
                        'color': colors['success']
                    }
                ],
                style_table={'overflowX': 'auto'},
                sort_action='native',
                page_action='native',
                page_current=0,
                page_size=5,
            )
        ], width=12, lg=6, className="mb-4")
    ])

# Layout
app.layout = dbc.Container([
    create_header(),
    create_graphs(),
    create_tables(),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # in milliseconds
        n_intervals=0
    )
], fluid=True, className="px-4")

@app.callback(
    [dash.dependencies.Output('kills-graph', 'figure'),
     dash.dependencies.Output('best-hit-graph', 'figure'),
     dash.dependencies.Output('games-played-graph', 'figure'),
     dash.dependencies.Output('user-stats-table', 'data'),
     dash.dependencies.Output('user-stats-table', 'columns'),
     dash.dependencies.Output('recent-games-table', 'data'),
     dash.dependencies.Output('recent-games-table', 'columns')],
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    users = get_users()
    user_stats = get_user_stats()
    recent_games = get_recent_games()

    df_users = pd.DataFrame(users)
    df_user_stats = pd.DataFrame(user_stats)
    df_recent_games = pd.DataFrame(recent_games)

    kills_fig = px.bar(df_users, x='username', y='kills', title='Kills per User')
    kills_fig.update_layout(graph_layout)
    kills_fig.update_traces(marker_color=colors['danger'])
    kills_fig.update_xaxes(title_text='Username')
    kills_fig.update_yaxes(title_text='Kills')

    best_hit_fig = px.bar(df_users, x='username', y='best_hit', title='Best Hit per User')
    best_hit_fig.update_layout(graph_layout)
    best_hit_fig.update_traces(marker_color=colors['success'])
    best_hit_fig.update_xaxes(title_text='Username')
    best_hit_fig.update_yaxes(title_text='Best Hit')

    games_played_fig = px.bar(df_user_stats, x='username', y='games_played', title='Games Played per User')
    games_played_fig.update_layout(graph_layout)
    games_played_fig.update_traces(marker_color=colors['warning'])
    games_played_fig.update_xaxes(title_text='Username')
    games_played_fig.update_yaxes(title_text='Games Played')

    user_stats_columns = [
        {"name": "Username", "id": "username"},
        {"name": "Games Played", "id": "games_played"},
        {"name": "Total Kills", "id": "total_kills"},
        {"name": "Best Hit", "id": "best_hit"},
        {"name": "Wins", "id": "wins"}
    ]
    recent_games_columns = [
        {"name": "Game ID", "id": "id"},
        {"name": "Created At", "id": "created_at"},
        {"name": "Winner", "id": "winner"},
        {"name": "Total Participants", "id": "total_participants"}
    ]

    return (kills_fig, best_hit_fig, games_played_fig,
            df_user_stats.to_dict('records'), user_stats_columns,
            df_recent_games.to_dict('records'), recent_games_columns)

if __name__ == '__main__':
    app.run_server(debug=True)