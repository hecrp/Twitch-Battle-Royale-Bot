import random
import asyncio
import json

class Weapon:
    """Represents a weapon in the Battle Royale game.
    """

    def __init__(self, name, dice):
        """
        Initialize a new weapon with a name and a dice type.

        Args:
            name (str): The name of the weapon.
            dice (int): The dice type used for rolling damage.
        """
        self.name = name
        self.dice = dice

    def roll_damage(self):
        """
        Roll the dice to determine the base damage.

        Returns:
            int: The damage rolled with the weapon's dice.
        """
        return random.randint(1, self.dice)
    
class Event:
    """Represents an event that occurs between rounds."""

    def __init__(self, name, damage_bonus, messages):
        """
        Initialize an event.

        Args:
            name (str): Name of the event.
            damage_bonus (int): Damage bonus provided by the event.
            messages (list): List of messages that represent the event when activated.
        """
        self.name = name
        self.damage_bonus = damage_bonus
        self.is_permanent_bonus = False
        self.is_activated = False
        self.affected_users = []
        self.messages = messages

    def select_participant(self, participants):
        """
        Select a random participant from the list of participants.

        Args:
            participants (list): List of participants.

        Returns:
            Participant: A randomly selected participant.
        """
        if participants:
            selected = random.choice(participants)
            self.affected_users.append(selected)
            return selected
        return None

    def activate_event(self, participants):
        """
        Activate the event, select a participant with a bonus of 0, and apply the effect.

        Args:
            participants (list): List of participants.

        Returns:
            tuple: Affected participant, event title, message, bonus, and permanence flag.
        """
        if not self.is_activated:
            eligible_participants = [p for p in participants if p.bonus == 0]
            
            if eligible_participants:
                affected = self.select_participant(eligible_participants)
                if affected:
                    self.is_activated = False
                    message = random.choice(self.messages).format(affected.name) + f" BONUS: {self.damage_bonus}"
                    return affected, self.name, message, self.damage_bonus, self.is_permanent_bonus
        
        return None

    def reset_event(self):
        """Reset the event's state so it can be activated again."""
        self.is_activated = False
        self.affected_users = []

class Participant:
    """Represents a participant in the Battle Royale game.
    """

    def __init__(self, name):

        """ Initialize a new participant with a name and no weapon.
        Args:
            name (str): The name of the participant.
        """
        self.name = name
        self.weapon = None
        self.has_permanent_weapon = False
        self.bonus = 0
        self.permanent_bonus = 0

    def assign_weapon(self, weapon):
        """
        Assign a weapon to the participant if they don't already have a permanent one.

        Args:
            weapon (Weapon): The weapon to assign to the participant.
        """
        if not self.has_permanent_weapon:
            self.weapon = weapon

    def roll_damage(self):
        """
        Roll the damage using the assigned weapon and apply the current bonus.

        Returns:
            int: The total damage rolled, including any bonuses.
        """
        if not self.weapon:
            return 0 
        base_damage = self.weapon.roll_damage()
        final_damage = base_damage + self.bonus + self.permanent_bonus
        self.bonus = 0
        return final_damage

class Question:

    """Represents a question in the Battle Royale game.
    """
    def __init__(self, question, answer, correct_message, prize, is_permanent):
        """
        Initialize a question for the game.

        Args:
            question (str): The question text.
            answer (str): The correct answer to the question.
            correct_message (str): The message to display when the answer is correct.
            prize (str or int): The prize awarded for answering correctly.
            is_permanent (bool): Flag indicating if the prize is permanent or temporary.
        """

        self.question = question
        self.answer = answer
        self.correct_message = correct_message
        self.prize = prize
        self.is_permanent = is_permanent

    def check_answer(self, given_answer):
        """
        Check if the provided answer is correct.

        Args:
            given_answer (str): The answer provided by the player.

        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        return given_answer.strip().lower() == self.answer.strip().lower()

    def get_prize(self):
        """
        Get the prize information.

        Returns:
            tuple: A tuple containing the prize (int or str) and a boolean indicating if it is permanent.
        """
        try:
            prize_value = int(self.prize)
        except ValueError:
            prize_value = self.prize
        
        return prize_value, self.is_permanent

    def get_correct_message(self):

        """
        Get the correct message including the prize information.

        Returns:
            str: The message indicating the prize and whether it is permanent or not.
        """
        prize_info = f"Prize: {self.prize}"
        if self.is_permanent:
            prize_info += " (Permanent)"
        
        return f"{self.correct_message} {prize_info}"

class BattleRoyaleGame:
    """Manages the Battle Royale game, including participants and battle simulation.
    """

    def __init__(self, weapons_file, events_file, questions_file, max_participants=30, event_probability=50):
        """
        Initialize the Battle Royale game.

        Args:
            weapons_file (str): Path to the JSON file containing weapon data.
            events_file (str): Path to the JSON file containing event data.
            questions_file (str): Path to the JSON file containing question data.
            max_participants (int): Maximum number of participants allowed. Defaults to 30.
            event_probability (int): Probability of an event occurring (%). Defaults to 50.
        """
        self.participants = []
        self.weapons = self._load_weapons(weapons_file)
        self.events = self._load_events(events_file)
        self.available_events = self.events.copy()
        self.questions = self._load_questions(questions_file)
        self.available_questions = self.questions.copy()
        self.active_question = None
        self.active_challenger = None
        self.max_participants = max_participants
        self.event_probability = event_probability
        self.battle_history = []
        self.lock = asyncio.Lock()

    @staticmethod
    def _load_weapons(file_path):
        """Load weapons from a JSON file.

        Args:
            file_path (str): Path to the JSON file containing weapon data.

        Returns:
            list: List of Weapon objects."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return [Weapon(item['name'], item['dice']) for item in data]

    @staticmethod
    def _load_events(file_path):

        """ Load events from a JSON file.
            Args:
                file_path (str): Path to the JSON file containing event data.
            Returns:
                list: List of Event objects.
        """

        with open(file_path, 'r') as f:
            data = json.load(f)
        return [Event(item['name'], item['damage_bonus'], item['messages']) for item in data]

    @staticmethod
    def _load_questions(file_path):
        """
        Load questions from a JSON file.

        Args:
            file_path (str): Path to the JSON file containing question data.

        Returns:
            list: List of Question objects.
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        return [Question(item['question'], item['answer'], item['correct_message'], item['prize'], item['is_permanent']) for item in data]

    async def add_participant(self, participant_name):
        """
        Add a new participant to the game.

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

    def get_participant_by_name(self, name):
        """
        Retrieve a participant by name from the list of participants.

        Args:
            name (str): The name of the participant to retrieve.

        Returns:
            Participant: The participant with the given name, or None if not found.
        """
        return next((p for p in self.participants if p.name == name), None)

    async def wipe(self):
        """
        Clear the list of participants and the battle history.

        Returns:
            bool: True when the wipe is complete.
        """
        async with self.lock:
            self.participants.clear()
            self.battle_history.clear()
            return True

    def is_full(self):
        """
        Check if the maximum number of participants has been reached.

        Returns:
            bool: True if the game is full, False otherwise.
        """
        return len(self.participants) >= self.max_participants

    def is_ready_to_start(self):
        """
        Check if there are enough participants to start the game.

        Returns:
            bool: True if the game can start, False otherwise.
        """
        return len(self.participants) > 1

    def conduct_battle(self, challenge_fight=False, challenge_target=None):
        """
        Simulate a battle between two participants.

        Args:
            challenge_fight (bool): Whether this is a challenge fight.
            challenge_target (Participant): The target participant for a challenge fight.

        Returns:
            tuple: Battle result and details.
        """
        if len(self.participants) < 2 and not challenge_fight:
            return None

        fighter1, fighter2 = (self.active_challenger, challenge_target) if challenge_fight else random.sample(self.participants, 2)

        weapon1 = fighter1.weapon if fighter1.has_permanent_weapon else self._assign_random_weapon(fighter1)
        weapon2 = fighter2.weapon if fighter2.has_permanent_weapon else self._assign_random_weapon(fighter2)

        fighter1_bonus = fighter1.bonus + fighter1.permanent_bonus
        fighter2_bonus = fighter2.bonus + fighter2.permanent_bonus
        roll1, roll2 = fighter1.roll_damage(), fighter2.roll_damage()

        if roll1 > roll2:
            self._record_battle(fighter1, fighter2, roll1)
            return 0, (fighter1.name, weapon1, roll1, fighter1_bonus), (fighter2.name, weapon2, roll2, fighter2_bonus)
        elif roll2 > roll1:
            self._record_battle(fighter2, fighter1, roll2)
            return 1, (fighter2.name, weapon2, roll2, fighter2_bonus), (fighter1.name, weapon1, roll1, fighter1_bonus)
        else:
            return 2, (fighter1.name, weapon1, roll1, fighter1_bonus), (fighter2.name, weapon2, roll2, fighter2_bonus)

    def _assign_random_weapon(self, fighter):
        """
        Assign a random weapon to a fighter.

        Args:
            fighter (Participant): The participant to assign a weapon to.

        Returns:
            Weapon: The assigned weapon.
        """
        weapon = random.choice(self.weapons)
        fighter.assign_weapon(weapon)
        return weapon

    def simulate_event(self):
        """
        Trigger a random event from the collection based on the given probability.

        Returns:
            tuple: Event title and message, or None if no event was triggered.
        """
        if not self.available_events:
            self.available_events = self.events.copy()

        if random.randint(1, 100) <= self.event_probability:
            current_event = random.choice(self.available_events)
            event_result = current_event.activate_event(self.participants)
            
            if event_result:
                affected, name, message, bonus, permanent = event_result
                if permanent:
                    affected.permanent_bonus += bonus
                else:
                    affected.bonus += bonus
                
                self.available_events.remove(current_event)
                
                return name, message

        return None

    def roll_for_question(self):
        """
        Roll to determine if a question should be asked.

        Returns:
            bool: True if a question is selected, False otherwise.
        """
        if not self.available_questions:
            self.available_questions = self.questions.copy()
            
        if random.randint(1, 100) <= self.event_probability / 5:
            self.active_question = random.choice(self.available_questions)
            self.available_questions.remove(self.active_question)
            return True
        return False

    def roll_for_challenge(self):
        """
        Roll to determine if a player becomes the challenger.

        Returns:
            Participant: The challenger participant, or None.
        """
        if not self.active_challenger:
            if random.randint(1, 100) <= self.event_probability / 5:
                self.active_challenger = random.choice(self.participants)
                return self.active_challenger     
        return None

    def _record_battle(self, winner, loser, damage):
        """
        Record the result of a battle and remove the loser from the participant list.

        Args:
            winner (Participant): The participant who won the battle.
            loser (Participant): The participant who lost the battle.
            damage (int): The amount of damage dealt in the battle.
        """
        self.participants.remove(loser)
        self.battle_history.append((winner.name, loser.name, damage))

    def get_winner(self):
        """
        Get the winner of the game if there is only one participant left.

        Returns:
            str or None: The name of the winner, or None if the game is not over.
        """
        return self.participants[0].name if len(self.participants) == 1 else None

    def get_stats(self):
        """
        Get statistics of the top 5 participants, including kills and best hits.

        Returns:
            dict: A dictionary where keys are the top 5 participant names and values are their stats.
        """
        stats = {}
        for winner, loser, damage in self.battle_history:
            if winner not in stats:
                stats[winner] = {'kills': 0, 'best_hit': 0}
            stats[winner]['kills'] += 1
            stats[winner]['best_hit'] = max(stats[winner]['best_hit'], damage)

        participants = [entry[0] for entry in self.battle_history[::-1]]
        top_5_participants = []
        seen = set()

        for participant in participants:
            if participant not in seen:
                top_5_participants.append(participant)
                seen.add(participant)
            if len(top_5_participants) == 5:
                break

        return {participant: stats[participant] for participant in top_5_participants if participant in stats}