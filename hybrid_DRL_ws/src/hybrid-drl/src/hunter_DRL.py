#!/usr/bin/env python3
import rospy
import numpy as np
import std_msgs
from geometry_msgs.msg import Twist, Pose2D
from sensor_msgs.msg import Imu

class pose_listener:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.psi = 0.0
        
        self.pose_estimate = rospy.Subscriber('/odom_pose', Pose2D, self.odom_callback)
        
    def odom_callback(self, msg):
        x   = msg.x
        y   = msg.y
        psi = msg.theta
        
        self.x      = x
        self.y      = y
        self.psi    = psi
    
    def pose_feedback(self):
        x_pose = self.x
        y_pose = self.y 
        psi_pose = self.psi
        return x_pose, y_pose, psi_pose

class imu_listener:
    def __init__(self):
        self.qx = 0.0
        self.qy = 0.0
        self.qz = 0.0
        self.qw = 0.0
        
        self.wx = 0.0
        self.wy = 0.0
        self.wz = 0.0
        
        self.ax = 0.0
        self.ay = 0.0
        self.az = 0.0
        
        self.pose_estimate = rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        
    def imu_callback(self, msg):
        self.qx = msg.orientation.x
        self.qy = msg.orientation.y
        self.qz = msg.orientation.z
        self.qw = msg.orientation.w
        
        self.wx = msg.angular_velocity.x
        self.wy = msg.angular_velocity.y
        self.wz = msg.angular_velocity.z
        
        self.ax = msg.linear_acceleration.x
        self.ay = msg.linear_acceleration.y
        self.az = msg.linear_acceleration.z
        
        
    
    def imu_feedback(self):
        qx_ = self.qx
        qy_ = self.qy
        qz_ = self.qz
        qw_ = self.qw
        
        wx_ = self.wx
        wy_ = self.wy
        wz_ = self.wz
        
        ax_ = self.ax
        ay_ = self.ay
        az_ = self.az
        
        return qx_, qy_, qz_, qw_, wx_, wy_, wz_, ax_, ay_, az_
    
class velocity_publisher():
    def __init__(self):
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        
        self.wx = 0.0
        self.wy = 0.0
        self.wz = 0.0
        
        self.move = Twist()
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    
    def publish_control(self, v, delta):
        self.move.linear.x = v
        self.move.angular.z = delta
        self.pub.publish(self.move)  

def hybrid_DRL_controller():
    
    '''Write Your Code here'''
    
    v = 0.0
    delta = 0.1
    return v, delta

def main():
    rospy.init_node('hybrid_drl')
    pose_feedback = pose_listener()
    imu_feedback  = imu_listener()
    controller    = velocity_publisher()
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        x, y, psi = pose_feedback.pose_feedback()
        
        print(x, y, psi)
        
        qx_, qy_, qz_, qw_, wx_, wy_, wz_, ax_, ay_, az_ = imu_feedback.imu_feedback()
        
        print(qx_, qy_, qz_, qw_, wx_, wy_, wz_, ax_, ay_, az_)
        
        v, delta = hybrid_DRL_controller()
        
        print(v, delta) 
        
        controller.publish_control(v, delta)
        
        rate.sleep()
        
        
        
if __name__ == '__main__':
    main()
        
        
        
            
            
    
