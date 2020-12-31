from src.round import Round
from src.warrior import Warrior


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
