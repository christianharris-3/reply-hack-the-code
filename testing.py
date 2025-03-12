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
        
        # Compute profit from current resources
        buildings_powered = sum(r[6] for r in active_resources)
        profit = min(buildings_powered, TX) * TR
        total_score += profit
        D += profit  # Add profit to budget before making purchases
        
        # Remove expired resources
        expired_resources = [r for r in active_resources if resource_lifetimes.get(r[0], 0) == 1]
        active_resources = [r for r in active_resources if resource_lifetimes.get(r[0], 0) > 1]
        for r in active_resources:
            resource_lifetimes[r[0]] -= 1
        
        # Prioritize resources that maximize `RU * TR` to increase score
        affordable_resources = sorted(
            [r for r in resources if r[1] <= D],
            key=lambda x: (x[6] * TR / (x[1] + 1)) * x[5],  # Maximizing contribution to score and lifespan
            reverse=True
        )
        
        chosen = []
        
        # Buy new resources if budget allows and more power is needed
        while affordable_resources and D >= affordable_resources[0][1]:
            best_resource = affordable_resources.pop(0)
            if D >= best_resource[1]:
                D -= best_resource[1]
                chosen.append(best_resource[0])
                active_resources.append(best_resource)
                resource_lifetimes[best_resource[0]] = best_resource[5]  # Track lifespan
                buildings_powered += best_resource[6]
        
        # Record the turn
        if chosen:
            decisions.append(f"{t} {len(chosen)} " + " ".join(map(str, chosen)))
        else:
            decisions.append(f"{t} 0")
        
        # Deduct maintenance costs after purchases, but ensure budget doesn’t go negative
        maintenance_cost = sum(r[2] for r in active_resources)
        D = max(0, D - maintenance_cost)
        
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
    inputs = ["0-demo.txt", "1-thunberg.txt", "2-attenborough.txt", "4-maathai.txt", "6-earle.txt", "8-shiva.txt"]
    for each in inputs:
        input_file = each  # Example input file
        output_file = each.rsplit(".",1)[0] + "output.txt"
        print(input_file, output_file)  # Example output file
        main(input_file, output_file)






