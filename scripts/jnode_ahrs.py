#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Quaternion
from glob import glob
from subprocess import call

# make sure we can exit the scirpt pressing STRG+C on linux
import signal,sys
def sig(signal,fname):
    sys.exit(0)
signal.signal(signal.SIGINT, sig)

def talker():
    pub = rospy.Publisher('orientation', Quaternion)
    rospy.init_node('jnode', anonymous=True)
    port = sorted(glob('/dev/ttyACM*'))[0]
    call("stty -F %s raw" % port, shell=True)
    serial = open(port, 'r')

    while not rospy.is_shutdown():
        line = serial.readline().split('\t')
        #rospy.loginfo(line)

        if len(line) != 4:
            rospy.loginfo("bogus read")

        pub.publish(*[float(x) for x in line])

if __name__ == '__main__':
    try: talker()
    except rospy.ROSInterruptException: pass
