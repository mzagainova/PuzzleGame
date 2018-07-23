#!/usr/bin/env python

import roslib; #roslib.load_manifest('smach_example')
import rospy
import smach
import smach_ros
import threading
import time
from std_msgs.msg import String

# define state PuzzleLevel (person is working on puzzle game)
class PuzzleLevel(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['level_done'])
        self.counter = 0
        self.done = False
        self.subscriber = rospy.Subscriber('trigger', String, self.callback, queue_size = 1)

    def callback(self, data):
        if data.data == "level completed":
            self.done = True

    def execute(self, data):
        for i in range(0,3000):
            if self.done:
                return 'level_done'
            time.sleep(.1)

# define state Behavior (robot is performing reward) & wait screen shown on tablet
class Behavior(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['reward_done'])
        self.done = False
        self.publisher = rospy.Publisher('reward', String, queue_size = 1)
        self.subscriber = rospy.Subscriber("kiwi", String, self.callback, queue_size = 1)

    def callback(self, data):
        if data.data == "behavior completed":
            self.done = True
            self.publisher.publish('behavior completed')

    def execute(self, userdata):
        for i in range(0,3000):
            if self.done:
                return 'reward_done'

            time.sleep(.1)

# main
def main():
    rospy.init_node('reward_study_smach')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['end_state'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('PuzzleLevel', PuzzleLevel(),
                               transitions={'level_done':'Behavior'})
        smach.StateMachine.add('Behavior', Behavior(),
                               transitions={'reward_done':'PuzzleLevel'})

    # Execute SMACH plan
    outcome = sm.execute()


if __name__ == '__main__':
    main()
