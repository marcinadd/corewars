from src.core import Core
from src.enum.mode import Mode
from src.enum.modifier import Modifier
from src.game import Game
from src.instructions import Instruction, DAT, MOV, ADD, JMP, SUB
from src.warrior import Warrior


def test_instruction_create():
    instruction = Instruction('AB', '#', 1, '@', -1)
    assert instruction.modifier() == Modifier.AB
    assert instruction.a_mode() == Mode.IMMEDIATE
    assert instruction.a_value() == 1
    assert instruction.b_mode() == Mode.B_INDIRECT
    assert instruction.b_value() == -1


def test_instruction_to_str():
    instruction = DAT('AB', '#', 1, '@', -1)
    assert str(instruction) == 'DAT.AB #1, @-1'


def test_mov_typical():
    warrior = Warrior(processes=[0])
    core = Core(data=[MOV('I', '$', '1', '$', '2'), DAT('F', '$', 1, '$', 2), DAT('F', '$', 0, '$', 0)])
    game = Game(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[2].a_value() == 1
    assert game.core()[2].b_value() == 2


def test_add_typical():
    warrior = Warrior(processes=[0])
    core = Core(data=[ADD('AB', '#', '3', '$', '1'), DAT('F', '$', 1, '$', -5)])
    game = Game(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[1].b_value() == -2


def test_sub_typical():
    warrior = Warrior(processes=[0])
    core = Core(data=[SUB('AB', '#', '3', '$', '1'), DAT('F', '$', 1, '$', -5)])
    game = Game(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[1].b_value() == -8


def test_jmp_typical():
    warrior = Warrior(processes=[2])
    core = Core(data=[DAT('F', '$', 1, '$', -5), DAT('F', '$', 1, '$', -5), JMP('B', '$', -1, '$', 0)])
    game = Game(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.warriors()[0].processes()[0] == 1
