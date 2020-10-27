#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 21:50:04 2020

@author: yueshan
"""
import cv2
import numpy as np
import rospy
from duckietown.dtros import DTROS, NodeType, DTParam,ParamType
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge



class ColorDetector(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(ColorDetector, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        # construct publisher
        self.sub = rospy.Subscriber('colordetector/image/compressed', CompressedImage, self.callback)
        self.pub = rospy.Publisher('colordetector/debug/image/compressed', CompressedImage, queue_size=10)
        self.bridge=CvBridge()
        
        #set color to deteect
        self.color=DTParam('~color',param_type=ParamType.STR)

    
    def detector(self,img):  
        #set detector
        yellow_lower=np.array([20,255*0.2,255*0.3],dtype=np.int32)
        yellow_upper=np.array([40,255,255],dtype=np.int32)
        
        red_lower_1=np.array([0,255*0.1,255*0.3],dtype=np.int32)
        red_upper_1=np.array([10,255,255],dtype=np.int32)
        red_lower_2=np.array([170,255*0.1,255*0.3],dtype=np.int32)
        red_upper_2=np.array([180,255,255],dtype=np.int32)
    
        #conver image to HLS
        imgHLS=cv2.cvtColor(img,cv2.COLOR_BGR2HLS)
        
        #detect color
        if self.color.value=='yellow':
            #yellow color
            yellow_mask = cv2.inRange(imgHLS, yellow_lower, yellow_upper)
            yellow_mask=cv2.GaussianBlur(yellow_mask,(9,9),10)
            mask=cv2.threshold(yellow_mask,127,255,cv2.THRESH_BINARY)[-1]
        
        else:
            #red color
            red_mask_1=cv2.inRange(imgHLS, red_lower_1, red_upper_1)
            red_mask_2=cv2.inRange(imgHLS, red_lower_2, red_upper_2)
            red_mask=cv2.bitwise_or(red_mask_1, red_mask_2)
            red_mask=cv2.GaussianBlur(red_mask,(9,9),10)
            mask=cv2.threshold(red_mask,127,255,cv2.THRESH_BINARY)[-1]
            
        #find contours
        contours=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
        #cv2.drawContours(frame,contours,-1,(0,0,255),3)
        #cv2.imshow('contour',frame)
        
        #find min area rectangle
        img_detected=img
        for contour in contours:
            rect=cv2.minAreaRect(np.vstack(contour).squeeze())
            box=cv2.boxPoints(rect)
            box=np.int0(box)
            img_detected=cv2.drawContours(img_detected,[box],0,(0,0,255),2)
        #cv2.imshow('rect',img)
        return img_detected

    def callback(self, img_compressed):
        img=self.bridge.compressed_imgmsg_to_cv2(img_compressed)
        img_detected=self.detector(self,img)
        img_debug=self.bridge.cv2_to_compressed_imgmsg(img_detected)
        self.pub.publish(img_debug)
        

if __name__ == '__main__':
    
    # create the node
    node = ColorDetector(node_name='colordetector')
       
    # keep spinning
    rospy.spin()