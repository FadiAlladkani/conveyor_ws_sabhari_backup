import random
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import Pose, Point
import numpy as np
import cv2
import pyrealsense2 as rs
from arm.srv import stepper_srv
import object_detection_model as odm
import trash_item
import message_filters
import time
import warnings
warnings.filterwarnings("ignore")
CONFIDENCE_THRESHOLD = 9
X_THRESHOLD = 750 #640
FPS_TARGET = 5
class Camera:
    def __init__(self):
        self.cameraInfo = CameraInfo()
        self.bridge = CvBridge()
        self.trash_items = []
        self.trash_items_shown = []
        self.classifier = odm.ObjectDetectionModel()
        self.no_trash = Pose()
        self.no_trash.position.x = -1
        self.no_trash.position.y = -1
        self.belt_speed = 15
        self.delta_x_sum = 0
        self.start_time = time.time()

        # Services
        self.srv_set_xy_axis = rospy.ServiceProxy('arm/xy_axis_set', stepper_srv)

        # Publishers
        self.target_location_pub = rospy.Publisher("/target_location", Pose, queue_size=1)

        # print("Camera Init")
        
    def update_camera_info(self, caminfo):
        self.cameraInfo = caminfo

    def get_delta_x(self):
        fps= 1/(time.time()-self.start_time)
        delta_x = (self.belt_speed * FPS_TARGET)/fps
        return self.delta_x_sum + delta_x

    def new_image_recieved(self, depth_image, color_img):
        self.start_time=time.time()
        cv_image = self.bridge.imgmsg_to_cv2(color_img, "bgr8")
        # print("New image!")

        # find trash objects in image
        new_trash_items = self.classifier.classify(cv_image)
        # print("new items: {0}".format(len(new_trash_items)))
        fps= 1/(time.time()-self.start_time)
        # update previously detected trash item list with belt speed
        delta_x = (self.belt_speed * FPS_TARGET)/fps
        self.delta_x_sum+=delta_x
        for trash in self.trash_items:
            trash.x += delta_x
            if trash.x > X_THRESHOLD:
                self.trash_items.remove(trash)
        # print("Updated old list")

        # check if any new trash objects match existing trash objects
        for new_trash in new_trash_items:
            matched_existing_trash = False
            for existing_trash in self.trash_items:
                if new_trash.compare_item(existing_trash):
                    matched_existing_trash = True
                    existing_trash.update_item(new_trash)
                    
            if not matched_existing_trash:
                    self.trash_items.append(new_trash)

        # print("Belt tspeed: {0}".format((self.belt_speed * FPS_TARGET)/fps))
        # print("time: {0}".format(1/(time.time()-self.start_time)))
        # print("Updated new list")

        # select confident trash item closest to the arm (the one with the highest x pos)
        target_trash = None
        curr_x = 0
        cv_depth_image = self.bridge.imgmsg_to_cv2(depth_image, "passthrough")
        for trash in self.trash_items:
            if trash.trash_type == 0: #Check if cardboard
                #Check if (conf est)*(num frames) > CONFIDENCE_THRESHOLD or trash item has been updated by the user
                if trash.conf*len(trash.kp_conf[trash.trash_type].measurements) > CONFIDENCE_THRESHOLD or trash.updated:
                    if trash.x > curr_x:
                        self.update_trash_location(trash, cv_depth_image)
                        target_trash = trash
                        curr_x = trash.x

        # print("Select trash")
        # convert & send target position to arm
        if target_trash:
            self.send_target_location(target_trash.pose)
        else:
            self.send_target_location(self.no_trash)

        return cv_image


    def send_target_location(self, target_pose):
        self.target_location_pub.publish(target_pose)
    
    def update_trash_location(self, trash, depth_image):
        x = int(trash.x)
        y = int(trash.kp_y.est)  # use the kalman estimate for y position of trash

        if y < len(depth_image) and x < len(depth_image[0]):
           z = depth_image[y, x]

        #    print("[{0},{1},{2}]".format(x, y, z))

           location = self.pixel_to_pos(x, y, self.cameraInfo)

           # print(location)
           trash.pose.position.x = location[0]
           trash.pose.position.y = location[1]
           trash.pose.position.z = location[2]


    def pixel_to_pos(self, x, y, cameraInfo):
        new_x = ((cameraInfo.width - x) / cameraInfo.width) * 800
        new_y = ((cameraInfo.height - y) / cameraInfo.height) * 610
        new_z = 0

        return new_y+120, new_x+730, new_z #Switch coord system from camera to arm

    def depth_to_pos(self, x, y, depth, cameraInfo):
        intrinsics = rs.intrinsics()
        intrinsics.width = cameraInfo.width
        intrinsics.height = cameraInfo.height
        intrinsics.ppx = cameraInfo.K[2]
        intrinsics.ppy = cameraInfo.K[5]
        intrinsics.fx = cameraInfo.K[0]
        intrinsics.fy = cameraInfo.K[4]
        # _intrinsics.model = cameraInfo.distortion_model
        intrinsics.model = rs.distortion.brown_conrady
        intrinsics.coeffs = [i for i in cameraInfo.D]

        result = rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], depth)
        # result[0]: right, result[1]: down, result[2]: forward
        return -result[0]+406, -result[1]+319+120, result[2]
        #return -result[0]+398, result[1]+283.423+120, result[2]




if __name__ == '__main__':
    rospy.init_node('camera', anonymous=True)
    Camera()
    rospy.spin()

