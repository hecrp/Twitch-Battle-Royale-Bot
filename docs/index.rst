Welcome to Battle Royale Bot's documentation!
=============================================

Introduction
---------------

Welcome to Twitch Battle Royale Bot documentation. Here you will find Setup and Usage Guides and also the complete API Reference for this Python package.

Twitch Battle Royale Bot hosts a simulated battle royale between Twitch chat users. Once activated, up to 30 participants by default can join the battle. When the game is ready and started, two random participants face off every few seconds in an epic DnD-style dice roll battle. But wait! Random events can also spawn between battles, applying benefitial or detrimental bonuses that can change the course of a random participant's next fight. Battle Royale fights and events continue until only one user remains, who is declared the winner. The bot also tracks kills and the highest dice roll for each participant.

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

*Admin only Commands*

- !activate: Activates the Battle Royale (allows users to join the game).
- !autofill: If the game isn't full, fills the remaining spaces with sample users.
- !fight: Starts the Battle Royale.
- !wipe: Clears the participants list.
- !expand {num}: Expands the current maximum number of participants by {num} free spots.
- !pause: Pauses an ongoing game.
- !resume: Resumes a paused game.

*User Commands*

- !join: Joins the Battle Royale.
- !seats: Shows the nomber of available spots for the next game.

API Reference
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules