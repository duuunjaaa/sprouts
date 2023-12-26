import sys
sys.path.append('..\sprouts')
from sprouts.SproutsGame import SproutsGame
import pickle

class TestSproutsGame:
    def test_step(self):
        state_tuples = pickle.load(open("tests/test_generation/test_files/tests_SproutsGame", "rb"))
        for i,state_tuple in enumerate(state_tuples):
            game = state_tuple[0]
            action = state_tuple[1]
            expected_state = state_tuple[2]
            s, done, r = game.step(action)
            assert done == expected_state.done
            assert r == expected_state.get_state_value()
            expected_state_str = ''.join([str(x) for x in state_tuple[2].state])
            s_str = ''.join([str(region) for region in s])
            assert s_str == expected_state_str

# TestSproutsGame().test_step()