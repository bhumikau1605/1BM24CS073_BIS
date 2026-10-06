import random
import numpy as np
def compute_total_delay(signal_times, arrival_rates, saturation_flows):
    total_delay = 0.0
    cycle_time = sum(signal_times)
    for arrival, saturation, green in zip(arrival_rates, saturation_flows, signal_times):
        if green <= 0:
            return float('inf')
        red_time = cycle_time - green
        capacity_ratio = arrival / (saturation * (green / cycle_time))
        if capacity_ratio >= 1.0:
            delay = 999999.0 
        else:
            delay = (arrival * red_time**2) / (2 * (1 - arrival / saturation))
        total_delay += delay
    return total_delay
class Particle:
    def __init__(self, dim, min_val, max_val):
        self.position = np.random.uniform(min_val, max_val, dim)
        self.velocity = np.random.uniform(-1.0, 1.0, dim)
        self.best_position = np.copy(self.position)
        self.best_fitness = float('inf')
        self.fitness = float('inf')
    def update_fitness(self, arrival_rates, saturation_flows):
        self.fitness = compute_total_delay(self.position, arrival_rates, saturation_flows)
        if self.fitness < self.best_fitness:
            self.best_fitness = self.fitness
            self.best_position = np.copy(self.position)
def optimize_traffic_signals(arrival_rates, saturation_flows, min_green=10, max_green=60, 
                             pop_size=30, max_iter=100, w=0.5, c1=1.5, c2=1.5):
    dim = len(arrival_rates)
    swarm = [Particle(dim, min_green, max_green) for _ in range(pop_size)]
    gbest_position = np.zeros(dim)
    gbest_fitness = float('inf')
    for particle in swarm:
        particle.update_fitness(arrival_rates, saturation_flows)
        if particle.fitness < gbest_fitness:
            gbest_fitness = particle.fitness
            gbest_position = np.copy(particle.best_position)
    for iteration in range(max_iter):
        for particle in swarm:
            r1 = np.random.rand(dim)
            r2 = np.random.rand(dim)
            particle.velocity = (w * particle.velocity + 
                                 c1 * r1 * (particle.best_position - particle.position) + 
                                 c2 * r2 * (gbest_position - particle.position))
            particle.position += particle.velocity
            particle.position = np.clip(particle.position, min_green, max_green)
            particle.update_fitness(arrival_rates, saturation_flows)
            if particle.fitness < gbest_fitness:
                gbest_fitness = particle.fitness
                gbest_position = np.copy(particle.best_position)
    return gbest_position, gbest_fitness
if __name__ == "__main__":
    print("--- Generating Random Traffic Scenario ---")
    num_phases = random.randint(3, 6)
    arrival_rates = [round(random.uniform(0.1, 0.6), 2) for _ in range(num_phases)]
    saturation_flows = [round(random.uniform(1.0, 2.0), 2) for _ in range(num_phases)]
    print(f"Number of Phases detected: {num_phases}")
    for i in range(num_phases):
        print(f"  Phase {i+1} -> Arrival Rate: {arrival_rates[i]} veh/s | Saturation Flow: {saturation_flows[i]} veh/s")
    print("\n--- Running Particle Swarm Optimization ---")
    best_greens, min_delay = optimize_traffic_signals(arrival_rates, saturation_flows)
    print("Optimization Complete!")
    print(f"Optimal Green Light Durations (seconds): {np.round(best_greens, 2)}")
    print(f"Total Combined Optimal Cycle Time: {np.round(sum(best_greens), 2)} seconds")
    print(f"Minimized Traffic Delay Score: {np.round(min_delay, 2)}")
