# Twitch Battle Royale Bot

## Overview

Twitch Battle Royale Bot hosts a simulated battle royale between Twitch chat users. Once activated, up to 30 participants by default can join the battle. When the game is ready and started, two random participants face off every few seconds in an epic DnD-style dice roll battle. But wait! Random events can also spawn between battles, applying benefitial or detrimental bonuses that can change the course of a random participant's next fight. Battle Royale fights and events continue until only one user remains, who is declared the winner. The bot also tracks kills and the highest dice roll for each participant.

Check the [documentation](https://twitch-battle-royale-bot.readthedocs.io) for more info!

Project description and instructions in English (gh-pages) [here](https://hecrp.github.io/Twitch-Battle-Royale-Bot/)

## Features

- Manual activation by the administrator.
- Allows up to a given maximum number of participants to join.
- Simulates a battle royale with dice rolls and random weapons.
- Simulate random events and quiz challenges between fights.
- Tracks kills and the highest roll for each participant to build the final ranking.

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

3. Modify `bot.py` (Line 15) and add your Twitch token, channel name, and admin username. Also tune the default values to modify elapsed time between events and maximum number of participants:

    ```python
    TOKEN = 'TOKEN'
    CHANNEL = 'CHANNEL'
    ADMIN = 'ADMIN'
    # ..
    # OPTIONAL: CHANGE THE GAME ASSETS PATHS
    #..
    #MINIMUM SLEEP TIME FOR TESTING PURPOSES. MODIFY AS NEEDED
    EVENT_SLEEP = 1
    FIGHT_SLEEP = 1
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
    -e TOKEN='your_token' \ 
    -e CHANNEL='your_channel' \ 
    -e ADMIN='your_admin' twitch-battle-royale-bot 

## Usage

### Admin Commands

- `!activate`: Activates the Battle Royale (allows users to join the game).
- `!autofill`: If the game isn't full, fills the remaining spaces with sample users.
- `!fight`: Starts the Battle Royale.
- `!wipe`: Clears the participants list.
- `!expand {num}`: Expands the current maximum number of participants by {num} free spots.
- `!pause`: Pauses an ongoing game.
- `!resume`: Resumes a paused game.

### User Commands

- `!join`: Joins the Battle Royale.
- `!seats`: Shows the nomber of available spots for the next game.
- `!answer {word}`: (Only enabled under special conditions) Gives a one word answer for the given question.
- `!challenge {user}`: (Only enabled under special conditions) The current challenger can fight any other alive user with this command.

## Creating Custom Game Sets
To enhance your Battle Royale game experience, you can create custom sets of weapons and events. This section will guide you on how to structure your JSON files and how to integrate your custom content into the game.

**Creating balanced custom sets** is essential for a fair and engaging gameplay experience. Weapons, events and questions are randomly selected and applied during the game, much like drawing cards from a shuffled deck. Ensure your custom sets are balanced to maintain the excitement and fairness of each match.

*Note that the minimum number of assets should be proportional to the number of participants per game. Larger games require more diverse sets to ensure a balanced and dynamic experience.*

### Custom Weapons
Create a JSON file for your weapons. Each weapon should have a `name` and `damage`. Here’s a sample structure for `weapons.json`:

```JSON
[
    {
        "name": "Rusty Dagger",
        "damage": 6
    },
    {
        "name": "Steel Longsword",
        "damage": 8
    }
    // Add more weapons as needed
]
```

### Custom Events
Create a JSON file this time for your events. Each event should include a `name`, `bonus`, and `messages`. You can include one or more messages related to the event to give more variability to the same event. Here’s a sample structure for `events.json`:

```JSON
[
    {
        "name": "Blessing of the Ancients",
        "bonus": 5,
        "messages": [
            "{} has been blessed by the Ancients! Their attacks are now more powerful.",
            "The Ancients smile upon {}. Their strength grows immensely!"
        ]
    },
    {
        "name": "Curse of the Fallen",
        "bonus": -3,
        "messages": [
            "{} has been cursed by the fallen spirits. Their strength diminishes.",
            "The shadows of the fallen weigh heavy on {}. Their attacks are weakened."
        ]
    }
    // Add more events as needed
]
```

### Custom Questions

Finally, create a JSON file for your questions. Each question should have  `question`, `answer` (ONE word), `correct_message` (a custom correct answer message), `prize` (positive integer bonus or `name` value of any weapon of your set) and `is_permanent` flag which specify if the prize is permanent. Here’s a sample structure for `questions.json`:

```JSON
[
    {
        "question": "I slither without a body, whispering secrets that drive men mad. What am I?",
        "answer": "shadow",
        "correct_message": "A shadow, indeed. It slithers without form, whispering madness into the minds of the unwary.",
        "prize": 1,
        "is_permanent": false
    },
    {
        "question": "I am not alive, yet I grow; I do not breathe, yet I consume. What am I?",
        "answer": "fire",
        "correct_message": "Fire, a living paradox. It grows, consumes, and yet is not truly alive.",
        "prize": "Eldritch Flame",
        "is_permanent": true
    }
    // Add more questions as needed
]
```

### Integrating Custom Sets

Save your custom `.json` files in the `ttv_battleroyale/game_assets/your_custom_set` directory.

Load Custom Sets: In `ttv_battleroyale/bot.py` (Line 19), change the game assets paths to your custom JSON files. For example:

```python
#GAME ASSETS
WEAPONS = 'game_assets/your_custom_set/weapons.json'
EVENTS = 'game_assets/your_custom_set/events.json'
EVENTS = 'game_assets/your_custom_set/questions.json'
```

By following these instructions, you can create and integrate your own custom sets of weapons and events, enhancing the variety and excitement of your game!

## Contributing
Feel free to fork this repository and submit pull requests.

## License
This project is licensed under the MIT License.
