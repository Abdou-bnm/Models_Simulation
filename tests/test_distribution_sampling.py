import numpy as np

def test_uniform_interarrival():
    samples = [np.random.uniform(0.5, 1.5) for _ in range(10000)]
    mean = np.mean(samples)
    assert 0.95 <= mean <= 1.05, f"Unexpected uniform mean: {mean}"

def test_weibull_service():
    samples = [np.random.weibull(2) for _ in range(10000)]
    mean = np.mean(samples)
    assert 0.85 <= mean <= 1.15, f"Unexpected Weibull mean: {mean}"

if __name__ == "__main__":
    test_uniform_interarrival()
    test_weibull_service()
    print("Distribution sampling tests passed.")
