import random
import asyncio

class Weapon:
    """
    Represents a weapon in the Battle Royale game.

    Attributes:
        name (str): The name of the weapon.
        dice (int): The type of dice used to determine damage (e.g., 6 for d6, 8 for d8).ss
    """

    def __init__(self, name, dice):
        """
        Initializes a new weapon with a name and a dice type.

        Args:
            name (str): The name of the weapon.
            dice (int): The dice type used for rolling damage.
        """
        self.name = name
        self.dice = dice

    def roll_damage(self):
        """
        Rolls the dice to determine the base damage.

        Returns:
            int: The damage rolled with the weapon's dice.
        """
        return random.randint(1, self.dice)
    
class Event:
    def __init__(self, name, damage_bonus, messages):
        """
        Base class representing an event that occurs between rounds.

        :param name: Name of the event.
        :param damage_bonus: Damage bonus provided by the event.
        :param messages: List of messages that represent the event when activated.
        """
        self.name = name
        self.damage_bonus = damage_bonus
        self.permanent_bonus = False
        self.activated = False
        self.affected_users = []
        self.messages = messages

    def select_participant(self, participants):
        """
        Selects a random participant from the list of participants.

        :param participants: List of participants.
        :return: A randomly selected participant.
        """
        if participants:
            selected = random.choice(participants)
            self.affected_users.append(selected)
            return selected
        return None

    def activate_event(self, participants):
        """
        Activates the event, selects a participant with a bonus of 0, and applies the effect.

        :param participants: List of participants.
        :return: Message from the activated event.
        """
        if not self.activated:
            eligible_participants = [p for p in participants if p.bonus == 0]
            
            if eligible_participants:
                affected = self.select_participant(eligible_participants)
                if affected:
                    self.activated = False
                    message = random.choice(self.messages).format(affected.name) + " BONUS: " + str(self.damage_bonus)
                    bonus = self.damage_bonus
                    permanent = self.permanent_bonus
                    event_title = self.name
                    return affected, event_title, message, bonus, permanent
            else:
                return None
        
        return None

    def reset_event(self):
        """
        Resets the event's state so it can be activated again.
        """
        self.activated = False
        self.affected_users = []

class Participant:
    """
    Represents a participant in the Battle Royale game.

    Attributes:
        name (str): The name of the participant.
        weapon (Weapon): The weapon assigned to the participant, or None if no weapon is assigned.s
        bonus (int): The bonus to apply when battling
        permanent_bonus (bool): Indicates if the current bonus is permanent
    """

    def __init__(self, name):
        """
        Initializes a new participant with a name and no weapon.

        Args:
            name (str): The name of the participant.
        """
        self.name = name
        self.weapon = None
        self.permanent_weapon = False
        self.bonus = 0
        self.permanent_bonus = False

    def assign_weapon(self, weapon):
        """
        Assigns a weapon to the participant if they don't already have one.

        Args:
            weapon (Weapon): The weapon to assign to the participant.
        """
        if not self.permanent_weapon:
            self.weapon = weapon

    def roll_damage(self):
        """
        Rolls the damage using the assigned weapon and applies the current bonus. Resets their bonus if not permanent

        Returns:
            int: The total damage rolled, including any bonuses.
        """
        if not self.weapon:
            return 0 
        base_damage = self.weapon.roll_damage()
        final_damage = base_damage + self.bonus
        if not self.permanent_bonus:
            self.bonus = 0
        return final_damage


class BattleRoyaleGame:
    """
    Manages the Battle Royale game, including participants and battle simulation.

    Attributes:
        participants (list): A list of current participants in the game.
        battle_log (list): A log of battles that have taken place.
        max_participants (int): The maximum number of participants allowed in the game.
        lock (asyncio.Lock): A lock to ensure thread-safe access to participants.
    """

    def __init__(self, weapons, events, max_participants=30):
        """
        Initializes the Battle Royale game.

        Args:
            max_participants (int): The maximum number of participants allowed in the game. Defaults to 10.
        """
        self.participants = []
        self.weapons = weapons
        self.events = events
        self.available_events = events.copy()
        self.event_probability = 75
        self.battle_log = []
        self.max_participants = max_participants
        self.lock = asyncio.Lock()

    async def add_participant(self, participant_name):
        """
        Adds a new participant to the game, ensuring no duplicates and within the limit.

        Args:
            participant_name (str): The name of the participant to add.

        Returns:
            bool: True if the participant was added, False otherwise.
        """
        async with self.lock:
            if any(p.name == participant_name for p in self.participants):
                return False
            if self.is_full():
                return False
            self.participants.append(Participant(participant_name))
            return True

    async def wipe(self):
        """
        Clears the list of participants and the battle log.

        Returns:
            bool: True when the wipe is complete.
        """
        async with self.lock:
            self.participants.clear()
            self.battle_log.clear()
            return True

    def is_full(self):
        """
        Checks if the maximum number of participants has been reached.

        Returns:
            bool: True if the game is full, False otherwise.
        """
        return len(self.participants) >= self.max_participants

    def is_ready_to_start(self):
        """
        Checks if there are enough participants to start the game.

        Returns:
            bool: True if the game can start, False otherwise.
        """
        return len(self.participants) > 1

    def simulate_battle(self):
        """
        Simulates a battle between two random participants.

        Returns:
            tuple: A tuple containing the winner's and loser's details, or None if there's a tie.
        """
        if len(self.participants) < 2:
            return None

        fighter1, fighter2 = random.sample(self.participants, 2)
        weapon1 = random.choice(self.weapons)
        weapon2 = random.choice(self.weapons)

        fighter1.assign_weapon(weapon1)
        fighter2.assign_weapon(weapon2)

        fighter1_bonus = fighter1.bonus
        fighter2_bonus = fighter2.bonus

        roll1 = fighter1.roll_damage()
        roll2 = fighter2.roll_damage()

        if roll1 > roll2:
            self.record_battle(fighter1, fighter2, roll1)
            return (fighter1.name, weapon1, roll1, fighter1_bonus), (fighter2.name, weapon2, roll2, fighter2_bonus)
        elif roll2 > roll1:
            self.record_battle(fighter2, fighter1, roll2)
            return (fighter2.name, weapon2, roll2, fighter2_bonus), (fighter1.name, weapon1, roll1, fighter1_bonus)
        else:
            return None
        
    def simulate_event(self):
        """
        Triggers a random event from the collection based on the given probability
        
        :return: Mensaje del evento o None si no se activó ningún evento.
        """
        if not self.available_events:
            self.available_events = self.events.copy()

        if random.randint(1, 100) <= self.event_probability:
            current_event = random.choice(self.available_events)
            event_result = current_event.activate_event(self.participants)
            
            if event_result:
                afectado, name, message, bonus, permanent = event_result
                afectado.bonus = bonus
                afectado.permanent_bonus = permanent
                self.available_events.remove(current_event)
                
                return name, message

        return None

    def record_battle(self, winner, loser, damage):
        """
        Records the result of a battle and removes the loser from the participant list.

        Args:
            winner (Participant): The participant who won the battle.
            loser (Participant): The participant who lost the battle.
            damage (int): The amount of damage dealt in the battle.
        """
        self.participants.remove(loser)
        self.battle_log.append((winner.name, loser.name, damage))

    def get_winner(self):
        """
        Returns the winner of the game if there is only one participant left.

        Returns:
            str or None: The name of the winner, or None if the game is not over.
        """
        if len(self.participants) == 1:
            return self.participants[0].name
        return None

    def get_stats(self):
        """
        Returns statistics of the battles, including kills and best hits.

        Returns:
            dict: A dictionary where keys are participant names and values are their stats.
        """
        stats = {}
        for winner, loser, damage in self.battle_log:
            if winner not in stats:
                stats[winner] = {'kills': 0, 'best_hit': 0}
            stats[winner]['kills'] += 1
            stats[winner]['best_hit'] = max(stats[winner]['best_hit'], damage)
        return stats