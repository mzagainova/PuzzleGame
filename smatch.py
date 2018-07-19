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
        self.subscriber = rospy.Subscriber('trigger', String, self.callback)

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
        self.subscriber = rospy.Subscriber("kiwi", String, self.callback)

    def callback(self, data):
        if data.data == "behavior completed":
            self.done = True
            self.publisher.publish('behavior completed')

    def execute(self, userdata):
        for i in range(0,3000):
            if self.done:
                return 'reward_done'

            time.sleep(.1)

# define state questions (robot finished reward action, person fills out questionnaire)
class Questions(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['repeat_puzzle', 'final_ranking'])
        self.subscriber = rospy.Subscriber("questions", String, self.callback)
        self.state = 0

    def callback(self, data):
        if data.data == "questions compelted":
            self.state = 1
        elif data.data == "final ranking":
            self.state = 2

    def execute(self, state):
        rospy.loginfo('Executing state Questions')
        for i in range(0,3000):
            if self.state == 1:
                return 'repeat_puzzle'
            elif self.state == 2:
                return 'final_ranking'

# define state EndQuestions (final q)
class EndQuestions(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['end_study'])

    def execute(self, userdata):
        rospy.loginfo('Executing state EndQuestions')
        return 'end_study'

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
                               transitions={'reward_done':'Questions'})
        smach.StateMachine.add('Questions', Questions(),
                               transitions={'repeat_puzzle':'PuzzleLevel',
                                            'final_ranking':'EndQuestions'})
        smach.StateMachine.add('EndQuestions', EndQuestions(),
                               transitions={'end_study':'end_state'})

    # Execute SMACH plan
    outcome = sm.execute()


if __name__ == '__main__':
    main()
