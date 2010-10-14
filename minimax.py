import unittest
import itertools

# Consider the point value of the game to the person whose turn it is.
# In this case the board state is:
# * monies of current player
# * monies of enemy player
# * remaining sequence
# * current bid level
# A move consists of updating the board state, possibly yielding score
# Bid level -1 means no bid has been placed.

g_cache = {}

def evaluate(state):
    """
    @return: the value of the state to the current player
    """
    c_mon, e_mon, seq, bid = state
    if not seq:
        return 0
    if state in g_cache:
        return g_cache[state]
    value = sum(seq) - min(sc for sc, st in gen_enemy_score_state_pairs(state))
    g_cache[state] = value
    return value

def gen_enemy_incr_state_pairs(state):
    """
    Yield (incremental_cost, next_state).
    The yielded cost is given to the enemy immediately.
    The next state is from the point of view of the enemy.
    @param state: the state for the current player
    """
    c_mon, e_mon, seq, bid = state
    # forfeit and switch player vantages
    yield seq[0], (e_mon - max(0, bid), c_mon, seq[1:], -1)
    # bid each allowed value and switch player vantages
    for mybid in range(bid+1, c_mon+1):
        yield 0, (e_mon, c_mon, seq, mybid)

def gen_enemy_score_state_pairs(state):
    for incr, e_state in gen_enemy_incr_state_pairs(state):
        yield incr + evaluate(e_state), e_state


class MinimaxTest(unittest.TestCase):

    def test_initial_win_a(self):
        observed = evaluate((8, 8, (5, 4, 3, 2, 1), -1))
        self.assertEqual(8, observed)

    def test_initial_win_b(self):
        observed = evaluate((8, 8, (5, 2, 4, 3, 1), -1))
        self.assertEqual(8, observed)

    def test_losing_state_a(self):
        """
        An initial bid of 5 for 54321 puts the enemy in a losing position.
        """
        observed = evaluate((8, 8, (5, 4, 3, 2, 1), 5))
        self.assertEqual(7, observed)

    def test_winning_state_a(self):
        """
        An initial bid of 6 for 54321 puts the enemy in a winning position.
        """
        observed = evaluate((8, 8, (5, 4, 3, 2, 1), 6))
        self.assertEqual(9, observed)

    def test_losing_state_b(self):
        """
        An initial bid of 4 for 52431 puts the enemy in a losing position.
        """
        observed = evaluate((8, 8, (5, 2, 4, 3, 1), 4))
        self.assertEqual(7, observed)

    def test_counterexample(self):
        state = ((28, 28, (10, 1, 2, 3, 4, 5, 6, 7, 8, 9), -1))
        self.assertEqual(28, evaluate(state))
        state = ((28, 28, (10, 1, 2, 3, 4, 5, 6, 7, 8, 9), 7))
        self.assertEqual(28, evaluate(state))
        state = ((28, 28, (10, 1, 2, 3, 4, 5, 6, 7, 8, 9), 8))
        self.assertEqual(27, evaluate(state))
        state = ((28, 28, (10, 1, 2, 3, 4, 5, 6, 7, 8, 9), 9))
        self.assertEqual(28, evaluate(state))
        state = ((28, 28, (10, 1, 2, 3, 4, 5, 6, 7, 8, 9), 10))
        self.assertEqual(29, evaluate(state))


if __name__ == '__main__':
    unittest.main()
