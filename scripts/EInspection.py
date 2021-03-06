#!/usr/bin/env python
# -*- coding: utf-8 -*

import rospy
import time
import subprocess
import std_srvs.srv
import tf
import actionlib
from std_msgs.msg import String
from geometry_msgs.msg import Twist,Quaternion,PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal


class Inspect:
    def __init__(self):
        #way points
        self.wp_list=[[8.67,-4.82,3.14],[6.29,-2.53,3.14],[2.89,-0.698,3.14],[0.388,0.716,3.14]]
        #publisher & subscriber
        self.init_pose_pub = rospy.Publisher('/initialpose',PoseWithCovarianceStamped,queue_size=1)
        self.vel_pub = rospy.Publisher('/cmd_vel_mux/input/teleop',Twist,queue_size=1)
        self.base_sub = rospy.Subscriber('/amcl_pose',PoseWithCovarianceStamped,self.BaseCB)
        self.laser_sub = rospy.Subscriber('/scan',LaserScan,self.LaserCB)
        #for navigation
        self.clear_costmap = rospy.ServiceProxy('move_base/clear_costmaps',std_srvs.srv.Empty)
        self.navigation_count = 0
        self.robot_pose_x = 999
        self.robot_pose_y = 999
        self.centor_laser_dist = -1
        self.ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        #for emergency stop
        self.before_laser_update_count = -1
        self.laser_update_count = 0
        self.emergency_stop_flg = False
        self.before_stop_pose = PoseWithCovarianceStamped()
        #for error
        self.wp_timeout_count = 0
        
#---------------------------CallBack
    def BaseCB(self,pose):
        self.robot_pose_x = pose.pose.pose.position.x
        self.robot_pose_y = pose.pose.pose.position.y
        if self.emergency_stop_flg == False:
            print 'remember now pose'
            self.before_stop_pose = pose
            
    def LaserCB(self,laser_scan):
        self.centor_laser_dist = laser_scan.ranges[405]
        self.laser_update_count += 1#use for detecting emergency stop

    def Speak(self,speech):
        cmd = '/usr/bin/picospeaker %s' % speech
        subprocess.call(cmd.strip().split(" "))
        time.sleep(len(speech)/10)

#--------------------------
    def Navigate(self,wp_num):
        if self.ac.wait_for_server(rospy.Duration(1)) == 1:
            print "wait for action client rising up 0"
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x =  self.wp_list[wp_num][0]
        goal.target_pose.pose.position.y =  self.wp_list[wp_num][1]
        q = tf.transformations.quaternion_from_euler(0, 0, self.wp_list[wp_num][2])
        goal.target_pose.pose.orientation = Quaternion(q[0],q[1],q[2],q[3])
        self.ac.send_goal(goal);
        
    def StopEmergency(self):
        if self.before_laser_update_count == self.laser_update_count:
            self.emergency_stop_flg = True
            print 'Hit the emergency stop button!'
            self.ac.cancel_goal()
            cmd = Twist()
            cmd.angular.z = 0
            while self.before_laser_update_count == self.laser_update_count and not rospy.is_shutdown():
                self.vel_pub.publish(cmd)
                #print 'wait for release the emergency stop button'
            time.sleep(5)
            self.init_pose_pub.publish(self.before_stop_pose)
            print 'initialize state!'
            time.sleep(5)
            self.emergency_stop_flg = False
            self.Speak('I start')
        self.before_laser_update_count = self.laser_update_count

#----------------------state
    def WaitOpeningDoor(self):#0
        print 'wait for opening the door',self.centor_laser_dist
        if self.centor_laser_dist > 0.6:
            self.Speak('I detect opening the door')
            return 1
        return 0
        
    def GoToWp0(self):#1
        self.wp_timeout_count += 1
        self.navigation_count += 1
        if self.navigation_count >= 20:
            self.navigation_count = 0
            self.clear_costmap()
            self.Navigate(0)
        self.StopEmergency()
        if self.ac.get_state()==3 or self.wp_timeout_count > 150:
            self.wp_timeout_count = 0
            return 2
        return 1

    
    def GoToWp1(self):#2
        self.wp_timeout_count += 1
        self.navigation_count += 1
        if self.navigation_count >= 20:
            self.navigation_count = 0
            self.clear_costmap()
            self.Navigate(1)
        self.StopEmergency()
        if self.ac.get_state()==3 or self.wp_timeout_count > 150:
            self.wp_timeout_count = 0
            self.navigation_count = 20
            return 3
        return 2

    def GoToWp2(self):#3
        self.navigation_count += 1
        if self.navigation_count >= 20:
            self.navigation_count = 0
            self.clear_costmap()
            self.Navigate(2)
        self.StopEmergency()
        if self.ac.get_state()==3:
            self.navigation_count = 20
            return 4
        return 3

    def IntroduceOneself(self):#4
        self.Speak('I am Happy mini')
        time.sleep(1)
        self.Speak('I was developed by')
        #time.sleep(1)
        self.Speak('KIT Happy Robots.')
        return 5

    def GoToWp3(self):#5
        self.navigation_count += 1
        if self.navigation_count >= 20:
            self.navigation_count = 0
            self.clear_costmap()
            self.Navigate(3)
        self.StopEmergency()
        if self.ac.get_state()==3:
            self.navigation_count = 20
            return 6
        return 5


    def FinishInsp(self):#6
        self.Speak('I finished robot inspection')
        return 999
        
if __name__ == '__main__':
    rospy.init_node('robot_inspection')
    ins = Inspect()
    ins.Speak('I start robot inspection')
    state = 0
    while not rospy.is_shutdown():
        if state == 0:
            state = ins.WaitOpeningDoor()
        elif state == 1:
            state = ins.GoToWp0()
        elif state == 2:
            state = ins.GoToWp1()
        elif state == 3:
            state = ins.GoToWp2()
        elif state == 4:
            state = ins.IntroduceOneself()
        elif state == 5:
            state = ins.GoToWp3()
        elif state == 6:
            state = ins.FinishInsp()
        elif state == 999:
            print 'finish'
        print "state is ",state
        rate = rospy.Rate(5)
        rate.sleep()
    rospy.spin()
