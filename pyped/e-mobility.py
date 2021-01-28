
from random import random, randint
import functools

class Battery:
    capacity    = 100
    charge_state= round(random(), 4)
    maxcharge   = randint(5,12)
    relcharge   = maxcharge / capacity

    def charge(self):
        final = min(1, self.charge_state + self.relcharge)
        delta = abs(self.charge_state - final)
        self.charge_state = final
        return delta

    def discharge(self, rate):
        if rate > self.charge_state:
            raise ValueError(f"discharge rate {rate} > charge_state {__name__.charge_state}.")
        else:
            final = max(0, self.charge_state - rate)
            delta = abs(self.charge_state - final)
            self.charge_state = final
            return -delta

class Ecar:
    states = ["plugged", ">moving"]
    target = randint(50,100)/100
    charged = 0
    diverted = 0
    utilized = 0

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
            if random() < 0.7:
                self.state = self.states[0]

    def handle_state(self):
        if self.state == self.states[0]:
            if self.battery.charge_state < self.target:
                self.charge()
            elif self.battery.charge_state > self.target:
                self.discharge()
        elif self.state == self.states[1]:
            self.move()

    def change_bar(func):
        @functools.wraps(func)
        def wrap(self):
            length = 20
            str = " "*18+" "*round(self.battery.charge_state * length)
            change = func(self)
            change_len = round(abs(change) * length)
            if change > 0:
                char = ">"
                pm = "+"
            else:
                char = "<"
                pm = ""
                str = str[:len(str)-change_len]
            change_str = char * change_len
            print(str+change_str+ f" {pm}{round(change*100)}%")
        return wrap

    @change_bar
    def move(self):
        req_energy = randint(10, 20)/100
        if self.battery.charge_state > req_energy:
            diff = self.battery.discharge(req_energy)
            self.utilized += self.battery.capacity * diff
            return diff
        else:
            diff = self.battery.discharge(self.battery.charge_state)
            self.utilized += self.battery.capacity * diff
            return diff

    @change_bar
    def charge(self):
        diff = self.battery.charge()
        self.charged += self.battery.capacity * diff
        return diff

    @change_bar
    def discharge(self):
        diff = self.battery.discharge(randint(5,15)/100)
        self.diverted += self.battery.capacity * diff
        return diff

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
        return f"E-car [{self.state}]: {charge_bar}"



if __name__ == "__main__":
    car1 = Ecar(1)
    for h in range(12):
        car1.update()
        print(car1)
