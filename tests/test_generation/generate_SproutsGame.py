from sprouts.SproutsGame import SproutsGame
import random
from copy import deepcopy
import pickle

random.seed(1)
def generate(test_cnt : int, max_n: int) -> None:
    generated = 0
    tests = [] # Tuples (s,a,s')
    # Generate random games
    while generated < test_cnt:
        n = random.randint(1, max_n)

        # Each move is one test
        # Save tuples (s,a,s') - state, action, next state
        game = SproutsGame(n)
        done = game.done
        while not done:
            start_state = deepcopy(game)

            actions = game.get_valid_actions()
            action = deepcopy(random.choice(actions))
            s, done, r = game.step(action)

            end_state = deepcopy(game)
            tests.append((start_state, action, end_state))
            generated += 1
            if generated >= test_cnt:
                break

    # Save tests to file
    pickle.dump(tests, open("tests/test_generation/test_files/tests_SproutsGame", "wb+"))
