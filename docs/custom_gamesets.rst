Creating Custom Game Sets
=============================================

To enhance your Battle Royale game experience, you can create custom sets of weapons and events. This section will guide you on how to structure your JSON files to integrate new content into the game.

**Creating balanced custom sets** is essential for a fair and engaging gameplay experience. Weapons and events are randomly selected and applied during the game, much like drawing cards from a shuffled deck. Ensure your custom sets are balanced to maintain the excitement and fairness of each match.

Note that the minimum number of weapons and events should be proportional to the number of participants per game. Larger games require more diverse sets to ensure a balanced and dynamic experience.

Custom Weapons
---------------

Create a JSON file for your weapons. Each weapon should have a `name` and `damage`. Here’s a sample structure for `weapons.json`:

.. code-block:: json
    {
        "name": "Rusty Dagger",
        "damage": 6
    },
    {
        "name": "Steel Longsword",
        "damage": 8
    }
    // Add more weapons as needed
    

Custom Events
---------------

Create a JSON file this time for your events. Each event should include a `name`, `bonus`, and `messages`. You can include one or more messages related to the event to give more variability to the same event. Here’s a sample structure for events.json:

.. code-block:: json
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