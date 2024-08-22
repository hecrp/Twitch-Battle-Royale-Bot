# Twitch Battle Royale Bot

## Overview

This is a Python-based Twitch bot that hosts a simulated battle royale between chat participants. Once activated, up to 10 participants can join the battle. After registration, the battle begins with two random participants facing off every 25 seconds in an epic DnD-style dice roll battle. The battle continues until only one user remains, who is declared the winner. The bot also tracks kills and the highest dice roll for each participant.

## Features

- Manual activation by the administrator.
- Allows up to 10 participants to join.
- Simulates a battle royale with dice rolls and random weapons.
- Tracks kills and the highest roll for each participant.
- Displays final stats after the battle concludes.

## Setup and Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/twitch-battle-royale-bot.git
   cd twitch-battle-royale-bot```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    Set up your environment variables:

3. Create a .env file in the root of the project and add your Twitch token, channel name, and admin username:

    ```makefile
    TOKEN=your_token_here
    CHANNEL=your_channel_here
    ADMIN=your_admin_here
    Run the bot:

4. Run the bot

    ```bash
    python bot_twitch.py


### Usage

!activar: Activates the battle royale (admin only).
!apuntar: Joins the battle royale.
!empezar: Starts the battle royale (admin only).

### Contributing
Feel free to fork this repository and submit pull requests.

### License
This project is licensed under the MIT License.