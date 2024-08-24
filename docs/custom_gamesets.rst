Creating Custom Game Sets
=============================================

To enhance your Battle Royale game experience, you can create custom sets of weapons and events. This section will guide you on how to structure your JSON files AND HOW to integrate your custom content into the game.

**Creating balanced custom sets** is essential for a fair and engaging gameplay experience. Weapons, events and questions are randomly selected and applied during the game, much like drawing cards from a shuffled deck. Ensure your custom sets are balanced to maintain the excitement and fairness of each match.

*Note that the minimum number of assets should be proportional to the number of participants per game. Larger games require more diverse sets to ensure a balanced and dynamic experience.*

Custom Weapons
---------------

Create a JSON file for your weapons. Each weapon should have a `name` and `damage`. Here’s a sample structure for `weapons.json`:

.. code-block:: json

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
    

Custom Events
---------------

Create a JSON file this time for your events. Each event should include a `name`, `damage_bonus`, and `messages`. You can include one or more messages related to the event to give more variability to the same event. Here’s a sample structure for events.json:

.. code-block:: json

    [
        {
            "name": "Blessing of the Ancients",
            "damage_bonus": 5,
            "messages": [
                "{} has been blessed by the Ancients! Their attacks are now more powerful.",
                "The Ancients smile upon {}. Their strength grows immensely!"
            ]
        },
        {
            "name": "Curse of the Fallen",
            "damage_bonus": -3,
            "messages": [
                "{} has been cursed by the fallen spirits. Their strength diminishes.",
                "The shadows of the fallen weigh heavy on {}. Their attacks are weakened."
            ]
        }
        // Add more events as needed
    ]

Custom Questions
----------------

Finally, create a JSON file for your questions. Each question should have  `question`, `answer` (ONE word), `correct_message` (a custom correct answer message), `prize` (positive integer bonus or `name` value of any weapon of your set) and `is_permanent` flag which specify if the prize is permanent. Here’s a sample structure for `questions.json`:

.. code-block:: json

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


Integrating Custom Sets
-----------------------

Save your custom `.json` files in the `ttv_battleroyale/game_assets/your_custom_set` directory.

Load Custom Sets: In `ttv_battleroyale/bot.py` (Line 19), change the game assets paths to your custom JSON files. For example:

.. code-block:: python

    #GAME ASSETS
    WEAPONS = 'game_assets/your_custom_set/weapons.json'
    EVENTS = 'game_assets/your_custom_set/events.json'
    EVENTS = 'game_assets/your_custom_set/questions.json'


By following these instructions, you can create and integrate your own custom sets of weapons and events, enhancing the variety and excitement of your game!