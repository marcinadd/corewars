from src.game import Game
from src.instructions import MOV
from src.warrior import Warrior


def test_play_game_ok():
    warrior_a = Warrior([MOV("I", "#", 1, "}", 0)])
    warrior_b = Warrior([MOV("I", "#", 1, "}", 0)])
    game = Game([warrior_a, warrior_b], max_cycles=20)
    game.play()


def test_game_results():
    warrior_a = Warrior([MOV("I", "#", 1, "}", 0)])
    warrior_b = Warrior([MOV("I", "#", 1, "}", 0)])
    game = Game([warrior_a, warrior_b], max_cycles=20)
    game.get_results_string()
