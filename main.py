from read_file import readFile
from Resource import Resource
import math

class Main:
    def __init__(self, input_file):
        self.output_file = 'outputs/output '+input_file.split("/")[-1]
        self.current_file = input_file.split('/')[-1].split(".")[0]
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

        self.accumulator = {'active':False, 'size':0, 'stored':0}

    def save_decisions(self):
        lines = []
        for decision in self.decisions:
            lines.append(" ".join([str(val) for val in decision])+"\n")
        with open(self.output_file, 'w') as f:
            f.writelines(lines)

    def play_game(self):
        count = 1
        for turn_info in self.turnsInfo:
            if count % 500 == 0:
                print('processing',self.current_file,f'{count}/{len(self.turnsInfo)}')
            count += 1
            self.do_turn(turn_info)
        self.save_decisions()
        print('total score: ',self.total_score)


    def do_turn(self, turn_info):
        self.turns_index += 1
        self.manage_resources()
        self.manage_accumulator()
        self.buy_resources(turn_info)
        turn_costs = self.calc_maintenance_cost()
        turn_profit = self.calc_profit(turn_info)
        self.budget = self.budget - turn_costs + turn_profit
        self.total_score += turn_profit
        print('current score:',self.total_score,'cost',turn_costs,'profit',turn_profit,'resources: ',[(a.isActive, a.RI) for a in self.existingResources])

    def manage_resources(self):
        remove_list = []
        for item in self.existingResources:
            item.update_turns()
            if item.get_out_of_life():
                remove_list.append(item)
        for rem in remove_list:
            self.existingResources.remove(rem)

    def buy_resources(self, turn_info):
        #### optimisation code in here somewhere

        # newResources = self.get_optimal_options(turn_info)
        newResources = self.get_predefined_options()

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
            missing_buildings = building_min-powered_buildings
            if missing_buildings <= self.accumulator['stored']:
                self.accumulator['stored'] -= missing_buildings
            else:
                return 0

        ## calculate buildings and store them in accumulator
        buildings = powered_buildings
        if powered_buildings > building_max:
            excess_buildings = powered_buildings - building_max
            space_in_accumulator = self.accumulator['size']-self.accumulator['stored']
            if space_in_accumulator>=excess_buildings:
                self.accumulator['stored'] += excess_buildings
                buildings += excess_buildings
            else:
                self.accumulator['stored'] += space_in_accumulator
                buildings += space_in_accumulator

        value_per_building = max(self.get_affected_value(turn_info['TR'], 'D') ,0)
        return buildings*value_per_building

    def get_affected_value(self,value, effect_code, floor=True):
        percent_total = 0
        for item in self.existingResources:
            if item.isActive:
                if item.RT == effect_code:
                    percent_total += item.RE
        if floor:
            return math.floor(value * (1+percent_total/100))
        return value * (1+percent_total/100)

    def manage_accumulator(self):
        total = 0
        for item in self.existingResources:
            if item.isActive and item.RT == 'E':
                total+=item.RE
        if total != 0:
            self.accumulator['active'] = True
            self.accumulator['size'] = total
        else:
            self.accumulator['active'] = False
            self.accumulator['size'] = 0
        if self.accumulator['stored'] > self.accumulator['size']:
            self.accumulator['stored'] = self.accumulator['size']


    def get_optimal_options(self, turn_info):
        # find affordable_resources
        affordable_resources = []
        for item in self.resources:
            if item.RA < self.budget:
                affordable_resources.append(item)

        # sort based on estimated value
        affordable_resources = sorted(affordable_resources,
                                      key=lambda x: self.get_resource_value(x, turn_info),
                                      reverse=True)

        money_left = self.budget
        new_resources = []
        while len(affordable_resources)>0 and money_left > affordable_resources[0].RA:
            best_resource = affordable_resources.pop(0)
            maintenance_cost = sum([r.RP for r in self.existingResources+new_resources]) + best_resource.RP
            if self.budget - best_resource.RA >= maintenance_cost:
                new_resources.append(best_resource)
                money_left -= best_resource.RA

        return new_resources

    def get_resource_value(self, resource, turn_info):
        return resource.RU * turn_info['TR'] * resource.RL / (resource.RA + resource.RP)

    def get_predefined_options(self):
        ids = [[5],[2],[2],[],[2,2],[2]]
        outputs = ids[self.turns_index]
        new_resources = []
        for id_val in outputs:
            new_resources.append(self.resources[id_val-1])
        return new_resources

if __name__ == "__main__":
    # inputs = ["0-demo.txt", "1-thunberg.txt", "2-attenborough.txt", "4-maathai.txt", "6-earle.txt",
    #           "7-mckibben.txt" ,"8-shiva.txt"]
    inputs = ["0-demo.txt"]
    for inp in inputs:
        main = Main('inputs/'+inp)
        main.play_game()