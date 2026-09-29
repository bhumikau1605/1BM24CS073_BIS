import random
import math
import matplotlib.pyplot as plt
NUMBER_OF_STOPS = 12
POPULATION_SIZE = 100
GENERATIONS = 500
MUTATION_RATE = 0.03
MAP_SIZE = 100
RANDOM_SEED = None
if RANDOM_SEED is not None:
    random.seed(RANDOM_SEED)
def generate_bus_stops(number_of_stops):
    stops = {}
    stops["Depot"] = (MAP_SIZE // 2, MAP_SIZE // 2)
    for i in range(1, number_of_stops + 1):
        x = random.randint(0, MAP_SIZE)
        y = random.randint(0, MAP_SIZE)
        stops[f"Stop {i}"] = (x, y)
    return stops
def generate_demand(stops):
    demand = {}
    for stop in stops:
        if stop == "Depot":
            demand[stop] = 0
        else:
            demand[stop] = random.randint(5, 40)
    return demand
def distance(stop1, stop2):
    x1, y1 = stops[stop1]
    x2, y2 = stops[stop2]
    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )
def route_distance(route):
    total_distance = 0
    previous_stop = "Depot"
    for stop in route:
        total_distance += distance(
            previous_stop,
            stop
        )
        previous_stop = stop
    total_distance += distance(
        previous_stop,
        "Depot"
    )
    return total_distance
def route_demand(route):
    total_demand = 0
    for stop in route:
        total_demand += passenger_demand[stop]
    return total_demand
def create_population():
    population = []
    bus_stops = [
        stop for stop in stops
        if stop != "Depot"
    ]
    for _ in range(POPULATION_SIZE):
        route = bus_stops.copy()
        random.shuffle(route)
        population.append(route)
    return population
def fitness(route):
    total_distance = route_distance(route)
    return 1 / (total_distance + 0.0001)
def selection(population):
    tournament_size = 5
    tournament = random.sample(
        population,
        tournament_size
    )
    best_route = min(
        tournament,
        key=route_distance
    )
    return best_route
def crossover(parent1, parent2):
    length = len(parent1)
    start, end = sorted(
        random.sample(
            range(length),
            2
        )
    )
    child = [None] * length
    child[start:end] = parent1[start:end]
    position = end
    for stop in parent2:
        if stop not in child:
            if position >= length:
                position = 0
            child[position] = stop
            position += 1
    return child
def mutation(route):
    route = route.copy()
    if random.random() < MUTATION_RATE:
        index1, index2 = random.sample(
            range(len(route)),
            2
        )
        route[index1], route[index2] = (
            route[index2],
            route[index1]
        )
    return route
def genetic_algorithm():
    population = create_population()
    best_route = None
    best_distance = float("inf")
    history = []
    for generation in range(GENERATIONS):
        population.sort(
            key=route_distance
        )
        current_best = population[0]
        current_distance = route_distance(
            current_best
        )
        if current_distance < best_distance:
            best_distance = current_distance
            best_route = current_best.copy()
        history.append(best_distance)
        new_population = population[:10]
        while len(new_population) < POPULATION_SIZE:
            parent1 = selection(population)
            parent2 = selection(population)
            child = crossover(
                parent1,
                parent2
            )
            child = mutation(child)
            new_population.append(child)
        population = new_population
    return best_route, best_distance, history
def display_stops():
    print("\n")
    print("=" * 65)
    print("RANDOMLY GENERATED BUS STOPS")
    print("=" * 65)
    print(
        f"{'Stop':<12}"
        f"{'X':<10}"
        f"{'Y':<10}"
        f"{'Passengers':<15}"
    )
    print("-" * 65)
    for stop, location in stops.items():
        x, y = location
        print(
            f"{stop:<12}"
            f"{x:<10}"
            f"{y:<10}"
            f"{passenger_demand[stop]:<15}"
        )
def display_route(route):
    print("Depot", end="")
    for stop in route:
        print(
            f" → {stop}",
            end=""
        )
    print(" → Depot")
print("\n")
print("=" * 65)
print("       BUS ROUTE MANAGEMENT SYSTEM")
print("       GENETIC ALGORITHM OPTIMIZER")
print("=" * 65)
stops = generate_bus_stops(
    NUMBER_OF_STOPS
)
passenger_demand = generate_demand(
    stops
)
display_stops()
initial_route = [
    stop for stop in stops
    if stop != "Depot"
]
random.shuffle(initial_route)
initial_distance = route_distance(
    initial_route
)
print("\n")
print("=" * 65)
print("INITIAL RANDOM BUS ROUTE")
print("=" * 65)
display_route(initial_route)
print(
    f"\nInitial Route Distance: "
    f"{initial_distance:.2f} units"
)
print("\n")
print("Optimizing bus route...")
print(
    f"Population Size : {POPULATION_SIZE}"
)
print(
    f"Generations     : {GENERATIONS}"
)
print(
    f"Mutation Rate   : {MUTATION_RATE}"
)
best_route, best_distance, history = (
    genetic_algorithm()
)
improvement = (
    (initial_distance - best_distance)
    / initial_distance
) * 100
print("\n")
print("=" * 65)
print("OPTIMIZED BUS ROUTE")
print("=" * 65)
display_route(best_route)
print("\n")
print(
    f"Initial Distance     : "
    f"{initial_distance:.2f} units"
)
print(
    f"Optimized Distance   : "
    f"{best_distance:.2f} units"
)
print(
    f"Distance Reduced     : "
    f"{initial_distance - best_distance:.2f} units"
)
print(
    f"Improvement          : "
    f"{improvement:.2f}%"
)
print(
    f"Total Passenger Demand: "
    f"{route_demand(best_route)}"
)
print("\n")
print("=" * 65)
print("OPTIMIZED ROUTE DETAILS")
print("=" * 65)
print(
    f"{'Sequence':<10}"
    f"{'Stop':<15}"
    f"{'Passengers':<15}"
    f"{'Distance From Previous':<25}"
)
print("-" * 65)
previous = "Depot"
for index, stop in enumerate(best_route, start=1):
    segment_distance = distance(
        previous,
        stop
    )
    print(
        f"{index:<10}"
        f"{stop:<15}"
        f"{passenger_demand[stop]:<15}"
        f"{segment_distance:<25.2f}"
    )
    previous = stop
route_for_plot = (
    ["Depot"] +
    best_route +
    ["Depot"]
)
x_values = [
    stops[stop][0]
    for stop in route_for_plot
]
y_values = [
    stops[stop][1]
    for stop in route_for_plot
]
plt.figure(figsize=(10, 8))
plt.plot(
    x_values,
    y_values,
    marker="o",
    linewidth=2
)
for stop in route_for_plot:
    x, y = stops[stop]
    plt.annotate(
        stop,
        (x, y),
        xytext=(5, 5),
        textcoords="offset points"
    )
plt.title(
    "Optimized Bus Route - Genetic Algorithm"
)
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.grid(True)
plt.tight_layout()
plt.show()
plt.figure(figsize=(10, 6))
plt.plot(
    range(1, GENERATIONS + 1),
    history
)
plt.title(
    "Genetic Algorithm Convergence"
)
plt.xlabel("Generation")
plt.ylabel("Best Route Distance")
plt.grid(True)
plt.tight_layout()
plt.show()