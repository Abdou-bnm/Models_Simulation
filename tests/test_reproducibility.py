from src.simulate_mm1 import simulate_mm1

def test_reproducibility():
    result1 = simulate_mm1(lambda_rate=0.6, mu_rate=1.0, num_customers=50000, seed=123)
    result2 = simulate_mm1(lambda_rate=0.6, mu_rate=1.0, num_customers=50000, seed=123)
    assert result1 == result2, "Results with same seed should be identical"
    print("Reproducibility test passed.")

if __name__ == "__main__":
    test_reproducibility()
