from src.core import Core
from src.enum.mode import Mode
from src.enum.modifier import Modifier
from src.instructions import DAT, MOV, ADD, JMP, SUB, SPL, JMZ, JMN, DJN, SEQ, DIV, MOD, SLT
from src.instructions import get_default_modifier
from src.round import Round
from src.warrior import Warrior


def test_instruction_create():
    instruction = DAT('AB', '#', 1, '@', -1)
    assert instruction.modifier() == Modifier.AB
    assert instruction.a_mode() == Mode.IMMEDIATE
    assert instruction.a_value() == 1
    assert instruction.b_mode() == Mode.B_INDIRECT
    assert instruction.b_value() == -1


def test_instruction_to_str():
    instruction = DAT('AB', '#', 1, '@', -1)
    assert str(instruction) == 'DAT.AB #1, @-1'


def test_mov_a():
    warrior = Warrior(processes=[0])
    core = Core(data=[MOV('A', '$', '1', '$', '2'), DAT('F', '$', 1, '$', 2), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[2].a_value() == 1
    assert game.core()[2].b_value() == 0


def test_mov_b():
    warrior = Warrior(processes=[0])
    core = Core(data=[MOV('B', '$', '1', '$', '2'), DAT('F', '$', 1, '$', 3), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[2].a_value() == 0
    assert game.core()[2].b_value() == 3


def test_mov_ab():
    warrior = Warrior(processes=[0])
    core = Core(data=[MOV('AB', '$', '1', '$', '2'), DAT('F', '$', 1, '$', 4), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[2].a_value() == 0
    assert game.core()[2].b_value() == 1


def test_mov_ba():
    warrior = Warrior(processes=[0])
    core = Core(data=[MOV('BA', '$', '1', '$', '2'), DAT('F', '$', 1, '$', 5), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[2].a_value() == 5
    assert game.core()[2].b_value() == 0


def test_mov_f():
    warrior = Warrior(processes=[0])
    core = Core(data=[MOV('F', '$', '1', '$', '2'), DAT('F', '$', 1, '$', 6), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[2].a_value() == 1
    assert game.core()[2].b_value() == 6


def test_mov_x():
    warrior = Warrior(processes=[0])
    core = Core(data=[MOV('X', '$', '1', '$', '2'), DAT('F', '$', 1, '$', 7), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[2].a_value() == 7
    assert game.core()[2].b_value() == 1


def test_mov_i():
    warrior = Warrior(processes=[0])
    core = Core(data=[MOV('I', '$', '1', '$', '2'), DAT('F', '$', 1, '$', 2), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[2].a_value() == 1
    assert game.core()[2].b_value() == 2


def test_sub_a():
    warrior = Warrior(processes=[0])
    core = Core(data=[SUB('A', '#', '3', '$', '1'), DAT('F', '$', 2, '$', -5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    instruction = game.core()[1]
    assert instruction.a_value() == -1
    assert instruction.b_value() == -5


def test_sub_b():
    warrior = Warrior(processes=[0])
    core = Core(data=[SUB('B', '#', '3', '$', '1'), DAT('F', '$', 2, '$', -5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    instruction = game.core()[1]
    assert instruction.a_value() == 2
    assert instruction.b_value() == -6


def test_sub_ab():
    warrior = Warrior(processes=[0])
    core = Core(data=[SUB('AB', '#', '3', '$', '1'), DAT('F', '$', 2, '$', -5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    instruction = game.core()[1]
    assert instruction.a_value() == 2
    assert instruction.b_value() == -8


def test_sub_ba():
    warrior = Warrior(processes=[0])
    core = Core(data=[SUB('BA', '#', '3', '$', '1'), DAT('F', '$', 2, '$', -5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    instruction = game.core()[1]
    assert instruction.a_value() == -8
    assert instruction.b_value() == -5


def test_sub_f():
    warrior = Warrior(processes=[0])
    core = Core(data=[SUB('F', '#', '3', '$', '1'), DAT('F', '$', 2, '$', -5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    instruction = game.core()[1]
    assert instruction.a_value() == -1
    assert instruction.b_value() == -6


def test_sub_x():
    warrior = Warrior(processes=[0])
    core = Core(data=[SUB('X', '#', '3', '$', '1'), DAT('F', '$', 2, '$', -5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    instruction = game.core()[1]
    assert instruction.a_value() == 1
    assert instruction.b_value() == -8


def test_add_ab():
    warrior = Warrior(processes=[0])
    core = Core(data=[ADD('AB', '#', '3', '$', '1'), DAT('F', '$', 2, '$', -5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    instruction = game.core()[1]
    assert instruction.a_value() == 2
    assert instruction.b_value() == -2


def test_sub_typical():
    warrior = Warrior(processes=[0])
    core = Core(data=[SUB('AB', '#', '3', '$', '1'), DAT('F', '$', 1, '$', -5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[1].b_value() == -8


def test_jmp_typical():
    warrior = Warrior(processes=[2])
    core = Core(data=[DAT('F', '$', 1, '$', -5), DAT('F', '$', 1, '$', -5), JMP('B', '$', -1, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.warriors()[0].processes()[0] == 1


def test_core_add_cycle_end():
    warrior = Warrior(processes=[1])
    core = Core(data=[DAT('F', '$', 1, '$', 5), ADD('AB', '#', '3', '$', '2'), DAT('F', '$', 1, '$', -5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[0].b_value() == 8


def test_core_add_cycle_end_two_times():
    warrior = Warrior(processes=[1])
    core = Core(data=[DAT('F', '$', 1, '$', 5), ADD('AB', '#', '3', '$', '5'), DAT('F', '$', 1, '$', -5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[0].b_value() == 8


def test_core_add_cycle_begin():
    warrior = Warrior(processes=[1])
    core = Core(data=[DAT('F', '$', 1, '$', 5), ADD('AB', '#', '3', '$', '-2'), DAT('F', '$', 1, '$', -5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[2].b_value() == -2


def test_core_add_cycle_begin_two_times():
    warrior = Warrior(processes=[1])
    core = Core(data=[DAT('F', '$', 1, '$', 5), ADD('AB', '#', '3', '$', '-5'), DAT('F', '$', 1, '$', -5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[2].b_value() == -2


def test_core_predecrement_a():
    warrior = Warrior(processes=[0])
    core = Core(data=[DAT('F', '{', 1, '$', 1), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[1].a_value() == -1


def test_core_predecrement_b():
    warrior = Warrior(processes=[0])
    core = Core(data=[DAT('F', '<', 1, '$', 1), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[1].b_value() == -1


def test_core_postincrement_a():
    warrior = Warrior(processes=[0])
    core = Core(data=[DAT('F', '}', 1, '$', 1), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[1].a_value() == 1


def test_core_postincrement_b():
    warrior = Warrior(processes=[0])
    core = Core(data=[DAT('F', '>', 1, '$', 1), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert game.core()[1].b_value() == 1


def test_spl_typical():
    warrior = Warrior(processes=[0])
    core = Core(data=[SPL('F', '$', 2, '$', 2), DAT('F', '$', 0, '$', 0), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [1, 2]


def test_jmz_a_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[JMZ('A', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 0, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [2]


def test_jmz_a_not_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[JMZ('A', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 1, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [1]


def test_jmz_b_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[JMZ('B', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 1, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [2]


def test_jmz_b_not_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[JMZ('B', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 0, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [1]


def test_jmz_f_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[JMZ('F', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [2]


def test_jmz_f_not_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[JMZ('B', '$', 2, '$', 0), DAT('F', '$', 0, '$', 1), DAT('F', '$', 0, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [1]


def test_jmn_a_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[JMN('A', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 0, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [1]


def test_jmn_a_not_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[JMN('A', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 1, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [2]


def test_jmn_b_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[JMN('B', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 1, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [1]


def test_jmn_b_not_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[JMN('B', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 0, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [2]


def test_jmn_f_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[JMN('F', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [1]


def test_jmn_f_not_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[JMN('B', '$', 2, '$', 0), DAT('F', '$', 0, '$', 1), DAT('F', '$', 0, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [2]


def test_djn_a_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[DJN('A', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 1, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [1]


def test_djn_a_not_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[DJN('A', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 2, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [2]


def test_djn_b_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[DJN('B', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 1, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [1]


def test_djn_b_not_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[DJN('B', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 0, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [2]


def test_djn_f_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[DJN('F', '$', 2, '$', 0), DAT('F', '$', 0, '$', 0), DAT('F', '$', 1, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [1]


def test_djn_f_not_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[DJN('B', '$', 2, '$', 0), DAT('F', '$', 0, '$', 1), DAT('F', '$', 0, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes() == [2]


def test_post_decrement_a():
    warrior = Warrior(processes=[0])
    core = Core(data=[MOV('I', '}', 1, '$', 1), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert core[1].a_value() == 0
    assert core[1].b_value() == 0


def test_seq_a_yes():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('A', '$', 1, '$', 2), DAT('F', '$', 1, '$', 4), DAT('F', '$', 1, '$', 5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 2


def test_seq_a_no():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('A', '$', 1, '$', 2), DAT('F', '$', 1, '$', 4), DAT('F', '$', 2, '$', 5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 1


def test_seq_b_yes():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('B', '$', 1, '$', 2), DAT('F', '$', 2, '$', 4), DAT('F', '$', 3, '$', 4)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 2


def test_seq_b_no():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('B', '$', 1, '$', 2), DAT('F', '$', 1, '$', 4), DAT('F', '$', 2, '$', 5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 1


def test_seq_ab_yes():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('AB', '$', 1, '$', 2), DAT('F', '$', 2, '$', 4), DAT('F', '$', 3, '$', 2)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 2


def test_seq_ab_no():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('AB', '$', 1, '$', 2), DAT('F', '$', 1, '$', 4), DAT('F', '$', 4, '$', 5)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 1


def test_seq_ba_yes():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('BA', '$', 1, '$', 2), DAT('F', '$', 2, '$', 4), DAT('F', '$', 4, '$', 2)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 2


def test_seq_ba_no():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('BA', '$', 1, '$', 2), DAT('F', '$', 1, '$', 4), DAT('F', '$', 3, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 1


def test_seq_f_yes():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('F', '$', 1, '$', 2), DAT('F', '$', 2, '$', 4), DAT('F', '$', 2, '$', 4)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 2


def test_seq_f_no():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('F', '$', 1, '$', 2), DAT('F', '$', 1, '$', 4), DAT('F', '$', 1, '$', 1)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 1


def test_seq_x_yes():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('X', '$', 1, '$', 2), DAT('F', '$', 2, '$', 4), DAT('F', '$', 4, '$', 2)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 2


def test_seq_x_no():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('X', '$', 1, '$', 2), DAT('F', '$', 1, '$', 4), DAT('F', '$', 1, '$', 4)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 1


def test_seq_i_yes():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('I', '$', 1, '$', 2), DAT('F', '$', 2, '$', 4), DAT('F', '$', 2, '$', 4)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 2


def test_seq_i_no():
    warrior = Warrior(processes=[0])
    core = Core(data=[SEQ('I', '$', 1, '$', 2), JMP('F', '$', 2, '$', 4), DAT('F', '$', 2, '$', 4)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert warrior.processes()[0] == 1


def test_div_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[DIV('I', '$', 1, '$', 2), DAT('F', '$', 0, '$', 0), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert len(warrior.processes()) == 0


def test_mod_zero():
    warrior = Warrior(processes=[0])
    core = Core(data=[MOD('I', '$', 1, '$', 2), DAT('F', '$', 0, '$', 0), DAT('F', '$', 0, '$', 0)])
    game = Round(core=core, warriors=[warrior], init_warriors=False)
    game.simulation_step()
    assert len(warrior.processes()) == 0


def test_get_default_modifier():
    assert get_default_modifier(DAT) == Modifier.F
    assert get_default_modifier(SLT) == Modifier.B
