import random
from enum import IntEnum
import sys
import argparse

EPSILON = 0.9
MCTS_N = 3500

class Card:
    def __init__(self, color, rank, value):
        self.color = color
        self.rank = rank
        self.value = value
        
    def __str__(self):
        return self.rank + " of " + self.color
        
    def __eq__(self, other):
        return self.color == other.color and self.rank == other.rank

def generate_deck(suits=["Hearts", "Spades", "Clubs", "Diamonds"], 
                  ranks=[("2",2), ("3",3), ("4",4), ("5",5), ("6",6), ("7",7), ("8",8), ("9",9), ("10",10), ("Jack",10), ("Queen",10), ("King",10), ("Ace",11)]):
    result = []
    for suit in suits:
        for (rank,value) in ranks:
            result.append(Card(suit,rank,value))
    return result
    
def format(cards):
    if isinstance(cards, Card):
        return str(cards)
    return ", ".join(map(str, cards))
    
def get_value(cards):
    """
    Calculate the value of a set of cards. Aces may be counted as 11 or 1, to avoid going over 21
    """
    result = 0
    aces = 0
    for card in cards:
        result += card.value
        if card.rank == "Ace":
            aces += 1
    while result > 21 and aces > 0:
        result -= 10
        aces -= 1
    return result
    

class PlayerType(IntEnum):
    PLAYER = 1
    DEALER = 2
    
class Action(IntEnum):
    HIT = 1
    STAND = 2
    DOUBLE_DOWN = 3
    SPLIT = 4

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
    def get_action(self, cards, actions, dealer_cards):
        return random.choice(actions)
    def reset(self):
        pass
        
class TimidPlayer(Player):
    def get_action(self, cards, actions, dealer_cards):
        return Action.STAND
        
class BasicStrategyPlayer(Player):
    def get_action(self, cards, actions, dealer_cards):
        pval = get_value(cards)
        if dealer_cards[0].value < 7:
            if pval < 12:
                return Action.HIT 
            return Action.STAND 
        if pval < 17:
            return Action.HIT
        return Action.STAND
        
class RolloutPlayer(Player):
    def __init__(self, name, deck):
        self.name = name
        self.actions = []
        self.deck = deck
    def get_action(self, cards, actions, dealer_cards):
        act = random.choice(actions)
        self.actions.append(act)
        return act
    def reset(self):
        self.actions = []
        

class Node:
    def __init__(self, node, name):
        self.parent_node = node
        self.name = name
        self.children_nodes = []
        self.rounds = 0
        self.scores = []

    def getBestChildNode(self):
        highest_average = -10000
        node_selected = None
        for child in self.children_nodes:
            temp = sum(child.scores)/child.rounds
            if temp > highest_average:
                highest_average = temp
                node_selected = child
        return node_selected

    def getRandomChildNode(self):
        random_child = random.choice(self.children_nodes)
        return random_child



class Tree:
    def __init__(self, nodo):
        self.root = nodo

    def addChildren(self, actions, parent_node):
        for action in actions:
            child = Node(parent_node, action)
            parent_node.children_nodes.append(child)

class Tree_Climber(Player):
    def __init__(self, tree):
        self.current_node = tree.root
        self.tree = tree
        self.rollout_flag= False

    def selection_strategy(self, node):
        node_selected = None
        if( random.random() > EPSILON):
            node_selected = node.getBestChildNode()
        else:
            node_selected = node.getRandomChildNode()
        node_selected.rounds += 1
        return node_selected

    def rollback_strategy(self, departure_node, result):
        iterator = departure_node
        while(iterator.parent_node != None):
            iterator.scores.append(result)
            iterator = iterator.parent_node

    def get_action(self, cards, actions, dealer_cards):
        if(self.rollout_flag):
            return random.choice(actions)
        if len(self.current_node.children_nodes) == 0:
            self.tree.addChildren(actions, self.current_node)
        for child in self.current_node.children_nodes:
            if(child.rounds == 0):
                self.current_node = child
                child.rounds += 1
                self.rollout_flag = True
                return child.name
        self.current_node = self.selection_strategy(self.current_node)
        return self.current_node.name

    def reset(self):
        self.bet = 2
      

class MCTSPlayer(Player):
    def __init__(self, name, deck):
        self.name = name
        self.bet = 2
        self.deck = deck

    def get_action(self, cards, actions, dealer_cards):
        deck = self.deck[:]
        for p in cards:
            deck.remove(p)
        for p in dealer_cards:
            deck.remove(p)
        
        root = Node(None,"root")
        mcts_tree = Tree(root)
        mcts_tree.addChildren(actions, root)

        p = Tree_Climber(mcts_tree)
        BJ_simulator = Game(deck, p, verbose=False)

        for run in range(MCTS_N):
            result = BJ_simulator.continue_round(cards, dealer_cards, self.bet)
            p.rollback_strategy(p.current_node,result)
            p.current_node = mcts_tree.root
            p.rollout_flag = False

        best_action_result = mcts_tree.root.getBestChildNode().name
        
        return best_action_result

    def reset(self):
        self.bet = 2
        
class Dealer(Player):
    def __init__(self):
        self.name = "Dealer"
        
    def get_action(self, cards, actions, dealer_cards):
        if get_value(cards) < 17:
            return Action.HIT
        return Action.STAND
        
def same_rank(a, b):
    return a.rank == b.rank
    
def same_value(a, b):
    return a.value == b.value

class Game:
    def __init__(self, cards, player, split_rule=same_value, verbose=True):
        self.cards = cards 
        self.player = player
        self.dealer = Dealer()
        self.dealer_cards = []
        self.player_cards = []
        self.split_cards = []
        self.verbose = verbose
        self.split_rule = split_rule

    def round(self, contexto):
        self.deck = self.cards[:]
        random.shuffle(self.deck)
        self.dealer_cards = []
        self.player_cards = []
        self.bet = 2
        self.player.reset()
        self.dealer.reset()
        for i in range(2):
            self.deal(self.player_cards)
            self.deal(self.dealer_cards)
        return self.play_round(contexto)
        
        
    def continue_round(self, player_cards, dealer_cards, bet):
        self.deck = self.cards[:]
        random.shuffle(self.deck)
        self.bet = bet
        self.player_cards = player_cards[:] 
        self.dealer_cards = dealer_cards[:]
        while len(self.dealer_cards) < 2:
            self.deal(self.dealer_cards)
        return self.play_round()
        
    def play_round(self, contexto = False):
        if contexto:
            cards = self.play(self.player, self.player_cards,True, True)
        else:
             cards = self.play(self.player, self.player_cards)
        self.play(self.dealer, self.dealer_cards)
        reward = sum(self.reward(c) for c in cards)
        if self.verbose:
            print("played for", self.bet, "won", reward)
        return reward

    def deal(self, cards):
        card = self.deck[0]
        self.deck = self.deck[1:]
        cards.append(card)

    def play(self, player, cards, cansplit=True, contexto = False):
        while get_value(cards) < 21:
            actions = [Action.HIT, Action.STAND, Action.DOUBLE_DOWN]
            if len(cards) == 2 and cansplit and self.split_rule(cards[0], cards[1]):
                actions.append(Action.SPLIT)
            act = player.get_action(cards, actions, self.dealer_cards[:1])
            if act in actions:
                if self.verbose:
                    print(player.name, "Do", act)
                if act == Action.STAND:
                    break
                if act == Action.HIT or act == Action.DOUBLE_DOWN:
                    self.deal(cards)
                if act == Action.DOUBLE_DOWN:
                    self.bet *= 2
                    break
                if act == Action.SPLIT:
                    pilea = cards[:1]
                    pileb = cards[1:]
                    if (contexto):
                        p = RolloutPlayer(player.name, cards)
                        self.play(p, pilea, False)
                        self.play(p, pileb, False)
                    else:
                        self.play(player, pilea, False)
                        self.play(player, pileb, False)
                    
                    return [pilea, pileb]
        return [cards]

    def reward(self, player_cards):
        pscore = get_value(player_cards)
        dscore = get_value(self.dealer_cards)
        if self.verbose:
            print(self.player.name + ":", format(player_cards), pscore)
            print(self.dealer.name + ":", format(self.dealer_cards), dscore)
        
        if pscore > 21:
            return -self.bet
        result = -self.bet
        if pscore > dscore or dscore > 21:
            if pscore == 21 and len(self.player_cards) == 2:
                result = 3*self.bet/2
            result = self.bet
        if pscore == dscore and (pscore != 21 or len(self.player_cards) != 2):
            result = 0
        return result
        
        
player_types = {"default": Player, "timid": TimidPlayer, "basic": BasicStrategyPlayer, "mcts": MCTSPlayer}
deck_types = {"default": generate_deck(), "high": generate_deck(ranks=[("2", 2), ("10", 10), ("Ace", 11), ("Fool", 12)]),
              "low": generate_deck(ranks=[("1.5", 1.5), ("2", 2), ("3", 3), ("3", 4), ("Ace", 11)]),
              "even": generate_deck(ranks=[("2",2), ("4",4), ("6",6), ("8",8), ("10",10), ("Jack",10), ("Queen",10), ("King",10)]),
              "odd": generate_deck(ranks=[("3",3), ("5",5), ("7",7), ("9",9), ("Ace",11)]),
              "red": generate_deck(suits=["Diamonds", "Hearts"]),
              "random": generate_deck(ranks=random.sample([("2",2), ("3",3), ("4",4), ("5",5), ("6",6), ("7",7), ("8",8), ("9",9), ("10",10), ("Jack",10), ("Queen",10), ("King",10), ("Ace",11)], random.randint(5,13)))}
        
def main(ptype="default", dtype="default", n=100, split_rule=same_value, verbose=True):
    deck = deck_types[dtype]
    g = Game(deck, player_types[ptype]("Sir Gladington III, Esq.", deck[:]), split_rule, verbose)
    points = []
    for i in range(n):
        print(i)
        points.append(g.round(True))
    print("Average points: ", sum(points)*1.0/n)
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a simulation of a Blackjack agent.')
    parser.add_argument('player', nargs="?", default="default", 
                        help='the player type (available values: %s)'%(", ".join(player_types.keys())))
    parser.add_argument('-n', '--count', dest='count', action='store', default=100,
                        help='How many games to run')
    parser.add_argument('-s', '-q', '--silent', '--quiet', dest='verbose', action='store_const', default=True, const=False,
                        help='Do not print game output (only average score at the end is printed)')
    parser.add_argument('-r', '--rank', '--rank-split', dest='split', action='store_const', default=same_value, const=same_rank,
                        help="Only allow split when the player's cards have the same rank (default: allow split when they have the same value)")
    parser.add_argument('-d', "--deck", metavar='D', dest="deck", nargs=1, default=["default"], 
                        help='the deck type to use (available values: %s)'%(", ".join(deck_types.keys())))
    args = parser.parse_args()
    if args.player not in player_types:
        print("Invalid player type: %s. Available options are: \n%s"%(args.player, ", ".join(player_types.keys())))
        sys.exit(-1)
    if args.deck[0] not in deck_types:
        print("Invalid deck type: %s. Available options are: \n%s"%(args.deck, ", ".join(deck_types.keys())))
        sys.exit(-1)
    main(args.player, args.deck[0], int(args.count), args.split, args.verbose)
