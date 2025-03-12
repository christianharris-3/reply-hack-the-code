import sys

def read_input(filename):
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    
    # Read initial parameters
    D, R, T = map(int, lines[0].split())
    resources = []
    
    # Read resource details
    for i in range(1, R + 1):
        data = lines[i].split()
        RI, RA, RP, RW, RM, RL, RU = map(int, data[:7])
        RT = data[7]
        RE = int(data[8]) if len(data) > 8 else 0
        resources.append([RI, RA, RP, RW, RM, RL, RU, RT, RE])
    
    # Read turn details
    turns = [tuple(map(int, line.split())) for line in lines[R + 1:]]
    
    return D, resources, turns

def select_resources(D, resources, turns):
    decisions = []
    active_resources = []
    resource_lifetimes = {}  # Track how long each resource remains active
    total_score = 0  # Optimized score based on profit formula
    
    for t in range(len(turns)):
        TM, TX, TR = turns[t]

        if t % 100 == 0:
            print(t)
        
        buildings_powered = sum(r[6] for r in active_resources)
        
        # Remove expired resources
        expired_resources = [r for r in active_resources if resource_lifetimes.get(r[0], 0) == 1]
        active_resources = [r for r in active_resources if resource_lifetimes.get(r[0], 0) > 1]
        for r in active_resources:
            resource_lifetimes[r[0]] -= 1
        
        # Prioritize resources that maximize long-term profit
        affordable_resources = sorted(
            [r for r in resources if r[1] <= D],
            key=lambda x: (x[6] * TR * x[5]) / (x[1] + x[2]),  # Maximizing long-term profit
            reverse=True
        )
        
        chosen = []
        
        # Buy new resources if budget allows and more power is needed
        while affordable_resources and D >= affordable_resources[0][1]:
            best_resource = affordable_resources.pop(0)
            maintenance_cost = sum(r[2] for r in active_resources) + best_resource[2]
            if D >= best_resource[1] and D - best_resource[1] >= maintenance_cost:
                D -= best_resource[1]
                chosen.append(best_resource[0])
                active_resources.append(best_resource)
                resource_lifetimes[best_resource[0]] = best_resource[5]  # Track lifespan
                buildings_powered += best_resource[6]
            else:
                break  # Stop purchasing if future maintenance costs cannot be covered
        
        # Record the turn
        if chosen:
            decisions.append(f"{t} {len(chosen)} " + " ".join(map(str, chosen)))
        else:
            decisions.append(f"{t} 0")
        
        # Deduct maintenance costs after purchases, but ensure budget doesn’t go negative
        maintenance_cost = sum(r[2] for r in active_resources)
        # Compute profit from current resources
        
        profit = min(buildings_powered, TX) * TR
        total_score += profit

        D += profit
        if D >= maintenance_cost:
            D -= maintenance_cost
        else:
            raise ValueError("Budget cannot cover maintenance costs.")
        
    print(f"Final Optimized Score: {total_score}")  # Debug output
    return decisions

def write_output(filename, decisions):
    with open(filename, 'w') as f:
        f.write('\n'.join(decisions) + '\n')

def main(input_file, output_file):
    D, resources, turns = read_input(input_file)
    decisions = select_resources(D, resources, turns)
    write_output(output_file, decisions)

if __name__ == "__main__":
    input_file = "8-shiva.txt"  # Only process shiva.txt
    output_file = "8-shiva-output.txt"
    print(input_file, output_file)  # Example output file
    main(input_file, output_file)






