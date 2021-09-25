# Class that represent Labanotation Data
# Inspired by https://link.springer.com/chapter/10.1007%2F978-3-662-45646-0_44


dir_threshold = {"front": 0.1, "diagonal": 0.05, "side": 0.1}
level_threshold = {"high": 0.08}


class LabanotationData:
    def __init__(self, col, start):
        self.column = col
        self.start = start
        self.end = start+1
        self.symbol = ""

    def __str__(self):
        return f"Col: {self.column}, Start: {self.start}\n{self.symbol}"

    def __eq__(self, other):
        return other.symbol == self.symbol

    def __ne__(self, other):
        return other.symbol != self.symbol

    def calculate_symbol(self, *args):
        """Returns the filename for the corresponding symbol"""
        symbol = ""
        if self.column == "right_arm":
            self.symbol += "right" + self.arm_direction(args[0], args[2]) + self.arm_level(args[0], args[2])
        elif self.column == "left_arm":
            self.symbol += "left" + self.arm_direction(args[0], args[2]) + self.arm_level(args[0], args[2])
        elif self.column == "right_leg":
            self.symbol += "right" + self.leg_direction(args[0], args[2]) + self.leg_level(args[0], args[2])
        elif self.column == "left_leg":
            self.symbol += "left" + self.leg_direction(args[0], args[2]) + self.leg_level(args[0], args[2])

    def arm_direction(self, wrist, shoulder):
        """ Returns a string: forward, side, back, or empty string for place """
        if abs(wrist[0] - shoulder[0]) > dir_threshold["side"]:
            return "side"
        elif abs(wrist[2] - shoulder[2]) > dir_threshold["front"]:
            return "forward" if wrist[2] < shoulder[2] else "back"
        elif abs(wrist[0] - shoulder[0]) > dir_threshold["diagonal"]:
            return "forwarddiagonal" if wrist[2] < shoulder[2] else "backdiagonal"
        else:
            return ""

    def arm_level(self, wrist, shoulder):
        """ Returns a string: high, middle, or low """
        if abs(wrist[1] - shoulder[1]) > level_threshold["high"]:
            return "high" if wrist[1] < shoulder[1] else "low"
        else:
            return "middle"

    def leg_direction(self, ankle, hip):
        """ Returns a string: forward, side, back, or empty string for place """
        if abs(ankle[0] - hip[0]) > dir_threshold["side"]:
            return "side"
        elif abs(ankle[2] - hip[2]) > dir_threshold["front"]:
            return "forward" if ankle[2] < hip[2] else "back"
        elif abs(ankle[0] - hip[0]) > dir_threshold["diagonal"]:
            return "forwarddiagonal" if ankle[2] < hip[2] else "backdiagonal"
        else:
            return ""

    def leg_level(self, ankle, hip):
        """ Returns a string: high, middle, or low """
        if abs(ankle[1] - hip[1]) > level_threshold["high"]:
            return "high" if ankle[1] < hip[1] else "low"
        else:
            return "middle"

    # TODO: change direction/level functions to general
    def direction(self, free, fixed):
        """ Returns a string: forward, side, back, or empty string for place """
        if abs(free[0] - fixed[0]) > dir_threshold["side"]:
            return "side"
        elif abs(free[2] - fixed[2]) > dir_threshold["front"]:
            return "forward" if free[2] < fixed[2] else "back"
        elif abs(free[0] - fixed[0]) > dir_threshold["diagonal"]:
            return "forwarddiagonal" if free[2] < fixed[2] else "backdiagonal"
        else:
            return ""

    def leg_level(self, ankle, hip):
        """ Returns a string: high, middle, or low """
        if abs(ankle[1] - hip[1]) > level_threshold["high"]:
            return "high" if ankle[1] < hip[1] else "low"
        else:
            return "middle"

    def set_column(self, col):
        self.column = col

    def get_column(self):
        return self.column

    def get_beat(self):
        return self.start

    def get_symbol(self):
        return self.symbol


