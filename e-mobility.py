
from random import random, randint

class Battery:
    capacity    = 100
    charge      = round(random(), 4)
    maxcharge   = randint(5,12)
    relcharge   = maxcharge / capacity
    def apply_charge(self):
        self.charge = min(1, self.charge + self.relcharge)

class Ecar:
    states = ["plugged", "trip"]
    target = randint(50,100)/100

    def __init__(self, id):
        self.id = f"testcar #{id}"
        self.state = self.states[0]
        self.battery = Battery()


    def handle_state(self,hour):
        if self.state == self.states[0]:
            self.apply_charge()

        elif self.state == self.states[1]:
            pass

    def apply_charge(self):
        if self.battery.charge < self.target:
            self.battery.apply_charge()

    def charge_bar(self):
        length = 30
        bar = "["+"#"*round(self.battery.charge*length)+" "*round(length-self.battery.charge*length)+"]"
        start = bar[:round(self.target*length)]
        end = bar[round(self.target*length)+1:]
        # print(start, end)
        return "|".join([start, end])

    def __repr__(self):
        charge_bar = self.charge_bar()
        # charge_bar[round(self.target/length)+1] = "|"
        return f"E-car: {charge_bar} charge: {round(self.battery.charge*100)}% > target: {round(self.target*100)}%"



if __name__ == "__main__":
    car1 = Ecar(1)
    for h in range(12):
        car1.apply_charge()
        print(car1)