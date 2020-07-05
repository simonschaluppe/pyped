
from random import random, randint

class Battery:
    capacity    = 100
    charge_state= round(random(), 4)
    maxcharge   = randint(5,12)
    relcharge   = maxcharge / capacity
    def charge(self):
        self.charge_state = min(1, self.charge_state + self.relcharge)
        return True
    def discharge(self, rate):
        if rate > self.charge_state:
            raise ValueError(f"discharge rate {rate} > charge_state {__name__.charge_state}.")
        else:
            self.charge_state = max(0, self.charge_state - rate)

class Ecar:
    states = ["plugged", "moving "]
    target = randint(50,100)/100

    def __init__(self, id):
        self.id = f"testcar #{id}"
        self.state = self.states[0]
        self.battery = Battery()

    def update(self):
        self.set_state()
        self.handle_state()

    def set_state(self):
        # TODO: Markov Chain Lookup
        if self.state == self.states[0]:
            if random() < 0.2:
                self.state = self.states[1]
        else:
            if random() < 0.5:
                self.state = self.states[0]

    def handle_state(self):
        if self.state == self.states[0]:
            self.charge()
        elif self.state == self.states[1]:
            self.move()

    def move(self):
        req_energy = randint(10, 20)/100
        if self.battery.charge_state > req_energy:
            self.battery.discharge(req_energy)

    def charge(self):
        if self.battery.charge_state < self.target:
            self.battery.charge()

    def charge_bar(self):
        length = 20
        bar = "[" +"#" * round(self.battery.charge_state * length) + " " * round(length - self.battery.charge_state * length) + "]"
        start = bar[:round(self.target*length)]
        end = bar[round(self.target*length)+1:]
        # print(start, end)
        return "|".join([start, end])

    def __repr__(self):
        charge_bar = self.charge_bar()
        # charge_bar[round(self.target/length)+1] = "|"
        return f"E-car [{self.state}]: {charge_bar} charge: {round(self.battery.charge_state * 100)}% > target: {round(self.target * 100)}%"



if __name__ == "__main__":
    car1 = Ecar(1)
    for h in range(12):
        car1.update()
        print(car1)
