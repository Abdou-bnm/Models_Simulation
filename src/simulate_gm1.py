import numpy as np

def simulate_gm1(lambda_rate, mu_rate, num_customers, inter_arrival_func, seed=None):
    """
    Simulate a G/M/1 queue where arrivals follow a general distribution (provided),
    and service times are exponential.

    Parameters:
    - lambda_rate: Mean arrival rate (used for reference only)
    - mu_rate: Service rate (μ)
    - num_customers: Number of customers to simulate
    - inter_arrival_func: Function generating inter-arrival times (e.g., np.random.uniform)
    - seed: Optional random seed

    Returns:
    - metrics: Dictionary with average waiting/response times and utilization
    """
    if seed is not None:
        np.random.seed(seed)

    clock = 0.0
    next_arrival = inter_arrival_func()
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
            clock = next_arrival
            if busy:
                queue.append(clock)
            else:
                busy = True
                service_time = np.random.exponential(1 / mu_rate)
                next_departure = clock + service_time
                total_service_time += service_time
                total_response_time += service_time
                busy_time += (clock - last_event_time)
            next_arrival = clock + inter_arrival_func()
        else:
            clock = next_departure
            num_served += 1
            if queue:
                arrival_time = queue.pop(0)
                wait_time = clock - arrival_time
                total_wait_time += wait_time
                service_time = np.random.exponential(1 / mu_rate)
                next_departure = clock + service_time
                total_service_time += service_time
                total_response_time += (wait_time + service_time)
                busy_time += (clock - last_event_time)
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
