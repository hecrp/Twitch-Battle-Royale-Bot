import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from twitchio.ext import commands
import random
from ttv_battleroyale.battleroyale_logic import BattleRoyaleGame
from ttv_battleroyale.sample_game_assets import sample_usernames, sample_questions, cosmic_horror_questions

#TO USE WITH DOCKER CONTAINER
# TOKEN = os.getenv('TOKEN')
# CHANNEL = os.getenv('CHANNEL')
# ADMIN = os.getenv('ADMIN')

TOKEN = 'TOKEN'
CHANNEL = 'CHANNEL'
ADMIN = 'ADMIN'

#GAME ASSETS
WEAPONS = 'game_assets/cosmic_horror_set/weapons.json'
EVENTS = 'game_assets/cosmic_horror_set/events.json'
QUESTIONS = cosmic_horror_questions
#MINIMUM SLEEP TIME FOR TESTING PURPOSES. MODIFY AS NEEDED
EVENT_SLEEP = 5
FIGHT_SLEEP = 7
#MAXIMUM PARTICIPANTS PER GAME
MAX_PARTICIPANTS = 30
#EVENT PROBABILITY (DEFAULT: 50). SET TO 75 FOR TESTING PURPOSES
EVENT_PROBABILITY = 55

class BattleRoyaleBot(commands.Bot):
    """
    A Twitch bot that manages and runs a Battle Royale game in the Twitch chat.

    Attributes:
        game_active (bool): Indicates if the game is currently active.
        game_started (bool): Indicates if the game has already started.
        game (BattleRoyaleGame): An instance of the BattleRoyaleGame class that handles the game logic.
    """

    #Base Methods
    def __init__(self):
        """
        Initializes the bot with the necessary credentials and sets up the game state.
        """
        super().__init__(token=TOKEN, prefix='!', initial_channels=[CHANNEL])
        self.game_active = False
        self.game_started = False
        self.paused = False

    async def event_ready(self):
        """
        Called when the bot is successfully connected to Twitch.

        Prints the bot's username and user ID.
        """
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        """
        Handles incoming Twitch chat messages.

        Args:
            message (twitchio.Message): The message object containing the content and metadata.
        """
        if message.author is None:
            print("Received message from an unknown source, skipping...")
            return
        await self.handle_commands(message)

    async def send_message(self, ctx, content):
        """
        Sends a message to the Twitch chat.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
            content (str): The message content to be sent to the chat.
        """
        await ctx.send(content)

    async def pause_game(self):
        self.paused = True

    async def resume_game(self):
        self.paused = False

    #Twitch bot commands
    @commands.command(name='activate')
    async def activate_game(self, ctx):
        """
        Activates the Battle Royale game, allowing participants to register.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        if ctx.author.name.lower() == ADMIN.lower():
            self.game_active = True
            await self.send_message(ctx, 'The Battle Royale is starting soon! Use !join to be part of this fierce tournament.')
            self.game = BattleRoyaleGame(WEAPONS, EVENTS, QUESTIONS, MAX_PARTICIPANTS, EVENT_PROBABILITY)
        else:
            await self.send_message(ctx, 'Only the admin can activate The Battle Royale.')

    @commands.command(name='autofill')
    async def autofill_participants(self, ctx):
        """
        Automatically fills the game with NPC participants if there are less than the maximum number of participants.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        if ctx.author.name.lower() == ADMIN.lower() and self.game_active:
            available_usernames = sample_usernames.copy()

            while not self.game.is_full() and available_usernames:
                random_user = random.choice(available_usernames)
                await self.game.add_participant(f'{random_user}')
                available_usernames.remove(random_user)
            await self.send_message(ctx, 'Done! The list has been filled with NPC participants.')

        elif not self.game_active:
            await self.send_message(ctx, 'The Battle Royale is not active.')
        elif ctx.author.name.lower() != ADMIN.lower():
            await self.send_message(ctx, 'Only the admin can autofill with NPCs.')
        else:
            await self.send_message(ctx, 'Cannot autofill the list.')

    @commands.command(name='join')
    async def register_participant(self, ctx):
        """
        Registers a participant in the game if it is active and not full.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        if self.game_active and not self.game.is_full():
            if await self.game.add_participant(ctx.author.name):
                await self.send_message(ctx, f'How brave! {ctx.author.name} has joined the Battle Royale!')
            else:
                await self.send_message(ctx, 'You are already registered or the game is full.')
        elif not self.game_active:
            await self.send_message(ctx, 'The Battle Royale is not active.')
        else:
            await self.send_message(ctx, 'The Battle Royale is already full... Sorry.')

    @commands.command(name='expand')
    async def expand(self, ctx, num: int):
        """
        Expands the maximum number of participants by a given number.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
            num (int): The number of slots to add to the maximum participants.
        """
        if ctx.author.name.lower() != ADMIN.lower():
            await ctx.send('This command can only be used by the administrator.')
            return

        if self.game_active and not self.game_started:
            if num > 0:
                self.game.max_participants += num
                await ctx.send(f'{num} slots have been added. The maximum number of participants is now {self.game.max_participants}.')
            else:
                await ctx.send('Please provide a positive integer.')
        elif not self.game_active:
            await ctx.send('The game is not active right now.')
        else:
            await ctx.send('You cannot expand the number of participants during an ongoing game.')

    @commands.command(name='seats')
    async def seats(self, ctx):
        """
        Shows the current maximum participants and available spots.
        """
        if self.game_active and not self.game_started:
            current_participants = len(self.game.participants)
            available_spots = self.game.max_participants - current_participants
            await ctx.send(f'The maximum number of participants is {self.game.max_participants}. There are currently {available_spots} available spots.')
        elif not self.game_active:
            await ctx.send('The game is not active right now.')
        else:
            await ctx.send('A game is in progress, no seats are available.')

    @commands.command(name='wipe')
    async def wipe_participants(self, ctx):
        """
        Wipes the list of participants if the game is active and has not started yet.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        if ctx.author.name.lower() == ADMIN.lower() and self.game_active and not self.game_started:
            await self.game.wipe()
            await self.send_message(ctx, 'Done! Participant list wiped.')
        elif not self.game_active:
            await self.send_message(ctx, 'The Battle Royale is not active. No participants to wipe.')
        elif self.game_started:
            await self.send_message(ctx, 'The Battle Royale has already started. You cannot wipe the participant list.')
        elif ctx.author.name.lower() != ADMIN.lower():
            await self.send_message(ctx, 'Only the admin can wipe the participant list.')

    @commands.command(name='fight')
    async def start_battle_royale(self, ctx):
        """
        Starts the Battle Royale game if it is ready to start and the user is the admin.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        if ctx.author.name.lower() == ADMIN.lower() and self.game_active and self.game.is_ready_to_start():
            await self.send_message(ctx, 'Let this edition of The Battle Royale begin! Who will win this time?')
            self.game_started = True
            await self.run_battle_royale(ctx)
        else:
            await self.send_message(ctx, 'The Battle Royale is not ready to start.')

    @commands.command(name="answer")
    async def answer(self, ctx, user_answer: str):
        if self.game.active_question:
            question = self.game.active_question
            
            participant = next((p for p in self.game.participants if p.name == ctx.author.name), None)
            
            if participant:
                if user_answer.lower() == question.answer.lower():
                    prize, is_permanent = question.get_prize()
                    
                    self.game.active_question = None
                    
                    if isinstance(prize, int):
                        if is_permanent:
                            participant.permanent_bonus += prize
                        else:
                            participant.bonus += prize
                    elif isinstance(prize, str):
                        weapon = next((w for w in self.game.weapons if w.name == prize), None)
                        if weapon:
                            participant.weapon = weapon
                            if is_permanent:
                                participant.permanent_weapon = True

                    await ctx.send(f"/me Correct answer, {ctx.author.name}! {question.get_correct_message()}")
                else:
                    print("WRONG ANSWER")

    @commands.command(name="challenge")
    async def challenge(self, ctx, target_user: str):

        if not self.paused and self.game.active_challenger and ctx.author.name.lower() == self.game.active_challenger.name.lower():

            target = next((p for p in self.game.participants if p.name.lower() == target_user.lower()), None)
            if target:
                await ctx.send(f"/me NEW CHALLENGE! {ctx.author.name} will face {target_user} in the next battle!")
                battle_result = self.game.simulate_battle(True, target)
                await self.post_battle_result(ctx, battle_result)
                self.game.active_challenger = None
            else:
                await ctx.send(f"/me Hey! {ctx.author.name}, the user {target_user} is not playing right now. Try again...")

    @commands.command(name='pause')
    async def pause(self, ctx):
        """
        Pauses the ongoing game.
        Only admins can use this command.
        """
        if ctx.author.name.lower() == ADMIN.lower():
            if self.game_active and self.game_started:
                await self.pause_game()
                await ctx.send("/me ATTENTION: The game has benn paused.")
            else:
                await ctx.send("/me There is no ongoing game.")
        else:
            await ctx.send("/me Only an admin can pause the game.")

    @commands.command(name='resume')
    async def resume(self, ctx):
        """
        Resumes the paused game.
        Only admins can use this command.
        """
        if ctx.author.name.lower() == ADMIN.lower():
            if self.game_started and self.paused:
                await self.resume_game()
                await ctx.send("/me ATTENTION: The game is now resumed.")
            else:
                await ctx.send("/me There is not a paused game.")
        else:
            await ctx.send("/me Only and admin can resume the game.")

    async def post_battle_result(self, ctx, battle_result):
        whowin, (winner, weapon1, roll1, bonus1), (loser, weapon2, roll2, bonus2) = battle_result
        
        if whowin in [0, 2]:
            battle_message = (
                f"FIGHT!! {winner} equipped with The {weapon1.name} (D{weapon1.dice}) and ({bonus1:+}) bonus "
                f"VS {loser} equipped with The {weapon2.name} (D{weapon2.dice}) and ({bonus2:+}) bonus!"
            )
        else:
            battle_message = (
                f"FIGHT!! {loser} equipped with The {weapon2.name} (D{weapon2.dice}) and ({bonus2:+}) bonus "
                f"VS {winner} equipped with The {weapon1.name} (D{weapon1.dice}) and ({bonus1:+}) bonus!"
            )

        await self.send_message(ctx, battle_message)

        await asyncio.sleep(FIGHT_SLEEP)
        
        result_message = (
            f"RESULT: {winner} rolled a total of {roll1} damage and killed {loser} ({roll2} damage)! "
            f"" 
            if whowin in [0, 1] else 
            f"TIE!! Both players dealt {roll1} damage. They almost killed each other... The battle is fierce!"
        )
        await self.send_message(ctx, result_message)

    async def run_battle_royale(self, ctx):
        """
        Runs the Battle Royale game loop, simulating events and battles until there is one winner.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        while len(self.game.participants) > 1:
            await asyncio.sleep(EVENT_SLEEP)

            #EVENTS
            while not self.paused:
                event_result = self.game.simulate_event()
                if event_result:
                    event_title, event_message = event_result
                    await ctx.send(f"/me EVENT!! {event_title}: {event_message}")
                    await asyncio.sleep(EVENT_SLEEP)
                    if random.random() <= 0.7:  # 70% CHANCE TO CHAINED EVENT
                        break
                else:
                    break

            #CHALLENGES.
            if not self.paused and self.game.roll_for_challenge():
                await ctx.send(f"/me ATTENTION {self.game.active_challenger.name}, YOU are now the Challenger!! Use !challenge user to fight any other user alive.")
                await asyncio.sleep(EVENT_SLEEP)

            #QUESTIONS
            if not self.paused and self.game.roll_for_question():
                await ctx.send(f"/me Question!! Answer using ONE word following the !answer command: {self.game.active_question.question}")
                await asyncio.sleep(EVENT_SLEEP)

            #FIGHT
            if not self.paused:
                battle_result = self.game.simulate_battle()
                await self.post_battle_result(ctx, battle_result)
        
        #GAME FINISHED: WINNER ANNOUNCE
        winner = self.game.get_winner()
        if winner:
            await self.send_message(ctx, f'{winner} won this edition of The Battle Royale. Congrats!')
            await self.display_final_stats(ctx)

        #RESET GAME MAIN STATES
        self.game_started = False
        self.game_active = False

    async def display_final_stats(self, ctx):
        """
        Displays the final statistics of the game in a single message, including the number of kills, 
        the best hit, and the rank for the top 5 participants.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        stats = self.game.get_stats()

        message_lines = ["TOP 5 players: "]

        for rank, (participant, stat) in enumerate(stats.items(), start=1):
            kills = stat['kills']
            best_hit = stat['best_hit']
            message_lines.append(f'{rank}-{participant}: {kills} kills, Best Hit: {best_hit}. ')

        final_message = "\n".join(message_lines)
        
        await self.send_message(ctx, final_message)

if __name__ == "__main__":
    bot = BattleRoyaleBot()
    bot.run()
