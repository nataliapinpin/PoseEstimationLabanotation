# Class that represent Labanotation Data
# Inspired by https://link.springer.com/chapter/10.1007%2F978-3-662-45646-0_44

import numpy as np

dir_threshold = {"front": 0.25, "diagonal": 0.15, "side": 0.25}
pytorch_dir = {"front": 0.1, "diagonal": 0.05, "side": 0.1}
level_threshold = {"high": 0.25}
pytorch_level = {"high": 0.08}
place_threshold = 0.2


class LabanotationData:
    def __init__(self, col, start, joints):
        self.column = col
        self.start = start
        self.end = start+1
        self.symbol = ""

        self.calculate_symbol_angle(joints)

    def __str__(self):
        return f"Col: {self.column}, Start: {self.start}\n{self.symbol}"

    def __eq__(self, other):
        if type(other) == str:
            return other == self.symbol
        return other.symbol == self.symbol

    def __ne__(self, other):
        if type(other) == str:
            return other != self.symbol
        return other.symbol != self.symbol


    def calculate_symbol_angle(self, joints):
        """Sets self.symbol equal to the filename for the corresponding symbol"""
        if self.column == "right_arm":
            direction = "right"
            free = joints['rWrist']
            fixed = joints['rShoulder']
        elif self.column == "left_arm":
            direction = "left"
            free = joints['lWrist']
            fixed = joints['lShoulder']
        elif self.column == "right_leg":
            direction = "right"
            free = joints['rAnkle']
            fixed = joints['rHip']
        elif self.column == "left_leg":
            direction = "left"
            free = joints['lAnkle']
            fixed = joints['lHip']
        
        self.symbol = direction + self._direction_angle(free, fixed) + self._level_angle(free, fixed)


    def _direction_angle(self, free, fixed):
        """ Returns a string: forward, side, back, or empty string for place """
        mask = np.array([True,False,True]) # project to xz-plane
        free_2d = np.array([free[0],free[2]])
        fixed_2d = np.array([fixed[0],fixed[2]])
        x_project = fixed_2d + np.array([1,0])
        angle = self._calculate_angle(free_2d,fixed_2d,x_project)

        if self._is_place(free_2d, fixed_2d):
            return ""
        elif 0 < angle < 22.5 or 157.5 < angle < 180:
            return "side"
        elif 67.5 < angle < 112.5:
            return "forward" if free[2] < fixed[2] else "back"
        else:
            return "forwarddiagonal" if free[2] < fixed[2] else "backdiagonal"


    def _level_angle(self, free, fixed):
        """ Returns a string: high, middle, or low """
        if self._is_place(np.array(free), np.array(fixed)):
            return "middle"

        y_project = fixed + np.array([0,1,0])
        angle = self._calculate_angle(np.array(free),np.array(fixed),y_project)

        if 0 < angle < 67.5:
            return "high"
        elif 112.5 < angle < 180:
            return "low"
        else:
            return "middle"

    def _calculate_angle(self, a, b, c):
        """ Returns angle in degrees between 3 points """
        ba = a-b
        bc = c-b
        cos_angle = np.dot(ba,bc) / (np.linalg.norm(ba) * np.linalg.norm (bc))
        angle = np.arccos(cos_angle)
        return np.degrees(angle)  #angle in degrees

    def _is_place(self, free, fixed, threshold=place_threshold):
        return np.linalg.norm(free - fixed) < threshold


    def set_column(self, col):
        self.column = col

    def get_column(self):
        return self.column

    def get_beat(self):
        return self.start

    def set_symbol(self, symbol):
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol


    """
    Old functions (not currently in use)
    """

    def calculate_symbol_distance(self, joints):
        """Returns the filename for the corresponding symbol"""
        print("Calculate symbol")
        if self.column == "right_arm":
            print(joints['rWrist'])
            self.symbol += "right" + self.arm_direction(joints['rWrist'], joints['rShoulder']) + self.arm_level(joints['rWrist'], joints['rShoulder'])
        elif self.column == "left_arm":
            self.symbol += "left" + self.arm_direction(joints['lWrist'], joints['lShoulder']) + self.arm_level(joints['lWrist'], joints['lShoulder'])
        elif self.column == "right_leg":
            self.symbol += "right" + self.leg_direction(joints['rAnkle'], joints['rHip']) + self.leg_level(joints['rAnkle'], joints['rHip'])
        elif self.column == "left_leg":
            self.symbol += "left" + self.leg_direction(joints['lAnkle'], joints['lHip']) + self.leg_level(joints['lAnkle'], joints['lHip'])

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
            return "high" if wrist[1] > shoulder[1] else "low"
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
            return "high" if ankle[1] > hip[1] else "low"
        else:
            return "middle"


    def _direction_distance(self, free, fixed):
        """ Returns a string: forward, side, back, or empty string for place """
        if abs(free[0] - fixed[0]) > dir_threshold["side"]:
            return "side"
        elif abs(free[2] - fixed[2]) > dir_threshold["front"]:
            return "forward" if free[2] < fixed[2] else "back"
        elif abs(free[0] - fixed[0]) > dir_threshold["diagonal"]:
            return "forwarddiagonal" if free[2] < fixed[2] else "backdiagonal"
        else:
            return ""

    def _level_distance(self, free, fixed):
        """ Returns a string: high, middle, or low """
        if abs(free[1] - fixed[1]) > level_threshold["high"]:
            return "high" if free[1] > fixed[1] else "low"
        else:
            return "middle"