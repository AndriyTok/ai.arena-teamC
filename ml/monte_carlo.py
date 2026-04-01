import numpy as np
import math
from collections import defaultdict

UNITS = ["Boar", "Chaos", "Dracula", "Slime", "Fire Mage", "Goblin", "Reaper", "Robed Spirit", "Skeleton"]
NUM_UNITS = len(UNITS)


class BattleState:
    """Simple battle state representation"""
    def __init__(self, team_a_hp, team_b_hp):
        self.team_a_hp = list(team_a_hp)
        self.team_b_hp = list(team_b_hp)
        
    def clone(self):
        return BattleState(self.team_a_hp.copy(), self.team_b_hp.copy())
    
    def is_terminal(self):
        return sum(self.team_a_hp) <= 0 or sum(self.team_b_hp) <= 0
    
    def get_winner(self):
        if sum(self.team_a_hp) <= 0:
            return 1 
        if sum(self.team_b_hp) <= 0:
            return 0 
        return -1  
    
    def get_actions(self, is_team_a):
        targets = self.team_b_hp if is_team_a else self.team_a_hp
        return [i for i, hp in enumerate(targets) if hp > 0]
    
    def apply_action(self, attacker_team_a, attacker_idx, target_idx, damage):
        if attacker_team_a:
            self.team_b_hp[target_idx] = max(0, self.team_b_hp[target_idx] - damage)
        else:
            self.team_a_hp[target_idx] = max(0, self.team_a_hp[target_idx] - damage)


class MCTSNode:
    def __init__(self, state, parent=None, action=None, is_team_a_turn=True):
        self.state = state
        self.parent = parent
        self.action = action
        self.is_team_a_turn = is_team_a_turn
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_actions = state.get_actions(is_team_a_turn) if not state.is_terminal() else []
        
    def ucb1(self, exploration=1.41):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + exploration * math.sqrt(math.log(self.parent.visits) / self.visits)
    
    def best_child(self):
        return max(self.children, key=lambda c: c.ucb1())
    
    def expand(self):
        action = self.untried_actions.pop()
        new_state = self.state.clone()
        damage = np.random.randint(5, 15)
        new_state.apply_action(self.is_team_a_turn, 0, action, damage)
        child = MCTSNode(new_state, self, action, not self.is_team_a_turn)
        self.children.append(child)
        return child


class MonteCarloPredictor:
    def __init__(self, simulations=100):
        self.simulations = simulations
        self.results_cache = {}
        
    def simulate_random_playout(self, state, is_team_a_turn):
        state = state.clone()
        turn = is_team_a_turn
        
        while not state.is_terminal():
            actions = state.get_actions(turn)
            if not actions:
                break
            target = np.random.choice(actions)
            damage = np.random.randint(5, 15)
            state.apply_action(turn, 0, target, damage)
            turn = not turn
            
        return state.get_winner()
    
    def mcts_search(self, initial_state, is_team_a=True):
        root = MCTSNode(initial_state.clone(), is_team_a_turn=is_team_a)
        
        for _ in range(self.simulations):
            node = root
            
            # Selection
            while node.untried_actions == [] and node.children:
                node = node.best_child()
            
            # Expansion
            if node.untried_actions:
                node = node.expand()
            
            # Simulation
            winner = self.simulate_random_playout(node.state, node.is_team_a_turn)
            
            # Backpropagation
            while node:
                node.visits += 1
                if winner == 0:  # Team A won
                    node.wins += 1
                node = node.parent
        
        return root.wins / root.visits if root.visits > 0 else 0.5
    
    def predict(self, team_a_units, team_b_units, team_a_hp=None, team_b_hp=None):
        if team_a_hp is None:
            team_a_hp = [100] * len(team_a_units)
        if team_b_hp is None:
            team_b_hp = [100] * len(team_b_units)
            
        state = BattleState(team_a_hp, team_b_hp)
        return self.mcts_search(state)
    
    def simulate_battle(self, team_a_units, team_b_units):
        prob_a = self.predict(team_a_units, team_b_units)
        return 0 if np.random.random() < prob_a else 1
    
    def get_stats(self):
        return {
            "model": "Monte Carlo Tree Search",
            "simulations_per_predict": self.simulations
        }


def run_tournament(predictor, n_battles=100):
    wins_a = 0
    for _ in range(n_battles):
        team_a = np.random.randint(0, NUM_UNITS, 3).tolist()
        team_b = np.random.randint(0, NUM_UNITS, 3).tolist()
        winner = predictor.simulate_battle(team_a, team_b)
        if winner == 0:
            wins_a += 1
    return wins_a / n_battles


if __name__ == "__main__":
    print("Monte Carlo Tree Search Demo")
    print("\n")    
    predictor = MonteCarloPredictor(simulations=50)
    
    team_a = [0, 1, 2]  # Boar, Chaos, Dracula
    team_b = [3, 4, 5]  # Slime, Fire Mage, Goblin
    
    prob = predictor.predict(team_a, team_b)
    print(f"Team A ({[UNITS[i] for i in team_a]})")
    print(f"Team B ({[UNITS[i] for i in team_b]})")
    print(f"Predicted win rate for Team A: {prob:.1%}")
    
    print(f"\nRunning tournament")
    win_rate = run_tournament(predictor, 50)
    print(f"Team A win rate over 50 battles: {win_rate:.1%}")
