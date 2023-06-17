class Pair :
    def __init__ (self, first , hand ):
        try :
            self.first = bool (first)
        except ValueError:
            print ("Uncorrect information should be bool")
        self.hand = hand

    def get_first (self):
        return self.first

    def get_hand (self):
        return self.hand

    def set_hand (self, hand2):
        self.hand = hand2 