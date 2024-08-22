Welcome to Battle Royale Bot's documentation!
=============================================

Introduction
---------------

This is a Python-based Twitch bot that hosts a simulated battle royale between chat users. Once activated, up to 30 participants by default can join the battle. When the game is ready and started, two random participants facing off every few seconds in an epic DnD-style dice roll battle. But wait! Random events can also spawn between battles, applying benefitial or detrimental bonuses that can change the course of a random participant's next fight. Battle Royale fights and events continue until only one user remains, who is declared the winner. The bot also tracks kills and the highest dice roll for each participant.

Key Features
------------

- Manual activation by the administrator.
- Allows up to a given maximum number of participants to join.
- Simulates a battle royale with dice rolls and random weapons.
- Simulate random events between fights.
- Tracks kills and the highest roll for each participant.

Setup and Installation
======================

Prerequisites
--------------

- Python 3.x
- pip (Python package installer)

Installation
------------

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/hecrp/Twitch-Battle-Royale-Bot.git
      cd Twitch-Battle-Royale-Bot

2. Install the required dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

3. Set up your environment variables:

   Modify `bot.py` and add your Twitch token, channel name, and admin username. Also check the settings for time elapsed between events and maximum number of participants:

   .. code-block:: python

      TOKEN = 'TOKEN'
      CHANNEL = 'CHANNEL'
      ADMIN = 'ADMIN'
      # MINIMUM SLEEP TIME FOR TESTING PURPOSES. MODIFY AS NEEDED
      EVENT_SLEEP = 1
      # MAXIMUM PARTICIPANTS PER GAME
      MAX_PARTICIPANTS = 30

4. Run the bot:

   .. code-block:: bash

      python bot_twitch.py

Usage
------

Check `ttv_battleroyale/sample_game_assets.py` for sample weapons and events details.

- **!activar**: Activates the battle royale (admin only).
- **!apuntar**: Joins the battle royale.
- **!autofill**: If the game isn't full yet, fill the remaining spaces with sample users (admin only).
- **!wipe**: Cleans the participants list (admin only).
- **!empezar**: Starts the battle royale (admin only).

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules