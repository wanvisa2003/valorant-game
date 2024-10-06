# import dash
# from dash import dcc, html
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output

# # Initialize the Dash app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# # Sample data for the agents
# agents = [
#     {'name': 'Astra', 'role': 'Controller', 'img': './assets/astra.png'},
#     {'name': 'Breach', 'role': 'Initiator', 'img': './assets/breach.png'},
#     {'name': 'Brimstone', 'role': 'Controller', 'img': './assets/brimstone.png'},
#     {'name': 'Chamber', 'role': 'Sentinel', 'img': './assets/chamber.png'},
#     {'name': 'Clove', 'role': 'Controller', 'img': './assets/clove.png'},
#     {'name': 'Cypher', 'role': 'Sentinel', 'img': './assets/cypher.png'},
#     {'name': 'Deadlock', 'role': 'Sentinel', 'img': './assets/deadlock.png'},
#     {'name': 'Fade', 'role': 'Initiator', 'img': './assets/fade.png'},
#     {'name': 'Gekko', 'role': 'Initiator', 'img': './assets/gekko.png'},
#     {'name': 'Harbor', 'role': 'Controller', 'img': './assets/harbor.png'},
#     {'name': 'Iso', 'role': 'Duelist', 'img': './assets/iso.png'},
#     {'name': 'Jett', 'role': 'Duelist', 'img': './assets/jett.png'},
#     {'name': 'KAY/O', 'role': 'Initiator', 'img': './assets/kayo.png'},
#     {'name': 'Killjoy', 'role': 'Sentinel', 'img': './assets/killjoy.png'},
#     {'name': 'Neon', 'role': 'Duelist', 'img': './assets/neon.png'},
#     {'name': 'Omen', 'role': 'Controller', 'img': './assets/omen.png'},
#     {'name': 'Phoenix', 'role': 'Duelist', 'img': './assets/phoenix.png'},
#     {'name': 'Raze', 'role': 'Duelist', 'img': './assets/raze.png'},
#     {'name': 'Reyna', 'role': 'Duelist', 'img': './assets/reyna.png'},
#     {'name': 'Sage', 'role': 'Sentinel', 'img': './assets/sage.png'},
#     {'name': 'Skye', 'role': 'Initiator', 'img': './assets/skye.png'},
#     {'name': 'Sova', 'role': 'Initiator', 'img': './assets/sova.png'},
#     {'name': 'Viper', 'role': 'Controller', 'img': './assets/viper.png'},
#     {'name': 'Vyse', 'role': 'Sentinel', 'img': './assets/vyse.png'},
#     {'name': 'Yoru', 'role': 'Duelist', 'img': './assets/yoru.png'}
# ]

# maps = {
#     'Ascent': './assets/ascent.png',
#     'Bind': './assets/bind.png',
#     'Haven': './assets/haven.png',
#     'Split': './assets/split.png',
#     'Breeze': './assets/breeze.png',
#     'Fracture': './assets/fracture.png',
#     'Icebox': './assets/icebox.png',
#     'Sunset': './assets/sunset.png',
#     'Lotus': './assets/lotus.png',
#     'Pearl': './assets/pearl.png',
# }

# # Function to create agent selection dropdowns
# def create_agent_dropdown(team_id, agent_num):
#     return dcc.Dropdown(
#         id=f'agent-dropdown-{team_id}-{agent_num}',
#         options=[{'label': agent['name'], 'value': i} for i, agent in enumerate(agents)],
#         value=0,  # Default selected agent
#         style={'width': '80%', 'margin': 'auto', 'margin-bottom': '10px'}
#     )

# # Layout for the team agent selection and images
# def create_team_layout(team_id):
#     return html.Div([  
#         html.H3(f"TEAM {team_id.upper()}", style={'text-align': 'center'}),
#         html.Div(
#             style={'display': 'flex', 'justify-content': 'space-around', 'padding': '20px'},
#             children=[
#                 html.Div(style={'text-align': 'center', 'width': '190px'}, children=[  # Added 'width' to control layout size
#                     create_agent_dropdown(team_id, i),  # Dropdown is placed on top
#                     html.Img(id=f'agent-image-{team_id}-{i}', style={'width': '150px', 'height': '190px', 'margin-top': '10px'}),
#                     html.P(id=f'agent-name-{team_id}-{i}', style={'color': 'white', 'margin': '5px 0'}),
#                     html.P(id=f'agent-role-{team_id}-{i}', style={'color': 'gray'})
#                 ]) for i in range(5)
#             ]
#         )
#     ], style={'margin-bottom': '20px'})



# app.layout = html.Div(style={'background-color': 'black', 'color': 'white', 'padding': '20px'}, children=[
#     # Team A Layout
#     create_team_layout('teamA'),
    
#     # Team B Layout
#     create_team_layout('teamB'),

#     # Map selection
#     html.Div([
#         html.P("Select map you want to play:", style={'text-align': 'center'}),
#         dcc.Dropdown(
#             id='map-dropdown',
#             options=[{'label': map_name, 'value': map_name} for map_name in maps],
#             value='Ascent',  # Default map
#             style={'width': '50%', 'margin': 'auto'}
#         ),
#         html.Img(id='map-image', src=maps['Ascent'], style={'width': '600px', 'height': '300px', 'margin': 'auto', 'display': 'block', 'margin-top': '20px'})
#     ], style={'text-align': 'center', 'margin-top': '20px'}),
# ])

# # Callbacks

# # Callback to update agent images and names/roles for Team A and Team B
# @app.callback(
#     [Output(f'agent-image-teamA-{i}', 'src') for i in range(5)] +
#     [Output(f'agent-name-teamA-{i}', 'children') for i in range(5)] +
#     [Output(f'agent-role-teamA-{i}', 'children') for i in range(5)] +
#     [Output(f'agent-image-teamB-{i}', 'src') for i in range(5)] +
#     [Output(f'agent-name-teamB-{i}', 'children') for i in range(5)] +
#     [Output(f'agent-role-teamB-{i}', 'children') for i in range(5)],
#     [Input(f'agent-dropdown-teamA-{i}', 'value') for i in range(5)] +
#     [Input(f'agent-dropdown-teamB-{i}', 'value') for i in range(5)]
# )
# def update_agent_images(*selected_agents):
#     teamA_images = []
#     teamA_names = []
#     teamA_roles = []
    
#     teamB_images = []
#     teamB_names = []
#     teamB_roles = []

#     for i in range(5):
#         # Team A
#         agent = agents[selected_agents[i]]
#         teamA_images.append(agent['img'])
#         teamA_names.append(agent['name'])
#         teamA_roles.append(agent['role'])

#         # Team B
#         agent = agents[selected_agents[i + 5]]
#         teamB_images.append(agent['img'])
#         teamB_names.append(agent['name'])
#         teamB_roles.append(agent['role'])

#     return teamA_images + teamA_names + teamA_roles + teamB_images + teamB_names + teamB_roles

# # Callback to update the map image based on dropdown selection
# @app.callback(
#     Output('map-image', 'src'),
#     Input('map-dropdown', 'value')
# )
# def update_map_image(selected_map):
#     return maps[selected_map]

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import random

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Sample data for the agents
agents = [
    {'name': 'Astra', 'role': 'Controller', 'img': './assets/astra.png'},
    {'name': 'Breach', 'role': 'Initiator', 'img': './assets/breach.png'},
    {'name': 'Brimstone', 'role': 'Controller', 'img': './assets/brimstone.png'},
    {'name': 'Chamber', 'role': 'Sentinel', 'img': './assets/chamber.png'},
    {'name': 'Clove', 'role': 'Controller', 'img': './assets/clove.png'},
    {'name': 'Cypher', 'role': 'Sentinel', 'img': './assets/cypher.png'},
    {'name': 'Deadlock', 'role': 'Sentinel', 'img': './assets/deadlock.png'},
    {'name': 'Fade', 'role': 'Initiator', 'img': './assets/fade.png'},
    {'name': 'Gekko', 'role': 'Initiator', 'img': './assets/gekko.png'},
    {'name': 'Harbor', 'role': 'Controller', 'img': './assets/harbor.png'},
    {'name': 'Iso', 'role': 'Duelist', 'img': './assets/iso.png'},
    {'name': 'Jett', 'role': 'Duelist', 'img': './assets/jett.png'},
    {'name': 'KAY/O', 'role': 'Initiator', 'img': './assets/kayo.png'},
    {'name': 'Killjoy', 'role': 'Sentinel', 'img': './assets/killjoy.png'},
    {'name': 'Neon', 'role': 'Duelist', 'img': './assets/neon.png'},
    {'name': 'Omen', 'role': 'Controller', 'img': './assets/omen.png'},
    {'name': 'Phoenix', 'role': 'Duelist', 'img': './assets/phoenix.png'},
    {'name': 'Raze', 'role': 'Duelist', 'img': './assets/raze.png'},
    {'name': 'Reyna', 'role': 'Duelist', 'img': './assets/reyna.png'},
    {'name': 'Sage', 'role': 'Sentinel', 'img': './assets/sage.png'},
    {'name': 'Skye', 'role': 'Initiator', 'img': './assets/skye.png'},
    {'name': 'Sova', 'role': 'Initiator', 'img': './assets/sova.png'},
    {'name': 'Viper', 'role': 'Controller', 'img': './assets/viper.png'},
    {'name': 'Vyse', 'role': 'Sentinel', 'img': './assets/vyse.png'},
    {'name': 'Yoru', 'role': 'Duelist', 'img': './assets/yoru.png'}
]

maps = {
    'Ascent': './assets/ascent.png',
    'Bind': './assets/bind.png',
    'Haven': './assets/haven.png',
    'Split': './assets/split.png',
    'Breeze': './assets/breeze.png',
    'Fracture': './assets/fracture.png',
    'Icebox': './assets/icebox.png',
    'Sunset': './assets/sunset.png',
    'Lotus': './assets/lotus.png',
    'Pearl': './assets/pearl.png',
}

# Function to create agent selection dropdowns
def create_agent_dropdown(team_id, agent_num, disabled=True):
    return dcc.Dropdown(
        id=f'agent-dropdown-{team_id}-{agent_num}',
        options=[{'label': agent['name'], 'value': i} for i, agent in enumerate(agents)],
        value=0,
        style={'width': '80%', 'margin': 'auto', 'margin-bottom': '10px'},
        disabled=disabled  # Set dropdown to be disabled by default
    )

# Layout for the team agent selection and images
def create_team_layout(team_id, disabled=True):
    return html.Div([  
        html.H3(f"TEAM {team_id.upper()}", style={'text-align': 'center'}),
        html.Div(
            style={'display': 'flex', 'justify-content': 'space-around', 'padding': '20px'},
            children=[
                html.Div(style={'text-align': 'center', 'width': '190px'}, children=[
                    create_agent_dropdown(team_id, i, disabled=disabled),
                    html.Img(id=f'agent-image-{team_id}-{i}', style={'width': '150px', 'height': '190px', 'margin-top': '10px'}),
                    html.P(id=f'agent-name-{team_id}-{i}', style={'color': 'white', 'margin': '5px 0'}),
                    html.P(id=f'agent-role-{team_id}-{i}', style={'color': 'gray'})
                ]) for i in range(5)
            ]
        )
    ], style={'margin-bottom': '20px'})

# Layout
app.layout = html.Div(style={'background-color': 'black', 'color': 'white', 'padding': '20px'}, children=[
    html.Link(rel='icon', type='image/png', href='./assets/icon.png'),
    
    # Main title for the application
    html.H1("VALORANT GAME", style={'text-align': 'center', 'color': '#c9242b', 'margin-bottom': '40px'}),
    
    html.Div([
        html.P("Select the map you want to play:", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='map-dropdown',
            options=[{'label': map_name, 'value': map_name} for map_name in maps],
            value='Ascent',
            style={'width': '50%', 'margin': 'auto'}
        ),
        html.Img(id='map-image', src=maps['Ascent'], style={'width': '750px', 'height': '300px', 'margin': 'auto', 'display': 'block', 'margin-top': '20px'})
    ], style={'text-align': 'center', 'margin-top': '25px', 'margin-bottom': '55px' }),
    
    create_team_layout('A'),
    create_team_layout('B'),
    
    html.Div([
        html.Button(
            'Predict', 
            id='predict-button', 
            n_clicks=0, 
            style={
                'margin-top': '20px',
                'border-radius': '7px',  
                'width': '200px',         
                'padding': '10px',        
                'background-color': 'white',  
                'color': 'black',         
                'font-size': '16px'       
            }
        ),
        html.H3(id='prediction-result', style={'text-align': 'center', 'margin-top': '20px'}),
    ], style={'text-align': 'center'})
])

# Callback to update agent images and names/roles for both teams
@app.callback(
    [Output(f'agent-image-A-{i}', 'src') for i in range(5)] +
    [Output(f'agent-name-A-{i}', 'children') for i in range(5)] +
    [Output(f'agent-role-A-{i}', 'children') for i in range(5)] +
    [Output(f'agent-image-B-{i}', 'src') for i in range(5)] +
    [Output(f'agent-name-B-{i}', 'children') for i in range(5)] +
    [Output(f'agent-role-B-{i}', 'children') for i in range(5)],
    [Input(f'agent-dropdown-A-{i}', 'value') for i in range(5)] +
    [Input(f'agent-dropdown-B-{i}', 'value') for i in range(5)]
)
def update_agent_images(*selected_agents):
    teamA_images, teamA_names, teamA_roles = [], [], []
    teamB_images, teamB_names, teamB_roles = [], [], []

    for i in range(5):
        agent_A = agents[selected_agents[i]]
        teamA_images.append(agent_A['img'])
        teamA_names.append(agent_A['name'])
        teamA_roles.append(agent_A['role'])

        agent_B = agents[selected_agents[i + 5]]
        teamB_images.append(agent_B['img'])
        teamB_names.append(agent_B['name'])
        teamB_roles.append(agent_B['role'])

    return teamA_images + teamA_names + teamA_roles + teamB_images + teamB_names + teamB_roles

# Callback to update the map image based on dropdown selection
@app.callback(
    Output('map-image', 'src'),
    Input('map-dropdown', 'value')
)
def update_map_image(selected_map):
    return maps[selected_map]

# Callback to enable agent dropdowns after selecting a map
@app.callback(
    [Output(f'agent-dropdown-A-{i}', 'disabled') for i in range(5)] +
    [Output(f'agent-dropdown-B-{i}', 'disabled') for i in range(5)],
    Input('map-dropdown', 'value')
)
def enable_agent_dropdowns(selected_map):
    return [False] * 10  # Enable all dropdowns when a map is selected

# Function to randomly predict the winner
def predict_winner(teamA_agents, teamB_agents, selected_map):
    return random.choice(['Team A', 'Team B'])

# Callback to predict and display the winner
@app.callback(
    Output('prediction-result', 'children'),
    Input('predict-button', 'n_clicks'),
    [Input(f'agent-dropdown-A-{i}', 'value') for i in range(5)] + 
    [Input(f'agent-dropdown-B-{i}', 'value') for i in range(5)] + 
    [Input('map-dropdown', 'value')]
)
def update_prediction(n_clicks, *selected_agents_and_map):
    if n_clicks > 0:  # Only predict after the button is clicked
        teamA_agents = selected_agents_and_map[:5]
        teamB_agents = selected_agents_and_map[5:10]
        selected_map = selected_agents_and_map[10]
        
        winner = predict_winner(teamA_agents, teamB_agents, selected_map)
        return f'{winner} win!'
    return ''  # No prediction result until button is clicked

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
