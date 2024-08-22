import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from src.bot import BattleRoyaleBot

class TestTwitchIntegration(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.bot = BattleRoyaleBot()

    @patch('src.bot.BattleRoyaleBot.send_message')
    async def test_battle_royale_integration(self, mock_send_message):
        # Configurar mock para el contexto y el autor del comando
        ctx = MagicMock()
        ctx.author.name.lower.return_value = 'admin'
        ctx.send = AsyncMock()

        # Activar el juego
        await self.bot.activate_game(ctx)
        self.assertTrue(self.bot.game_active)
        ctx.send.assert_called_with('¡El Battle Royale ha sido activado! Escribe !apuntar para unirte.')

        # Añadir 10 participantes manualmente
        for i in range(10):
            user_name = f'manual_user{i}'
            ctx.author.name = user_name
            await self.bot.register_participant(ctx)
            ctx.send.assert_called_with(f'{user_name} se ha apuntado al Battle Royale!')
        self.assertEqual(len(self.bot.game.participants), 10)

        # No se puede autorellenar una partida llena
        # Modo administrador para limpiar y autorellenar (user: admin)
        ctx.author.name = 'admin'
        await self.bot.autofill_participants(ctx)
        ctx.send.assert_called_with('Cupo de participantes lleno. No se han añadido usuarios mock')

        # Wipe de participantes
        ctx.author.name = 'admin'
        await self.bot.wipe_participants(ctx)
        self.assertEqual(len(self.bot.game.participants), 0)
        ctx.send.assert_called_with('¡Listo! Lista de participantes limpia')

        # Autorellenar lista de participanes vacía
        ctx.author.name = 'admin'
        await self.bot.autofill_participants(ctx)
        ctx.send.assert_called_with('¡Listo! Se han apuntado participantes mock')
        self.assertEqual(len(self.bot.game.participants), 10)

        # Autorellenar lista de participanes sin completar
        ctx.author.name = 'admin'
        await self.bot.wipe_participants(ctx)
        self.assertEqual(len(self.bot.game.participants), 0)
        for i in range(5):
            user_name = f'initial_user{i}'
            ctx.author.name = user_name
            await self.bot.register_participant(ctx)
            ctx.send.assert_called_with(f'{user_name} se ha apuntado al Battle Royale!')
        self.assertEqual(len(self.bot.game.participants), 5)
        ctx.author.name = 'admin'
        await self.bot.autofill_participants(ctx)
        self.assertEqual(len(self.bot.game.participants), 10)
        ctx.author.name = 'admin'
        ctx.send.assert_called_with('¡Listo! Se han apuntado participantes mock')

        # Wipe+Ola de participantes
        ctx.author.name = 'admin'
        await self.bot.wipe_participants(ctx)
        self.assertEqual(len(self.bot.game.participants), 0)
        ctx.send.assert_called_with('¡Listo! Lista de participantes limpia')
        for i in range(50):
            user_name = f'initial_user{i}'
            ctx.author.name = user_name
            await self.bot.register_participant(ctx)
        ctx.send.assert_called_with('El cupo está lleno.')
    
        # Empezar el juego
        ctx.author.name = 'admin'
        await self.bot.start_battle_royale(ctx)
        ctx.send.assert_any_call('¡El Battle Royale comienza ahora!')

        # Finalizar el juego
        winner = self.bot.game.get_winner()
        self.assertIsNotNone(winner)
        ctx.send.assert_any_call(f'{winner} is the champion of the Battle Royale!')
        self.assertFalse(self.bot.game_active)

    async def asyncTearDown(self):
        self.bot = None

if __name__ == '__main__':
    unittest.main()
