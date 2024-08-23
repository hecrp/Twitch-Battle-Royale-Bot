# Twitch Battle Royale Bot

## Overview

This is a Python-based Twitch bot that hosts a simulated battle royale between chat users. Once activated, up to 30 participants by default can join the battle. When the game is ready and started, two random participants face off every few seconds in an epic DnD-style dice roll battle. But wait! Random events can also spawn between battles, applying benefitial or detrimental bonuses that can change the course of a random participant's next fight. Battle Royale fights and events continue until only one user remains, who is declared the winner. The bot also tracks kills and the highest dice roll for each participant.

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
   cd Twitch-Battle-Royale-Bot```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    Set up your environment variables:

3. Modify bot.py and add your Twitch token, channel name, and admin username. Also check the seting for time elapsed between events and maximum number of participans:

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


### Usage

Check ttv_battleroyale/sample_game_assets.py for sample weapons and events details.

!activar: Activates the battle royale (admin only).

!apuntar: Joins the battle royale.

!autofill: If the game isn't full yet, fill the remaining spaces with sample users (admin only).

!wipe: Cleans the participants list (admin only).

!empezar: Starts the battle royale (admin only).


### Contributing
Feel free to fork this repository and submit pull requests.

### License
This project is licensed under the MIT License.
