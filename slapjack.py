import random
from time import sleep
class slapjack:
    def __init__(self):
        self.current = 1

    def if_slap(self, card):
        # return True if we want to slap :))
        if random.random < 0.7:
            return self.judge(card)

        if random.random < 0.2:
            sleep(random.random())
            return self.judge(card)

        sleep(random.random())
        return True

    def judge(card):
        return card == self.current
