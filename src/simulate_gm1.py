import numpy as np

def simulate_gm1(lambda_rate, mu_rate, num_customers, inter_arrival_func, seed=None):
    """
    Simulate a G/M/1 queue where arrivals follow a general distribution (provided),
    and service times are exponential. Uses numpy.random.default_rng for clean RNG.

    Parameters:
    - lambda_rate: Arrival rate (λ)
    - mu_rate: Service rate (μ)
    - num_customers: Number of customers to simulate
    - inter_arrival_func: Function (lambda_rate, rng) -> float
    - seed: Optional seed for reproducibility

    Returns:
    - Dictionary with average waiting time, response time, and utilization
    """
    rng = np.random.default_rng(seed)

    clock = 0.0
    next_arrival = inter_arrival_func(lambda_rate, rng)
    next_departure = float('inf')
    queue = []
    busy = False

    total_wait_time = 0.0
    total_response_time = 0.0
    total_service_time = 0.0
    busy_time = 0.0
    num_served = 0
    last_event_time = 0.0

    while num_served < num_customers:
        if next_arrival < next_departure:
            time_elapsed = next_arrival - last_event_time
            if busy:
                busy_time += time_elapsed

            clock = next_arrival
            if busy:
                queue.append(clock)
            else:
                busy = True
                service_time = rng.exponential(1 / mu_rate)
                next_departure = clock + service_time
                total_service_time += service_time
                total_response_time += service_time

            next_arrival = clock + inter_arrival_func(lambda_rate, rng)
        else:
            time_elapsed = next_departure - last_event_time
            if busy:
                busy_time += time_elapsed

            clock = next_departure
            num_served += 1

            if queue:
                arrival_time = queue.pop(0)
                wait_time = clock - arrival_time
                total_wait_time += wait_time
                service_time = rng.exponential(1 / mu_rate)
                next_departure = clock + service_time
                total_service_time += service_time
                total_response_time += (wait_time + service_time)
            else:
                busy = False
                next_departure = float('inf')

        last_event_time = clock

    avg_waiting_time = total_wait_time / num_served
    avg_response_time = total_response_time / num_served
    utilization = busy_time / clock

    return {
        "lambda": lambda_rate,
        "mu": mu_rate,
        "avg_waiting_time": avg_waiting_time,
        "avg_response_time": avg_response_time,
        "utilization": utilization
    }
