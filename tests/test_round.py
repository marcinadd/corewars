from src.instructions import MOV
from src.round import Round
from src.warrior import Warrior


def test_round_without_gui():
    warrior_a = Warrior([MOV("I", "#", 1, "}", 0)])
    warrior_b = Warrior([MOV("I", "#", 1, "}", 0)])
    round_obj = Round([warrior_a, warrior_b])
    round_obj.play()


def test_has_alive_warriors_true():
    warrior_a = Warrior(processes=[])
    warrior_b = Warrior(processes=[1])
    game = Round([warrior_a, warrior_b], core_size=2)
    assert game.get_alive_warriors()


def test_has_alive_warriors_false():
    warrior_a = Warrior(processes=[])
    warrior_b = Warrior(processes=[])
    game = Round([warrior_a, warrior_b], core_size=2)
    assert game.get_alive_warriors()
