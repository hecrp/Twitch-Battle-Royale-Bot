import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from twitchio.ext import commands
import random
from ttv_battleroyale.battleroyale_logic import BattleRoyaleGame
from ttv_battleroyale.sample_game_assets import sample_weapons, sample_events, sample_usernames

#TO USE WITH DOCKER CONTAINER
# TOKEN = os.getenv('TOKEN')
# CHANNEL = os.getenv('CHANNEL')
# ADMIN = os.getenv('ADMIN')

TOKEN = 'TOKEN'
CHANNEL = 'CHANNEL'
ADMIN = 'USER'
#MINIMUM SLEEP TIME FOR TESTING PURPOSES. MODIFY AS NEEDED
EVENT_SLEEP = 1
#MAXIMUM PARTICIPANTS PER GAME
MAX_PARTICIPANTS = 30
#EVENT PROBABILITY (DEFAULT: 50). SET TO 75 FOR TESTING PURPOSES
EVENT_PROBABILITY = 75

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
        #self.game = BattleRoyaleGame(zeling_weapons, zeling_events)

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

    #Twitch bot commands
    @commands.command(name='activar')
    async def activate_game(self, ctx):
        """
        Activates the Battle Royale game, allowing participants to register.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        if ctx.author.name.lower() == ADMIN.lower():
            self.game_active = True
            await self.send_message(ctx, '¡Los Juegos de Sepe van a comenzar! Escribe !apuntar si eres tan valiente como participar...')
            self.game = BattleRoyaleGame(sample_weapons, sample_events.copy(), MAX_PARTICIPANTS, EVENT_PROBABILITY)
        else:
            await self.send_message(ctx, 'Solo el administrador puede activar el juego.')

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
            await self.send_message(ctx, f'¡Listo! Se ha rellenado la lista con usuarios NPC')

        elif not self.game_active:
            await self.send_message(ctx, 'Los Juegos de Sepe no están activados.')
        elif ctx.author.name.lower() != ADMIN.lower():
            await self.send_message(ctx, 'Solo el administrador puede autorellenar con NPCs.')
        else:
            await self.send_message(ctx, 'No se puede autorellenar la lista')

    @commands.command(name='apuntar')
    async def register_participant(self, ctx):
        """
        Registers a participant in the game if it is active and not full.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        if self.game_active and not self.game.is_full():
            if await self.game.add_participant(ctx.author.name):
                await self.send_message(ctx, f'Qué valiente! {ctx.author.name} se ha apuntado a Los Juegos de Sepe!')
            else:
                await self.send_message(ctx, 'Ya estás apuntado o el cupo está lleno.')
        elif not self.game_active:
            await self.send_message(ctx, 'Los juegos de Sepe no están activados.')
        else:
            await self.send_message(ctx, 'Los juegos se Sepe ya están a tope... Lo siento')

    @commands.command(name='wipe')
    async def wipe_participants(self, ctx):
        """
        Wipes the list of participants if the game is active and has not started yet.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        if ctx.author.name.lower() == ADMIN.lower() and self.game_active and not self.game_started:
            await self.game.wipe()
            await self.send_message(ctx, f'¡Hecho! Lista de participantes limpia')
        elif not self.game_active:
            await self.send_message(ctx, 'Los Juegos de Sepe no están activados. No hay participantes que limpiar.')
        elif self.game_started:
            await self.send_message(ctx, 'Los juegos de Sepe ya están en marcha. No puedes limpiar la lista de participantes')
        elif ctx.author.name.lower() != ADMIN.lower():
            await self.send_message(ctx, 'Solo el administrador puede limpiar la lista de participantes.')

    @commands.command(name='empezar')
    async def start_battle_royale(self, ctx):
        """
        Starts the Battle Royale game if it is ready to start and the user is the admin.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        if ctx.author.name.lower() == ADMIN.lower() and self.game_active and self.game.is_ready_to_start():
            await self.send_message(ctx, '¡Que comiencen Los Juegos de Sepe! Quién ganará esta vez?')
            self.game_started = True
            await self.run_battle_royale(ctx)
        else:
            await self.send_message(ctx, 'Los Juegos de Sepe no están listos para comenzar.')

    #Main Loop and final stats
    async def run_battle_royale(self, ctx):
        """
        Runs the Battle Royale game loop, simulating events and battles until there is one winner.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        #Main Game Loop: Probable chained events + random battle
        while len(self.game.participants) > 1:

            await asyncio.sleep(EVENT_SLEEP)

            while True:
                        event_result = self.game.simulate_event()
                        if event_result:
                            event_title, event_message = event_result
                            await ctx.send("/me EVENT!!  " + event_title + ": " + event_message)
                            await asyncio.sleep(EVENT_SLEEP)
                        else:
                            break


            battle_result = self.game.simulate_battle()

            if battle_result:
                (winner, weapon1, roll1, bonus1), (loser, weapon2, roll2, bonus2) = battle_result
                bonus1_str = f"{'+' if bonus1 >= 0 else ''}{bonus1}"
                bonus2_str = f"{'+' if bonus2 >= 0 else ''}{bonus2}"
                await self.send_message(ctx, f'{winner} killed {loser} rolling {roll1} damage using The {weapon1.name} ({bonus1_str})! This time The {weapon2.name} ({bonus2_str}) dealt {roll2} damage but wasn\'t enough!')
            else:
                await self.send_message(ctx, 'Two participants almost killed each other but it is a tie this time... The battle is fierce!')

        winner = self.game.get_winner()

        if winner:
            await self.send_message(ctx, f'{winner} won this edition of Los Juegos de Sepe. Congrats!')
            await self.display_final_stats(ctx)

        self.game_started = False
        self.game_active = False

    async def display_final_stats(self, ctx):
        """
        Displays the final statistics of the game, including the number of kills and the best hit for each participant.

        Args:
            ctx (twitchio.Context): The context object representing the current chat context.
        """
        stats = self.game.get_stats()
        for participant, stat in stats.items():
            kills = stat['kills']
            best_hit = stat['best_hit']
            await self.send_message(ctx, f'{participant} killed {kills} players with a top hit of {best_hit} damage.')

if __name__ == "__main__":
    bot = BattleRoyaleBot()
    bot.run()
