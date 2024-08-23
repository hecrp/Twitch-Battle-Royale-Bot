# Twitch Battle Royale Bot

## Overview

Twitch Battle Royale Bot hosts a simulated battle royale between Twitch chat users. Once activated, up to 30 participants by default can join the battle. When the game is ready and started, two random participants face off every few seconds in an epic DnD-style dice roll battle. But wait! Random events can also spawn between battles, applying benefitial or detrimental bonuses that can change the course of a random participant's next fight. Battle Royale fights and events continue until only one user remains, who is declared the winner. The bot also tracks kills and the highest dice roll for each participant.

[Check the documentation](https://twitch-battle-royale-bot.readthedocs.io) for more info!

[Game instructions in Spanish (gh-pages)](https://hecrp.github.io/Twitch-Battle-Royale-Bot/)

## Features

- Manual activation by the administrator.
- Allows up to a given maximum number of participants to join.
- Simulates a battle royale with dice rolls and random weapons.
- Simulate random events between fights.
- Tracks kills and the highest roll for each participant.

## Setup and Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/hecrp/Twitch-Battle-Royale-Bot.git
   cd Twitch-Battle-Royale-Bot

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt

3. Modify bot.py and add your Twitch token, channel name, and admin username. Also tune the default values to modify elapsed time between events and maximum number of participans:

    ```python
    TOKEN = 'TOKEN'
    CHANNEL = 'CHANNEL'
    ADMIN = 'ADMIN'
    #MINIMUM SLEEP TIME FOR TESTING PURPOSES. MODIFY AS NEEDED
    EVENT_SLEEP = 1
    #MAXIMUM PARTICIPANTS PER GAME
    MAX_PARTICIPANTS = 30


4. Run the bot

    ```bash
    python bot_twitch.py

### Install and run with Docker (Testing)

1. Build the Docker image using the provided Dockerile:

    ```bash
    docker build -t twitch-battle-royale-bot .

2. Run the container. Remember to set up your port and environment variables in the command. To enable this mode, replace the credentials assignment at bot.py

    ```bash
    docker run -d \ 
    -p 3000:3000 \ 
    --name twitch-bot \ 
    -e TOKEN=your_token \ 
    -e CHANNEL=your_channel \ 
    -e ADMIN=your_admin twitch-battle-royale-bot 

### Usage

Check ttv_battleroyale/sample_game_assets.py for sample weapons and events details.

#### Admin Commands

- `!activate`: Activates the Battle Royale (allows users to join the game).
- `!autofill`: If the game isn't full, fills the remaining spaces with sample users.
- `!fight`: Starts the Battle Royale.
- `!wipe`: Clears the participants list.
- `!expand {num}`: Expands the current maximum number of participants by {num} free spots.
- `!pause`: Pauses an ongoing game.
- `!resume`: Resumes a paused game.

#### User Commands

- `!join`: Joins the Battle Royale.
- `!seats`: Shows the nomber of available spots for the next game.

### Contributing
Feel free to fork this repository and submit pull requests.

### License
This project is licensed under the MIT License.
