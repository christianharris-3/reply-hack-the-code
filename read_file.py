

def read_file(filename):
    # load file
    with open(filename,'r') as f:
        lines = f.readlines()
    # split file into a 2d list
    data = []
    for line in lines:
        data.append([])
        for item in line.split():
            try:
                item = int(item)
            except:
                pass
            data[-1].append(item)

    # sort data into individual variables
    initial_capital = data[0][0]
    available_resources = data[0][1]
    game_turns = data[0][2]

    resource_info = []
    for resources in data[1:available_resources+1]:
        resource_info.append({
            'RI': resources[0],
            'RA': resources[1],
            'RP': resources[2],
            'RW': resources[3],
            'RM': resources[4],
            'RL': resources[5],
            'RU': resources[6],
            'RT': resources[7],
        })
        if len(resources) > 8:
            resource_info[-1]['RE'] = resources[8]

    turns_info = []
    for turn in data[available_resources+1:available_resources+1+game_turns]:
        turns_info.append({
            'TM': turn[0],
            'TX': turn[0],
            'TR': turn[0],
        })

    return initial_capital, resource_info, turns_info

if __name__ == "__main__":
    print(read_file("0-demo.txt"))
