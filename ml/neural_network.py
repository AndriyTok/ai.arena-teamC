import numpy as np

UNITS = ["Boar", "Chaos", "Dracula", "Slime", "Fire Mage", "Goblin", "Reaper", "Robed Spirit", "Skeleton"]
NUM_UNITS = len(UNITS)


class SimpleNeuralNetwork:
    def __init__(self, input_size=NUM_UNITS * 2, hidden_size=16, lr=0.01):
        self.lr = lr
        self.W1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros(hidden_size)
        self.W2 = np.random.randn(hidden_size, 1) * 0.1
        self.b2 = np.zeros(1)
        self.losses = []
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2
    
    def backward(self, X, y):
        m = X.shape[0]
        
        dz2 = self.a2 - y.reshape(-1, 1)
        dW2 = self.a1.T @ dz2 / m
        db2 = np.mean(dz2, axis=0)
        
        da1 = dz2 @ self.W2.T
        dz1 = da1 * (self.z1 > 0)
        dW1 = X.T @ dz1 / m
        db1 = np.mean(dz1, axis=0)
        
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
        
    def compute_loss(self, y_pred, y_true):
        eps = 1e-7
        y_true = y_true.reshape(-1, 1)
        return -np.mean(y_true * np.log(y_pred + eps) + (1 - y_true) * np.log(1 - y_pred + eps))


class NeuralNetworkPredictor:
    def __init__(self, hidden_size=16, lr=0.01):
        self.model = SimpleNeuralNetwork(NUM_UNITS * 2, hidden_size, lr)
        self.trained = False
        
    def encode_matchup(self, unit_a, unit_b):
        vec = np.zeros(NUM_UNITS * 2)
        vec[unit_a] = 1
        vec[NUM_UNITS + unit_b] = 1
        return vec
    
    def train(self, battles, epochs=100, verbose=True):
        X = np.array([self.encode_matchup(b['unit_a'], b['unit_b']) for b in battles])
        y = np.array([1 - b['winner'] for b in battles])  # 1 if A wins, 0 if B wins
        
        for epoch in range(epochs):
            y_pred = self.model.forward(X)
            loss = self.model.compute_loss(y_pred, y)
            self.model.losses.append(loss)
            
            self.model.backward(X, y)
            
            if verbose and (epoch + 1) % 20 == 0:
                acc = np.mean((y_pred.flatten() > 0.5) == y)
                print(f"Epoch {epoch+1}/{epochs}, Loss: {loss:.4f}, Accuracy: {acc:.1%}")
        
        self.trained = True
        
    def predict(self, unit_a, unit_b):
        X = self.encode_matchup(unit_a, unit_b).reshape(1, -1)
        return float(self.model.forward(X)[0, 0])
    
    def predict_team_battle(self, team_a, team_b):
        total = 0
        for a in team_a:
            for b in team_b:
                total += self.predict(a, b)
        return total / (len(team_a) * len(team_b))
    
    def simulate_battle(self, unit_a, unit_b):
        prob = self.predict(unit_a, unit_b)
        return 0 if np.random.random() < prob else 1
    
    def get_stats(self):
        return {
            "model": "Neural Network",
            "hidden_size": self.model.W1.shape[1],
            "trained": self.trained,
            "final_loss": self.model.losses[-1] if self.model.losses else None
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
    print("Neural Network Predictor")
    
    battles, _ = generate_synthetic_battles(500)
    
    predictor = NeuralNetworkPredictor(hidden_size=16, lr=0.05)
    predictor.train(battles, epochs=100)
    
    print(f"\nSample predictions:")
    for _ in range(3):
        a, b = np.random.randint(0, NUM_UNITS, 2)
        prob = predictor.predict(a, b)
        print(f"  {UNITS[a]} vs {UNITS[b]}: {prob:.1%} chance A wins")
