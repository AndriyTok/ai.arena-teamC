import numpy as np
import matplotlib.pyplot as plt

from markov_chain import MarkovChainPredictor
from monte_carlo import MonteCarloPredictor, UNITS, NUM_UNITS
from neural_network import NeuralNetworkPredictor, generate_synthetic_battles


def compare_models(n_training=500, n_battles=100):
    """Train models and battle them against each other"""
    print("Generating training data...")
    training_battles, _ = generate_synthetic_battles(n_training)
    
    markov = MarkovChainPredictor()
    markov.train(training_battles)
    
    nn = NeuralNetworkPredictor(hidden_size=16, lr=0.05)
    nn.train(training_battles, epochs=50, verbose=False)
    
    mcts = MonteCarloPredictor(simulations=30)
        
    results = {
        "Markov vs NN": {"Markov": 0, "NN": 0},
        "Markov vs MC": {"Markov": 0, "MC": 0},
        "NN vs MC": {"NN": 0, "MC": 0},
    }
    
    for i in range(n_battles):
        team_a = np.random.randint(0, NUM_UNITS, 3).tolist()
        team_b = np.random.randint(0, NUM_UNITS, 3).tolist()
        
        m_pred = markov.predict_team_battle(team_a, team_b)
        n_pred = nn.predict_team_battle(team_a, team_b)
        mc_pred = mcts.predict(team_a, team_b)
        
        actual = np.random.random() < 0.5 
        
        m_correct = (m_pred > 0.5) == actual
        n_correct = (n_pred > 0.5) == actual
        if m_correct and not n_correct:
            results["Markov vs NN"]["Markov"] += 1
        elif n_correct and not m_correct:
            results["Markov vs NN"]["NN"] += 1
        
        mc_correct = (mc_pred > 0.5) == actual
        if m_correct and not mc_correct:
            results["Markov vs MC"]["Markov"] += 1
        elif mc_correct and not m_correct:
            results["Markov vs MC"]["MC"] += 1
        
        if n_correct and not mc_correct:
            results["NN vs MC"]["NN"] += 1
        elif mc_correct and not n_correct:
            results["NN vs MC"]["MC"] += 1
    
    print("BATTLE RESULTS (Model vs Model)")
    
    for matchup, scores in results.items():
        names = list(scores.keys())
        print(f"\n{matchup}:")
        print(f"  {names[0]}: {scores[names[0]]} wins")
        print(f"  {names[1]}: {scores[names[1]]} wins")
        winner = names[0] if scores[names[0]] > scores[names[1]] else names[1]
        print(f"  Winner: {winner}")
    
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    colors = [['#4CAF50', '#2196F3'], ['#4CAF50', '#FF9800'], ['#2196F3', '#FF9800']]
    for idx, (matchup, scores) in enumerate(results.items()):
        ax = axes[idx]
        names = list(scores.keys())
        vals = list(scores.values())
        ax.bar(names, vals, color=colors[idx])
        ax.set_title(matchup)
        ax.set_ylabel('Wins')
        for j, v in enumerate(vals):
            ax.text(j, v + 1, str(v), ha='center', fontweight='bold')
    
    plt.suptitle(f'Model vs Model ({n_battles} battles each)', fontsize=14)
    plt.tight_layout()
    plt.savefig('model_battles.png', dpi=100)
    print("\nSaved: model_battles.png")
    plt.show()


if __name__ == "__main__":
    compare_models()
