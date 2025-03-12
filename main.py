from read_file import readFile
from Resource import Resource
import math

class Main:
    def __init__(self, input_file):
        self.output_file = 'outputs/output '+input_file.split("/")[-1]
        out = readFile(input_file)
        self.initialCapital = out[0]
        self.resourceInfo = out[1]
        self.turnsInfo = out[2]

        self.resources = [Resource(val) for val in self.resourceInfo]
        self.budget = self.initialCapital
        self.total_score = 0
        self.existingResources = []
        self.turns_index = -1

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
        self.turns_index += 1
        self.manage_resources()
        self.buy_resources()
        turn_costs = self.calc_maintenance_cost()
        turn_profit = self.calc_profit(turn_info)
        self.budget = self.budget - turn_costs + turn_profit

    def manage_resources(self):
        remove_list = []
        for item in self.existingResources:
            item.update_turns()
            if item.get_out_of_life():
                remove_list.append(item)
        for rem in remove_list:
            self.existingResources.remove(rem)

    def buy_resources(self):
        newResources = []
        #### optimisation code in here somewhere

        # if self.budget > 5:
        #     newResources.append(self.resources[1])

        #### ------

        #### create all new resources
        # cut resources that cost too much
        get_cost = lambda resources: sum([res.RA for res in resources])
        while self.budget < get_cost(newResources) and len(newResources) > 0:
            del newResources[0]

        # apply decisions
        self.budget -= get_cost(newResources)
        decision = [self.turns_index, len(newResources)]
        for item in newResources:
            self.existingResources.append(item.recreate(self.get_affected_value(1,'C',False)))
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

        ## apply effect A
        powered_buildings = self.get_affected_value(powered_buildings, 'A')

        # apply effect B
        building_min = self.get_affected_value(turn_info['TM'], 'B')
        building_max = self.get_affected_value(turn_info['TX'], 'B')

        if powered_buildings < building_min:
            return 0
        buildings = min(powered_buildings, building_max)
        value_per_building = max(self.get_affected_value(turn_info['TR'], 'D') ,0)
        return buildings*value_per_building

    def get_affected_value(self,value, effect_code, floor=True):
        percent_total = 0
        for item in self.existingResources:
            if item.isActive:
                if item.RT == effect_code:
                    percent_total += item.RE
        if floor:
            return math.floor(value * percent_total)
        return value*percent_total


if __name__ == "__main__":
    inputs = ["0-demo.txt", "1-thunberg.txt", "2-attenborough.txt", "4-maathai.txt", "6-earle.txt",
              "7-mckibben.txt" ,"8-shiva.txt"]
    for inp in inputs:
        main = Main('inputs/'+inp)
        main.play_game()