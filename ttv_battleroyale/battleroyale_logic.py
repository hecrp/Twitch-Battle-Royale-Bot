import random
import asyncio
import json

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
        self.permanent_bonus = 0

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
        final_damage = base_damage + self.bonus + self.permanent_bonus
        self.bonus = 0
        return final_damage

class Question:
    def __init__(self, question, answer, correct_message, prize, is_permanent):
        """
        Initializes a riddle for the game.

        Args:
            question (str): The riddle's question.
            answer (str): The correct answer to the riddle.
            correct_message (str): The message to display when the answer is correct, including any bonus or prize information.
            prize (str or int): The prize awarded for answering correctly. Can be a numeric bonus or the name of a weapon.
            is_permanent (bool): Flag indicating if the prize is permanent or temporary.
        """
        self.question = question
        self.answer = answer
        self.correct_message = correct_message
        self.prize = prize
        self.is_permanent = is_permanent

    def check_answer(self, given_answer):
        """
        Checks if the provided answer is correct.

        Args:
            given_answer (str): The answer provided by the player.

        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        return given_answer.strip().lower() == self.answer.strip().lower()

    def get_prize(self):
        """
        Returns the prize information, converting it to a numeric bonus if applicable.

        Returns:
            tuple: A tuple containing the prize (int or str) and a boolean indicating if it is permanent.
        """
        try:
            # Try converting prize to integer (bonus)
            prize_value = int(self.prize)
        except ValueError:
            # If conversion fails, prize is a weapon name (str)
            prize_value = self.prize
        
        return prize_value, self.is_permanent

    def get_correct_message(self):
        """
        Returns the correct message including the prize information.

        Returns:
            str: The message indicating the prize and whether it is permanent or not.
        """
        prize_info = f"Prize: {self.prize}"
        if self.is_permanent:
            prize_info += " (Permanent)"
        
        return f"{self.correct_message} {prize_info}"

class BattleRoyaleGame:
    """
    Manages the Battle Royale game, including participants and battle simulation.

    Attributes:
        participants (list): A list of current participants in the game.
        battle_log (list): A log of battles that have taken place.
        max_participants (int): The maximum number of participants allowed in the game.
        lock (asyncio.Lock): A lock to ensure thread-safe access to participants.
    """

    def __init__(self, weapons_file, events_file, questions_file, max_participants=30, event_probability=50):
        """
        Initializes the Battle Royale game.

        Args:
            weapons_file (str): The path to the JSON file containing weapon data.
            events_file (str): The path to the JSON file containing event data.
            max_participants (int, optional): The maximum number of participants allowed in the game. Defaults to 30.
            event_probability (int, optional): The probability (in percentage) of an event occurring during the game. Defaults to 50.
        """
        self.participants = []
        self.weapons = self.load_weapons(weapons_file)

        self.events = self.load_events(events_file)
        self.available_events = self.events.copy()

        self.questions = self.load_questions(questions_file)
        self.available_questions = self.questions.copy()
        self.active_question = None

        self.active_challenger = None

        self.max_participants = max_participants
        self.event_probability = event_probability

        self.battle_log = []
        self.lock = asyncio.Lock()

    def load_weapons(self, file_path):
        weapons = []
        with open(file_path, 'r') as f:
            data = json.load(f)
            for item in data:
                weapon = Weapon(name=item['name'], dice=item['dice'])
                weapons.append(weapon)
        return weapons

    def load_events(self, file_path):
        events = []
        with open(file_path, 'r') as f:
            data = json.load(f)
            for item in data:
                event = Event(name=item['name'], 
                              damage_bonus=item['damage_bonus'], 
                              messages=item['messages'])
                events.append(event)
        return events
    
    def load_questions(self, file_path):
        questions = []
        with open(file_path, 'r') as f:
            data = json.load(f)
            for item in data:
                question = Question(question=item['question'], 
                                    answer=item['answer'], 
                                    correct_message=item['correct_message'], 
                                    prize=item['prize'], 
                                    is_permanent=item['is_permanent'])
                questions.append(question)
        return questions

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

    def get_participant_byname(self, name):
        """
        Retrieves a participant by name from the list of participants.

        Args:
            name (str): The name of the participant to retrieve.

        Returns:
            Participant: The participant with the given name, or None if not found.
        """
        for participant in self.participants:
            if participant.name == name:
                return participant
        return None

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

    def simulate_battle(self, challenge_fight=False, challenge_target=None):
        """
        Simulates a battle between two random participants or between a challenger and a target.

        Args:
            challenge_fight (bool): Whether the battle is a challenge fight.
            challenge_target (Participant): The target participant for the challenge fight.

        Returns:
            tuple: A tuple containing the result and details of the battle.
        """
        if len(self.participants) < 2 and not challenge_fight:
            return None

        #FIGHTERS SELECTION
        if challenge_fight:
            fighter1, fighter2 = self.active_challenger, challenge_target
        else:
            fighter1, fighter2 = random.sample(self.participants, 2)

        #RANDOM WEAPON ASSIGNMENT TO NON-PERMANENT WEAPON FIGHTERS
        weapon1 = fighter1.weapon if fighter1.permanent_weapon else self.assign_random_weapon(fighter1)
        weapon2 = fighter2.weapon if fighter2.permanent_weapon else self.assign_random_weapon(fighter2)

        #STORE FINAL BONUS AND ROLL FOR DAMAGE
        fighter1_bonus = fighter1.bonus + fighter1.permanent_bonus
        fighter2_bonus = fighter2.bonus + fighter2.permanent_bonus
        roll1, roll2 = fighter1.roll_damage(), fighter2.roll_damage()

        #DETERMINE WHO IS THE WINNER. "2" MEANS TIE. SORRY, I'LL THINK SOMETHING BETTER FOR THIS :(
        if roll1 > roll2:
            self.record_battle(fighter1, fighter2, roll1)
            return 0, (fighter1.name, weapon1, roll1, fighter1_bonus), (fighter2.name, weapon2, roll2, fighter2_bonus)
        elif roll2 > roll1:
            self.record_battle(fighter2, fighter1, roll2)
            return 1, (fighter2.name, weapon2, roll2, fighter2_bonus), (fighter1.name, weapon1, roll1, fighter1_bonus)
        else:
            return 2, (fighter1.name, weapon1, roll1, fighter1_bonus), (fighter2.name, weapon2, roll2, fighter2_bonus)

    def assign_random_weapon(self, fighter):
        """
        Assigns a random weapon to a fighter and updates their weapon attribute.

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
                if permanent:
                    afectado.permanent_bonus += bonus
                else:
                    afectado.bonus += bonus
                
                self.available_events.remove(current_event)
                
                return name, message

        return None

    def roll_for_question(self):
        """
        Rolls to determine if a question should be asked.

        Returns:
            bool: True if a question is selected, False otherwise.
        """
        if not self.available_questions:
            self.available_questions = self.questions.copy()
            
        if random.randint(1, 100) <= self.event_probability / 5:
            self.active_question = random.choice(self.available_questions)
            self.available_questions.remove(self.active_question)
            return True
        else:
            return False

    def roll_for_challenge(self):
        """
        Rolls to determine if a player is now the challenger.

        Returns:
            Object: Challenger participant, None otherwise.
        """
        if not self.active_challenger:
            if random.randint(1, 100) <= self.event_probability / 5:
                self.active_challenger = random.choice(self.participants)
                return self.active_challenger     
        else:
            return False

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
        Returns statistics of the top 5 participants, including kills and best hits.

        Returns:
            dict: A dictionary where keys are the top 5 participant names and values are their stats.
        """
        stats = {}
        for winner, loser, damage in self.battle_log:
            if winner not in stats:
                stats[winner] = {'kills': 0, 'best_hit': 0}
            stats[winner]['kills'] += 1
            stats[winner]['best_hit'] = max(stats[winner]['best_hit'], damage)

        participants = [entry[0] for entry in self.battle_log[::-1]]
        top_5_participants = []
        seen = set()

        for participant in participants:
            if participant not in seen:
                top_5_participants.append(participant)
                seen.add(participant)
            if len(top_5_participants) == 5:
                break

        top_5_stats = {participant: stats[participant] for participant in top_5_participants if participant in stats}

        return top_5_stats