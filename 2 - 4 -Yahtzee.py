"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """    
    if len(hand) == 0:
        return 0
    
    else:
        clone_dice = list(hand)
        scores = []
        newscore = 0
        for dice in clone_dice:
            newscore = clone_dice.count(dice) * dice
            scores.append(newscore)
            
        scores.sort(reverse = True)
        highest_score = scores[0]

            
    return highest_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    outcomes = []
    for index in range(num_die_sides):
        outcomes.append(index + 1)
    
    all_seqs = gen_all_sequences(outcomes, num_free_dice)
    
    totalscore = 0.0
    for sequence in all_seqs:
        for dice in held_dice:
            sequence = sequence + (dice,)
        totalscore += float(score(sequence))
    
    expect_value = totalscore / len(all_seqs)
    return expect_value


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    answer_set = set([()])
    binary = gen_all_sequences((0, 1), len(hand))
    
    for bin_item in binary:
        temp_set = ()
        for char in range(len(bin_item)):
            if bin_item[char] == 1:
                temp_set = temp_set + (hand[char],)
        answer_set.add(tuple(temp_set))
    return answer_set


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    max_value = 0
    max_value_shit = ()
    for hold in all_holds:
        expected = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if  expected > max_value:
            max_value = expected
            max_value_shit = hold
    return (max_value, max_value_shit)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()






