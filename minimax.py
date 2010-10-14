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
    c_mon, e_mon, seq, bid = state
    if not seq:
        return 0
    if state in g_cache:
        return g_cache[state]
    value = sum(seq) - min(sc for sc, st in gen_enemy_score_state_pairs(state))
    g_cache[state] = value
    return value

def gen_enemy_states(state):
    """
    Yield (cost, next_state).
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
    for e_value, e_state in gen_enemy_states(state):
        yield e_value + evaluate(e_state), e_state

def backtrace(state):
    print state, 'is worth', evaluate(state), 'to the current player'
    while True:
        print state
        c_mon, e_mon, seq, bid = state
        if not seq:
            break
        v, state = min(gen_enemy_score_state_pairs(state))

def seek_counterexample():
    N = 5
    tsum = (N*(N+1))/2
    if tsum % 2 == 0:
        raise ValueError('sum of all scores should be odd')
    target = tsum - tsum/2
    print 'required score to win:', target
    for remainder in itertools.permutations(range(1,N)):
        seq = tuple([N] + list(remainder))
        state = (target, target, seq, -1)
        print state, 'is worth', evaluate(state), 'to the current player'
        v, state = min(gen_enemy_score_state_pairs(state))
        initial_bid = state[-1]
        print 'initial bid:', initial_bid
        print

seek_counterexample()

state = ((28, 28, (10, 1, 2, 3, 4, 5, 6, 7, 8, 9), -1))
print state, 'is worth', evaluate(state), 'to the current player'

state = ((28, 28, (10, 1, 2, 3, 4, 5, 6, 7, 8, 9), 7))
print state, 'is worth', evaluate(state), 'to the current player'

state = ((28, 28, (10, 1, 2, 3, 4, 5, 6, 7, 8, 9), 8))
print state, 'is worth', evaluate(state), 'to the current player'

state = ((28, 28, (10, 1, 2, 3, 4, 5, 6, 7, 8, 9), 9))
print state, 'is worth', evaluate(state), 'to the current player'

state = ((28, 28, (10, 1, 2, 3, 4, 5, 6, 7, 8, 9), 10))
print state, 'is worth', evaluate(state), 'to the current player'


backtrace((8, 8, (5, 4, 3, 2, 1), -1))
#backtrace((8, 8, (5, 2, 4, 3, 1), -1))

#backtrace((8, 8, (5, 1, 2, 3, 4), -1))

#print evaluate((8, 8, (5, 4, 3, 2, 1), -1))
#print evaluate((8, 8, (5, 2, 4, 3, 1), -1))


class MinimaxTest(unittest.TestCase):

    def test_initial_win_a(self):
        """
        Check the expected gain.
        """
        observed = evaluate((8, 8, (5, 4, 3, 2, 1), -1))
        self.assertEqual(8, observed)

    def test_initial_win_b(self):
        """
        Check the expected gain.
        """
        observed = evaluate((8, 8, (5, 2, 4, 3, 1), -1))
        self.assertEqual(8, observed)

    def test_losing_state_a(self):
        """
        Assert a losing state.
        """
        observed = evaluate((8, 8, (5, 4, 3, 2, 1), 5))
        self.assertEqual(7, observed)

    def test_winning_state_a(self):
        """
        Check the expected gain.
        """
        observed = evaluate((8, 8, (5, 4, 3, 2, 1), 6))
        self.assertEqual(9, observed)

    def test_losing_state_b(self):
        """
        Check the expected gain.
        """
        observed = evaluate((8, 8, (5, 2, 4, 3, 1), 4))
        self.assertEqual(7, observed)


if __name__ == '__main__':
    unittest.main()
