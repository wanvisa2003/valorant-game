import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import random
import tensorflow as tf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model

# Load CNN model
cnn_model = tf.keras.models.load_model('cnn_model.h5')

data = pd.read_csv('./data/data_clean.csv')


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

agent_mapping = {agent['name']: idx for idx, agent in enumerate(agents)}

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

map_mapping = {map_name: idx for idx, map_name in enumerate(maps.keys())}

map_encoder = LabelEncoder()
# Fit the encoder on the unique map names
map_encoder.fit(list(maps.keys()))

features = [
    'Score', 'Pick %', 'Dmg/Round', 'KDA',
    'Attacker Win %', 'Attacker KDA',
    'Defender Win %', 'Defender KDA',
    'A Pick %', 'A Defuse %', 
    'B Pick %', 'B Defuse %',
    'C Pick %', 'C Defuse %'
]

# Prepare the input data
input_data = data[features].values

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
        html.Img(id='map-image', src=maps['Ascent'], style={'width': '750px', 'height': '300px', 'margin': 'auto', 'display': 'block', 'margin-top': '20px'}),

        html.Div(id='agent-image-container', style={'text-align': 'center', 'margin-top': '20px'})
    ], style={'text-align': 'center', 'margin-top': '25px', 'margin-bottom': '55px'}),
    
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

@app.callback(
    Output('agent-image-container', 'children'),
    Input('map-dropdown', 'value')
)

def update_agent_images(selected_map):
    # Filter the data for the selected map
    filtered_data = data[data['Map'] == selected_map]
    
    # Remove duplicates based on the 'Agent' column to get unique agents
    unique_agents = filtered_data.drop_duplicates(subset='Agent')
    
    # Sort by Win % and select top 5 unique agents
    top_agents = unique_agents.nlargest(5, 'Win %')
    
    # Create image components for the agents
    agent_images = [
        html.Div([
            html.Img(src=f'./assets/{agent}.png', style={'width': '150px', 'height': '200px'}),
            html.P(f"{agent}: {win_rate:.3f}%", style={'text-align': 'center', 'color': 'white'})
        ], style={'display': 'inline-block', 'margin': '10px'})
        for agent, win_rate in zip(top_agents['Agent'], top_agents['Win %'])
    ]
    
    # Create the title component
    title = html.H3(f"Top 5 Unique Agents on {selected_map}", style={'text-align': 'center', 'margin-top': '50px', 'color': 'white'})
    
    # Combine the title and the images into one div
    return [title] + agent_images

# Callback to enable agent dropdowns after selecting a map
@app.callback(
    [Output(f'agent-dropdown-A-{i}', 'disabled') for i in range(5)] +
    [Output(f'agent-dropdown-B-{i}', 'disabled') for i in range(5)],
    Input('map-dropdown', 'value')
)
def enable_agent_dropdowns(selected_map):
    return [False] * 10  # Enable all dropdowns when a map is selected

# def predict_winner(teamA_agents, teamB_agents, selected_map):
#     return random.choice(['Team A', 'Team B'])

# # Callback to predict and display the winner
# @app.callback(
#     Output('prediction-result', 'children'),
#     Input('predict-button', 'n_clicks'),
#     [Input(f'agent-dropdown-A-{i}', 'value') for i in range(5)] + 
#     [Input(f'agent-dropdown-B-{i}', 'value') for i in range(5)] + 
#     [Input('map-dropdown', 'value')]
# )
# def update_prediction(n_clicks, *selected_agents_and_map):
#     if n_clicks > 0:  # Only predict after the button is clicked
#         teamA_agents = selected_agents_and_map[:5]
#         teamB_agents = selected_agents_and_map[5:10]
#         selected_map = selected_agents_and_map[10]
        
#         winner = predict_winner(teamA_agents, teamB_agents, selected_map)
#         return f'{winner} win!'
#     return ''  # No prediction result until button is clicked



def predict_winner(teamA_agents, teamB_agents, selected_map):
    # Prepare data for prediction (mock example, adapt this as per your actual data structure)
    teamA_features = np.array([agent_mapping[agents[i]['name']] for i in teamA_agents])
    teamB_features = np.array([agent_mapping[agents[i]['name']] for i in teamB_agents])
    
    # Encode the selected map
    map_feature = map_encoder.transform([selected_map])[0]
    
    # Combine into the feature set for prediction
    input_features = np.hstack([features])
    
    # Reshape input to the model's expected input dimensions (assuming a single sample)
    input_features = input_features.reshape((1, -1))
    
    # Predict using the CNN model
    prediction = cnn_model.predict(input_features)
    
    # Use softmax output to determine the winner
    winner = 'Team A' if prediction[0][0] > 0.5 else 'Team B'
    
    return winner


# Function to prepare input data for prediction
def prepare_input_data(teamA_agents, teamB_agents, selected_map):
    print("Preparing input data...")

    # Encode Team A agents
    try:
        teamA_encoded = [agent_mapping[agent] for agent in teamA_agents]
        print("Team A Encoded:", teamA_encoded)
    except KeyError as e:
        print(f"KeyError: '{e}' not found in agent mapping for Team A.")
        return None

    # Encode Team B agents
    try:
        teamB_encoded = [agent_mapping[agent] for agent in teamB_agents]
        print("Team B Encoded:", teamB_encoded)
    except KeyError as e:
        print(f"KeyError: '{e}' not found in agent mapping for Team B.")
        return None

    # Encode the selected map
    try:
        encoded_map = map_encoder.transform([selected_map])
        print("Encoded Map:", encoded_map)
    except ValueError as e:
        print(f"ValueError: {e}. Check if the selected map is valid.")
        return None

    # Combine encoded data
    input_data = teamA_encoded + teamB_encoded + encoded_map.tolist()[0]  # Flatten the array
    print("Combined Input Data (before padding):", input_data)

    # Ensure the input data has the correct length
    while len(input_data) < 416:
        input_data.append(0)

    print("Combined Input Data (after padding):", input_data)

    return np.array(input_data).reshape(1, -1)  # Reshape to (1, 416)

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
        
        # Predict the winner
        winner = predict_winner(teamA_agents, teamB_agents, selected_map)
        
        return f"Predicted Winner: {winner}"
    return ""

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)