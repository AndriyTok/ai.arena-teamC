import numpy as np
import json

# Unit types mapping
UNITS = ["Boar", "Chaos", "Dracula", "Slime", "Fire Mage", "Goblin", "Reaper", "Robed Spirit", "Skeleton"]
NUM_UNITS = len(UNITS)

class MarkovChainPredictor:
    def __init__(self):
        self.transition_matrix = np.full((NUM_UNITS, NUM_UNITS), 0.5)
        self.match_counts = np.zeros((NUM_UNITS, NUM_UNITS))
        
    def train(self, battles):
        for battle in battles:
            a, b, winner = battle['unit_a'], battle['unit_b'], battle['winner']
            self.match_counts[a, b] += 1
            if winner == 0:
                self.transition_matrix[a, b] = (
                    self.transition_matrix[a, b] * (self.match_counts[a, b] - 1) + 1
                ) / self.match_counts[a, b]
            else:
                self.transition_matrix[a, b] = (
                    self.transition_matrix[a, b] * (self.match_counts[a, b] - 1)
                ) / self.match_counts[a, b]
                
    def predict(self, unit_a, unit_b):
        return self.transition_matrix[unit_a, unit_b]
    
    def predict_team_battle(self, team_a, team_b):
        total_prob = 0
        for a in team_a:
            for b in team_b:
                total_prob += self.predict(a, b)
        return total_prob / (len(team_a) * len(team_b))
    
    def simulate_battle(self, unit_a, unit_b):
        prob_a = self.predict(unit_a, unit_b)
        return 0 if np.random.random() < prob_a else 1
    
    def get_stats(self):
        return {
            "model": "Markov Chain",
            "matrix_shape": self.transition_matrix.shape,
            "total_matches": int(self.match_counts.sum())
        }


def generate_synthetic_battles(n=1000):
    battles = []
    strengths = np.random.random((NUM_UNITS, NUM_UNITS))
    for _ in range(n):
        a, b = np.random.randint(0, NUM_UNITS, 2)
        prob_a = strengths[a, b] / (strengths[a, b] + strengths[b, a])
        winner = 0 if np.random.random() < prob_a else 1
        battles.append({'unit_a': a, 'unit_b': b, 'winner': winner})
    return battles, strengths


if __name__ == "__main__":
    model = MarkovChainPredictor()
    battles, _ = generate_synthetic_battles(500)
    model.train(battles)
    
    print("Markov Chain Predictor Demo")
    print("-" * 40)
    print(f"Trained on {len(battles)} battles")
    print(f"\nSample predictions:")
    for i in range(3):
        a, b = np.random.randint(0, NUM_UNITS, 2)
        prob = model.predict(a, b)
        print(f"  {UNITS[a]} vs {UNITS[b]}: {prob:.1%} chance A wins")
