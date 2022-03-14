import labanotation_data as lnd
from labanotation_data import LabanotationData

"""
Keypoint Dictionary Keys
    rAnkle
    rKnee
    rHip
    lHip
    lKnee
    lAnkle
    pelvis
    midSpine
    neck
    head
    rWrist
    rElbow
    rShoulder
    lShoulder
    lElbow
    lWrist
"""


class LabanotationScore:
    def __init__(self):
        self.right_arm = []
        self.left_arm = []
        self.right_leg = []
        self.left_leg = []
        self.right_support = []
        self.left_support = []

        self.joints = None
        self.current_beat = -1

    def get_score(self):
        return [self.right_arm, self.left_arm, 
                self.right_leg, self.left_leg,
                self.right_support, self.left_support]

    def analyze_beat(self, joints: dict):
        self.joints = joints
        self.current_beat += 1

        self._analyze_arms()
        self._analyze_legs()

        print(self.right_arm[-1])
        print(self.left_arm[-1])


    def _analyze_arms(self):
        r_arm = LabanotationData("right_arm", self.current_beat, self.joints)
        if len(self.right_arm) == 0 or self.right_arm[-1] != r_arm:
                self.right_arm.append(r_arm)

        l_arm = LabanotationData("left_arm", self.current_beat, self.joints)
        if len(self.left_arm) == 0 or self.left_arm[-1] != l_arm:
                self.left_arm.append(l_arm)


    def _analyze_legs(self):
        r_leg = LabanotationData("right_leg", self.current_beat, self.joints)
        if r_leg != "rightlow":
           if len(self.right_leg) == 0 or self.right_leg[-1] != r_leg:
                self.right_leg.append(r_leg)
        else:
            r_leg.set_column("right_support")
            r_leg.set_symbol("rightmiddle")
            r_hold = self._analyze_right_support(r_leg)

        l_leg = LabanotationData("left_leg", self.current_beat, self.joints)
        if l_leg != "leftlow":
            if len(self.left_leg) == 0 or self.left_leg[-1] != l_leg:
                self.left_leg.append(l_leg)
        else:
            l_leg.set_column("left_support")
            l_leg.set_symbol("leftmiddle")
            l_hold = self._analyze_left_support(l_leg)

        # make a new method to handle/fix supports
        if r_leg == "righthold" and l_leg == "lefthold" or r_leg == "check_left" and l_leg == "lefthold" or r_leg == "righthold" and l_leg == "check_right":
            if r_leg == "check_left":
                self.right_support.append(r_leg)
            if l_leg != "check_right":
                self.left_support.pop(-1)
            r_leg.set_symbol("hold")
            r_leg.set_column("support")
        elif r_leg == "check_left" and l_leg == "leftmiddle":
            r_leg.set_symbol("righthold")
            self.right_support.append(r_leg)
        elif l_leg == "check_right" and r_leg == "rightmiddle":
            l_leg.set_symbol("lefthold")
            self.left_support.append(l_leg)


    def _analyze_right_support(self, support):
        # if there are not yet any support symbols OR if there has been a gesture after a support symbol
        if len(self.right_support) == 0 or len(self.right_leg) != 0 and self.right_support[-1].get_beat() < self.right_leg[-1].get_beat():
            self.right_support.append(support)
        # if the previous beat was support and it is being held
        elif len(self.right_support) != 0 and self.right_support[-1].get_beat() == self.current_beat - 1 and self.right_support[-1].get_symbol() == "rightmiddle":
            support.set_symbol("righthold")
            self.right_support.append(support)
        else:
            support.set_symbol("check_left")

    def _analyze_left_support(self, support):
        if (len(self.left_support) == 0 or len(self.left_leg) != 0 and self.left_support[-1].get_beat() < self.left_leg[-1].get_beat()):
            self.left_support.append(support)
        elif len(self.left_support) != 0 and self.left_support[-1].get_beat() == self.current_beat - 1 and self.left_support[-1].get_symbol() == "leftmiddle":
            support.set_symbol("lefthold")
            self.left_support.append(support)
        else:
            support.set_symbol("check_right")


        # REVIEW: cases to put hold symbol

    def get_beat(self):
        return self.current_beat
