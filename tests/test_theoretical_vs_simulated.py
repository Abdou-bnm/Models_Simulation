from src.simulate_mm1 import simulate_mm1
from src.analysis_utils import theoretical_mm1_metrics

def test_mm1_theory_match():
    lam = 0.5
    mu = 1.0
    sim = simulate_mm1(lambda_rate=lam, mu_rate=mu, num_customers=100000, seed=42)
    theory = theoretical_mm1_metrics(lam, mu)
    error_margin = 0.05 

    assert abs(sim["avg_response_time"] - theory["avg_response_time"]) < error_margin, "Response time mismatch"
    assert abs(sim["avg_waiting_time"] - theory["avg_waiting_time"]) < error_margin, "Waiting time mismatch"
    print("M/M/1 simulation-theory agreement test passed.")

if __name__ == "__main__":
    test_mm1_theory_match()
