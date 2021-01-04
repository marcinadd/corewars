from src.instructions import MOV
from src.round import Round
from src.warrior import Warrior


def test_round_without_gui():
    warrior_a = Warrior([MOV("I", "#", 1, "}", 0)])
    warrior_b = Warrior([MOV("I", "#", 1, "}", 0)])
    round_obj = Round([warrior_a, warrior_b])
    round_obj.play()
