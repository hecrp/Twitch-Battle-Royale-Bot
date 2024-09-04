import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
from models import get_users, get_games, get_user_stats, get_recent_games

# Use a modern Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Custom CSS for additional styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Twitch Battle Royale Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #f8f9fa;
                font-family: 'Roboto', sans-serif;
            }
            .card {
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease-in-out;
            }
            .card:hover {
                box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
                transform: translateY(-5px);
            }
            .table th {
                background-color: #007bff;
                color: white;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Color scheme
colors = {
    'background': '#f8f9fa',
    'text': '#212529',
    'primary': '#007bff',
    'secondary': '#6c757d',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545'
}

# Graph layout
graph_layout = {
    'plot_bgcolor': colors['background'],
    'paper_bgcolor': colors['background'],
    'font': {'color': colors['text']},
    'title': {'font': {'size': 20, 'color': colors['primary']}},
    'xaxis': {'title': {'font': {'size': 14, 'color': colors['secondary']}}},
    'yaxis': {'title': {'font': {'size': 14, 'color': colors['secondary']}}},
}

def create_header():
    return dbc.Card(
        dbc.CardBody([
            html.H1("Twitch Battle Royale Dashboard", className="text-center text-primary mb-4"),
            html.P("Real-time statistics and game data for Twitch Battle Royale", className="text-center text-muted"),
        ]),
        className="mb-4"
    )

def create_graphs():
    user_stats = pd.DataFrame(get_user_stats())
    
    kills_graph = dcc.Graph(
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
        dbc.Col(dbc.Card(dbc.CardBody(kills_graph)), width=12, lg=4, className="mb-4"),
        dbc.Col(dbc.Card(dbc.CardBody(best_hit_graph)), width=12, lg=4, className="mb-4"),
        dbc.Col(dbc.Card(dbc.CardBody(games_played_graph)), width=12, lg=4, className="mb-4")
    ])

def create_tables():
    return dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H3("User Statistics", className="text-center")),
            dbc.CardBody(
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
                        'color': 'white',
                        'fontWeight': 'bold',
                    },
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px',
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ],
                    style_table={'overflowX': 'auto'},
                    sort_action='native',
                    filter_action='native',
                    page_action='native',
                    page_current=0,
                    page_size=10,
                )
            )
        ]), width=12, lg=6, className="mb-4"),
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H3("Recent Games", className="text-center")),
            dbc.CardBody(
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
                        'color': 'white',
                        'fontWeight': 'bold',
                    },
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px',
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ],
                    style_table={'overflowX': 'auto'},
                    sort_action='native',
                    page_action='native',
                    page_current=0,
                    page_size=5,
                )
            )
        ]), width=12, lg=6, className="mb-4")
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
], fluid=True, className="py-4")

@app.callback(
    [dash.Output('user-stats-table', 'data'),
     dash.Output('recent-games-table', 'data')],
    [dash.Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    user_stats = get_user_stats()
    recent_games = get_recent_games()
    return user_stats, recent_games

if __name__ == '__main__':
    app.run_server(debug=True)