import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from src.battleroyale_logic import BattleRoyaleGame

class TestBattleRoyaleGame(unittest.TestCase):

    def setUp(self):
        self.game = BattleRoyaleGame()

    async def test_add_participant(self):
        self.assertTrue(await self.game.add_participant("user1"))
        self.assertFalse(await self.game.add_participant("user1"))

    async def test_is_full(self):
        for i in range(10):
            await self.game.add_participant(f"user{i}")
        self.assertTrue(self.game.is_full())

    async def test_simulate_battle(self):
        await self.game.add_participant("user1")
        await self.game.add_participant("user2")
        result = self.game.simulate_battle()
        print (result)
        self.assertIsNotNone(result)

    async def test_get_winner(self):
        #Simulate end of Battle Royale: only one user left
        await self.game.add_participant("user1")
        self.assertIsNotNone(self.game.get_winner())
        #Simulate battle should be None when there is only one user alive
        self.assertIsNone(self.game.simulate_battle())

if __name__ == '__main__':
    unittest.main()
