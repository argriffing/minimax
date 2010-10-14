import itertools

# the game state is:
# * point advantage of current player
# * monies of current player
# * monies of enemy player
# * remaining sequence
# * current bid level

# End state is when remaining sequence is empty.
# The value of the end state is:
# * 1 if the current player point advantage is positive
# * 0 if the current player point advantage is zero
# * -1 if the current player point advantage is negative

# possible moves are:
# * pass
# * bid an integer greater than the current bid level
#   and at most the monies of the current player

# OR
# I could look at the game as
# the point value of the game to the person whose turn it is.
# In this case the board state is:
# * monies of current player
# * monies of enemy player
# * remaining sequence
# * current bid level
# A move consists of updating the board state, possibly yielding score

# Bid level:
# -2: you have to pass and increment bid level to -1
# -1: forfeit, or bid more than the bid level if possible
# >=0: forfeit, or bid more than the bid level if possible

g_cache = {}

def evaluate(state):
    c_mon, e_mon, seq, bid = state
    if not seq:
        return 0
    if state in g_cache:
        return g_cache[state]
    value = sum(seq) - min(gen_enemy_scores(state))
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

def gen_enemy_scores(state):
    for e_value, e_state in gen_enemy_states(state):
        yield e_value + evaluate(e_state)

def backtrace(state):
    print state, 'is worth', evaluate(state), 'to the current player'
    while True:
        print state
        c_mon, e_mon, seq, bid = state
        if not seq:
            break
        n_value_state_pairs = []
        for inc, n_state in gen_enemy_states(state):
            value = inc + evaluate(n_state)
            n_value_state_pairs.append((value, n_state))
        v, state = min(n_value_state_pairs)

def seek_counterexample():
    N = 10
    tsum = (N*(N+1))/2
    if tsum % 2 == 0:
        raise ValueError('sum of all scores should be odd')
    target = tsum - tsum/2
    print 'required score to win:', target
    for remainder in itertools.permutations(range(1,N)):
        seq = tuple([N] + list(remainder))
        state = (target, target, seq, -1)
        print state, 'is worth', evaluate(state), 'to the current player'
        n_value_state_pairs = []
        for inc, n_state in gen_enemy_states(state):
            value = inc + evaluate(n_state)
            n_value_state_pairs.append((value, n_state))
        v, state = min(n_value_state_pairs)
        initial_bid = state[-1]
        print 'initial bid:', initial_bid
        print

#seek_counterexample()

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


#backtrace((8, 8, (5, 4, 3, 2, 1), -1))
#print
#backtrace((8, 8, (5, 2, 4, 3, 1), -1))

#backtrace((8, 8, (5, 1, 2, 3, 4), -1))

#print evaluate((8, 8, (5, 4, 3, 2, 1), -1))
#print evaluate((8, 8, (5, 2, 4, 3, 1), -1))

#print g_cache
