#Sample username for !autofill and sample questions list
from ttv_battleroyale.battleroyale_logic import Question

sample_questions = [
    Question(
        question="What is the name of the sword that Aragorn wields?",
        answer="Anduril",
        correct_message="The sword reforged, Anduril, Flame of the West, is now yours! Your strength increases!",
        prize="Titan’s Greatsword",
        is_permanent=True
    ),
    Question(
        question="What is the home of the Elves in Middle-Earth?",
        answer="Rivendell",
        correct_message="The wisdom of Rivendell grants you clarity. Your next attack will be True!",
        prize=3,
        is_permanent=False
    ),
    Question(
        question="Who is known as the 'White Wizard'?",
        answer="Gandalf",
        correct_message="Gandalf's power flows through you, increasing your magical abilities!",
        prize="Fireball Spell",
        is_permanent=False
    ),
    Question(
        question="What is the name of the Dark Lord in the Lord of the Rings?",
        answer="Sauron",
        correct_message="The shadow of Sauron looms, but you resist, gaining new strength!",
        prize=5,
        is_permanent=True
    ),
    Question(
        question="What is Frodo's last name?",
        answer="Baggins",
        correct_message="You share in the courage of Frodo Baggins, gaining endurance!",
        prize="Mace of the Holy Light",
        is_permanent=False
    ),
    Question(
        question="Which creature did Gandalf face in the Mines of Moria?",
        answer="Balrog",
        correct_message="The fire of the Balrog's defeat fuels your resolve!",
        prize=4,
        is_permanent=False
    ),
    Question(
        question="What is the elvish word for 'friend'?",
        answer="Mellon",
        correct_message="The doors of Durin open to you, revealing a hidden strength!",
        prize=2,
        is_permanent=False
    ),
    Question(
        question="Who is the King of Rohan?",
        answer="Theoden",
        correct_message="King Theoden's valor inspires you, boosting your combat skills!",
        prize="Battle Axe of the Fallen",
        is_permanent=True
    ),
    Question(
        question="What is the name of the inn in Bree where Frodo and his friends meet Strider?",
        answer="Prancing Pony",
        correct_message="At the Prancing Pony, you find respite and renewed energy!",
        prize=3,
        is_permanent=False
    ),
    Question(
        question="What type of creature is Smaug?",
        answer="Dragon",
        correct_message="You possess the cunning of Smaug, increasing your attack power!",
        prize="Doombringer Scythe",
        is_permanent=True
    ),

    # Adivinanzas y preguntas pequeñas
    Question(
        question="What has roots as nobody sees, is taller than trees, up, up it goes, and yet never grows?",
        answer="Mountain",
        correct_message="You have the endurance of a mountain! Your defense increases!",
        prize=4,
        is_permanent=True
    ),
    Question(
        question="This thing all things devours: Birds, beasts, trees, flowers; Gnaws iron, bites steel; Grinds hard stones to meal; Slays king, ruins town, and beats high mountain down.",
        answer="Time",
        correct_message="You have understood the power of Time itself. Your wisdom grows!",
        prize="Orbital Strike Device",
        is_permanent=False
    ),
    Question(
        question="Voiceless it cries, Wingless flutters, Toothless bites, Mouthless mutters. What is it?",
        answer="Wind",
        correct_message="The wind whispers your name, guiding your strikes!",
        prize=3,
        is_permanent=False
    ),
    Question(
        question="A box without hinges, key, or lid, yet golden treasure inside is hid.",
        answer="Egg",
        correct_message="The treasure of the egg nourishes your strength. Your attacks are more powerful!",
        prize=2,
        is_permanent=False
    ),
    Question(
        question="It cannot be seen, cannot be felt, cannot be heard, cannot be smelt. It lies behind stars and under hills, and empty holes it fills. It comes first and follows after, Ends life, kills laughter.",
        answer="Darkness",
        correct_message="You understand the power of Darkness, using it to your advantage!",
        prize="Shadow Blade",
        is_permanent=True
    ),
    Question(
        question="Alive without breath, As cold as death; Never thirsty, ever drinking, All in mail never clinking.",
        answer="Fish",
        correct_message="The cunning of the fish is now yours, increasing your agility!",
        prize=2,
        is_permanent=False
    ),
    Question(
        question="An eye in a blue face saw an eye in a green face. 'That eye is like to this eye' Said the first eye, 'But in low place, not in high place.'",
        answer="Sun",
        correct_message="The Sun’s light fills you with warmth, boosting your health!",
        prize=3,
        is_permanent=False
    ),
    Question(
        question="It cannot be seen, cannot be felt, cannot be heard, cannot be smelt. What is it?",
        answer="Air",
        correct_message="You harness the power of Air, moving swiftly in battle!",
        prize="Hunter’s Bow",
        is_permanent=False
    ),
    Question(
        question="If you look at the numbers on my face, you won’t find thirteen anyplace.",
        answer="Clock",
        correct_message="The clock reveals time’s secrets to you, increasing your awareness!",
        prize=3,
        is_permanent=False
    ),
    Question(
        question="What has a heart that doesn’t beat?",
        answer="Artichoke",
        correct_message="You have uncovered the artichoke's mystery, gaining resilience!",
        prize=1,
        is_permanent=False
    )
]

cosmic_horror_questions = [
    Question(
        question="I am the dark that lives beyond the stars, always present but never seen. What am I?",
        answer="void",
        correct_message="Indeed, the void is ever-present, lurking beyond the stars, unseen but all-encompassing.",
        prize=2,
        is_permanent=False
    ),
    Question(
        question="I have many faces, but none can see me. I am eternal, yet I end all. What am I?",
        answer="death",
        correct_message="You understand the inevitability of death, the eternal force that ends all things.",
        prize=3,
        is_permanent=True
    ),
    Question(
        question="I slither without a body, whispering secrets that drive men mad. What am I?",
        answer="shadow",
        correct_message="A shadow, indeed. It slithers without form, whispering madness into the minds of the unwary.",
        prize=1,
        is_permanent=False
    ),
    Question(
        question="I am not alive, yet I grow; I do not breathe, yet I consume. What am I?",
        answer="fire",
        correct_message="Fire, a living paradox. It grows, consumes, and yet is not truly alive.",
        prize="Eldritch Flame",
        is_permanent=True
    ),
    Question(
        question="I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
        answer="echo",
        correct_message="An echo, yes. A voice of the wind, speaking without a body.",
        prize=2,
        is_permanent=False
    ),
    Question(
        question="I am the keeper of time, but I do not tick. I silently watch all things, from beginning to end. What am I?",
        answer="stars",
        correct_message="The stars, silent keepers of time, watching the cosmos from beginning to end.",
        prize="Celestial Blade",
        is_permanent=True
    ),
    Question(
        question="I have no wings, but I can fly. I have no eyes, but I can cry. What am I?",
        answer="cloud",
        correct_message="A cloud, floating in the sky, shedding tears upon the world below.",
        prize=1,
        is_permanent=False
    ),
    Question(
        question="I guard the gate to the unknown, and once you pass, there is no return. What am I?",
        answer="dream",
        correct_message="A dream, guarding the threshold to the unknown, from which there is no return.",
        prize=2,
        is_permanent=True
    ),
    Question(
        question="I can be cracked, made, told, and played. What am I?",
        answer="riddle",
        correct_message="A riddle, indeed. A puzzle of words, meant to challenge the mind.",
        prize=1,
        is_permanent=False
    ),
    Question(
        question="I exist in the realm of fear, born from the mind's eye. I am as real as you believe me to be. What am I?",
        answer="nightmare",
        correct_message="A nightmare, a creation of the mind's eye, as real as your fear allows.",
        prize="Nightmare Blade",
        is_permanent=True
    )
]

sample_usernames = [
    "cool_cat42",
    "meme_lord_2000",
    "dancing_banana",
    "coffee_addict_87",
    "ninja_coder",
    "sunset_chaser",
    "pizza_lover_3000",
    "gamer_girl_xx",
    "bookworm_123",
    "fitness_freak_2024",
    "travel_bug_nomad",
    "music_maestro",
    "tech_guru_101",
    "food_photographer",
    "eco_warrior_green",
    "movie_buff_cinephile",
    "art_vandal",
    "crypto_king_btc",
    "yoga_master_zen",
    "fashionista_chic",
    "dog_whisperer_woof",
    "meme_queen_lol",
    "sports_fanatic_23",
    "science_nerd_42",
    "history_buff_1776",
    "conspiracy_theorist_x",
    "dank_memer_420",
    "cosmic_explorer",
    "plant_parent_green_thumb",
    "social_butterfly_xoxo"
]