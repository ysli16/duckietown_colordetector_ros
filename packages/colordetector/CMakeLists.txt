cmake_minimum_required(VERSION 2.8.3)
project(colordetector)

find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
  duckietown_msgs
  cv_bridge
)

catkin_package()
