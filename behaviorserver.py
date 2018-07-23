import roslib; roslib.load_manifest('saunter_interaction')
import rospy
from std_msgs.msg import String
from robot_manager import RobotManager
import time
from cordial_sound.libsoundplay import SoundClient


class BehaviorPlayer():
    def __init__(self):

        def callback(data):
            #action behavior processing
            if int(data.data) == 0 and len(self.performedBehaviors) > 1:
                self.performedBehaviors = []

            if data not in self.performedBehaviors:
                print("performing behavior")
                time.sleep(2.0)

                case = int(data.data)
                if case == 0:
                    self.robot.say("demo1", wait=True)
                elif case == 1:
                    self.robot.say("dance1", wait=True)
                    # time.sleep(4.0)
                elif case == 2:
                    self.robot.say("compliment1", wait=True)
                elif case == 3:
                    self.robot.say("encouragement1", wait=True)
                elif case == 4:
                    self.robot.say("sassy1", wait=True)
                elif case == 5:
                    self.robot.say("joke1", wait=True)
                elif case == 6:
                    self.sound.playWave('/home/saunter/rosbuild_ws/saunter/saunter_interaction/speech/data/DanceSong.wav')
                    self.robot.do("shimmy", wait=True)
                    # time.sleep(4.0)

                self.performedBehaviors += [data]
                self.robot.do("returnToNeutral", wait=True)

            rospy.Publisher("kiwi", String, queue_size = 1).publish("behavior completed")


        # In ROS, nodes are uniquely named. If two nodes with the same
        # node are launched, the previous one is kicked off. The
        # anonymous=True flag means that rospy will choose a unique
        # name for our 'listener' node so that multiple listeners can
        # run simultaneously.
        rospy.init_node('BehaviorServer', anonymous=True)
        rospy.Subscriber("behavior_number", String, callback)

        self.robot = RobotManager("DB1")
        self.performedBehaviors = []
        self.sound = SoundClient()






if __name__ == '__main__':
    BehaviorPlayer()

    rospy.spin()
    # spin() simply keeps python from exiting until this node is stopped
