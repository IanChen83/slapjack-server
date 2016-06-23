import random
from time import sleep

SET_HIT = "HIT"
SET_FAKE_HIT = "FAKE_HIT"
DUMMY = "DUMMY"

class slapjack:
    def __init__(self):
        self.current = 1

    def set(self, cur):
        self.current = cur

    def increment(self):
        self.current += 1

    def if_slap(self, card):
        # return True if we want to slap :))
        if random.random < 0.7:
            return SET_HIT if self.judge(card) else DUMMY

        if random.random < 0.2:
            sleep(random.random())
            return SET_HIT if self.judge(card) else SET_FAKE_HIT

        sleep(random.random())
        return SET_HIT

    def judge(card):
        return card == self.current
