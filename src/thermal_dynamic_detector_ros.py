#!/usr/bin/env python

import rospy
import numpy as np
from cv_bridge import CvBridge
import thermal_dynamic_detector as dd
from sensor_msgs.msg import Image



rospy.init_node('thermal_dynamic_detector', anonymous=False)
nodeName = rospy.get_name()

# Name of input topics from launch-file. 
topic_image_in = rospy.get_param(nodeName+'/topicImageIn', nodeName+'/UnknownInputTopic') 
    
# Name of output topics from launch-file. 
topic_image_out = rospy.get_param(nodeName+'/topicImageOut', nodeName+'/UnknownOutputTopic')


#rSky = 0.2 # Area not to be used in the in determining the median temperature. 
#degAboveMedian = 3.0 # 
#degDiff = 12.0
#rot90Image = 2

rRemoveSky = rospy.get_param(nodeName+'/rRemoveSky', 0.0 )
degAboveMedian = rospy.get_param(nodeName+'/degAboveMedian', 2.0 )
degDiff = rospy.get_param(nodeName+'/degDiff', 10.0)
rot90Image = rospy.get_param(nodeName+'/rot90Image', 0)

print("topic_image_in",topic_image_in)
print("topic_image_out",topic_image_out)


# Publishers
pub_image = rospy.Publisher(topic_image_out, Image , queue_size=0)


bridge = CvBridge()

    
def callback_bb(image):
    #print("Image received")
    cv_image = bridge.imgmsg_to_cv2(image, desired_encoding="passthrough")


    out,nRemoveSky = dd.dynamicThreshold(cv_image,degAboveMedian,degDiff,rRemoveSky,rot90ImageK=rot90Image)
    image_message = bridge.cv2_to_imgmsg(out, encoding="passthrough")
    pub_image.publish(image_message)

# Get subscripers.
rospy.Subscriber(topic_image_in, Image,callback_bb,queue_size=None)

# main
def main():
    rospy.spin()

if __name__ == '__main__':
    main()
