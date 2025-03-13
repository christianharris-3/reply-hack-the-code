from read_file import readFile
import math

def get_max_score(file):
    t,resources, turns = readFile(file)

    max_houses_multiplier = 0
    profit_multiplier = 0
    for r in resources:
        if r['RT'] == 'B':
            max_houses_multiplier += max(0,r['RE'])
        elif r['RT'] == 'D':
            profit_multiplier += max(0,r['RE'])

    profit_multiplier*=5000
    max_houses_multiplier*=5000
    
    total = 0
    for t in turns:
        total += math.floor(t['TX']*(1+max_houses_multiplier/100))*math.floor(t['TR']*(1+profit_multiplier/100))
    return total

total_possible_score = 0
inputs = ["0-demo.txt", "1-thunberg.txt", "2-attenborough.txt", "4-maathai.txt",
          "6-earle.txt", "7-mckibben.txt" ,"8-shiva.txt"]
for inp in inputs:
    score = get_max_score("inputs/"+inp)
    print(f'max score for {inp.split(".")[0]} is {score}')
    total_possible_score+=score
print('total:',total_possible_score)
