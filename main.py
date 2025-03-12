from read_file import readFile
from Resource import Resource

class Main:
    def __init__(self, input_file):
        self.output_file = 'output '+input_file
        out = readFile(input_file)
        self.initialCapital = out[0]
        self.resourceInfo = out[1]
        self.turnsInfo = out[2]

        self.resources = [Resource(val) for val in self.resourceInfo]
        self.budget = self.initialCapital
        self.total_score = 0
        self.existingResources = []

        self.decisions = []

    def save_decisions(self):
        lines = []
        for decision in self.decisions:
            lines.append(" ".join([str(val) for val in decision])+"\n")
        with open(self.output_file, 'w') as f:
            f.writelines(lines)

    def play_game(self):
        for turn_info in self.turnsInfo:
            self.do_turn(turn_info)
        self.save_decisions()


    def do_turn(self, turn_info):
        self.buy_resources()
        # self.apply_periodic_cost()
        # self.apply_profit()
        turn_costs = self.calc_maintenance_cost()
        turn_profit = self.calc_profit(turn_info)
        self.budget = self.budget - turn_costs + turn_profit



    def buy_resources(self):
        newResources = []
        #### optimisation code in here somewhere

        newResources.append(self.resources[0])

        #### ------

        ## create all new resources
        cost = sum([res.RA for res in newResources])
        self.budget -= cost
        decision = [len(self.decisions), len(newResources)]
        for item in newResources:
            self.existingResources.append(item.recreate())
            decision.append(item.RI)
        self.decisions.append(decision)


    def calc_maintenance_cost(self):
        total = 0
        for resource in self.existingResources:
            total+=resource.get_maintenance_cost()
        return total

    def calc_profit(self, turn_info):
        powered_buildings = 0
        for resource in self.existingResources:
            powered_buildings += resource.get_powered_buildings()
        if powered_buildings < turn_info['TM']:
            return 0
        return min(powered_buildings, turn_info['TX']) * turn_info['TR']

if __name__ == "__main__":
    main = Main("0-demo.txt")
    main.play_game()