#!/usr/bin/env python3
import os
import random
import argparse
import copy
import math
import cv2
from colorama import Fore, Back, Style
import numpy as np
import json
import datetime
import colorsys


def main():
    f = open('limits.json')
    data = json.load(f)
    mins = np.array([data['limits']['B']['min'], data['limits']['G']['min'], data['limits']['R']['min']])  # Gets minimum RGB color values from data variable.
    maxs = np.array([data['limits']['B']['max'], data['limits']['G']['max'], data['limits']['R']['max']])
    # image_processed = cv2.inRange(image, mins, maxs)
    capture = cv2.VideoCapture(0)
    window_name = 'Original'
    window_name2 = 'Processed'
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(window_name2, cv2.WINDOW_AUTOSIZE)

    _, image = capture.read()
    #parte de optical flow
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = np.zeros_like(image)
    mask[..., 1] = 255


    while True:
        _, image = capture.read()  # get an image from the camera
        image_processed = cv2.inRange(image, mins, maxs)
        #parte de optcial flow
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray,
                                       None,
                                       0.5, 3, 15, 3, 5, 1.2, 0)
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        mask[..., 0] = angle * 180 / np.pi / 2
        mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
        cv2.imshow("dense optical flow", rgb)
        #print(flow)
        #print(magnitude[0])
        m = cv2.moments(image_processed)

        if m['m00'] == 0:

            cv2.imshow(window_name2, image_processed)
            cv2.imshow(window_name, image)
            cv2.waitKey(20)
        else:
            w = []
            x = m['m10']/m['m00']
            y = m['m01']/m['m00']
            z = [x,y]
            w.append(z)

            for i in range(len(w)):
                #x = m['m10']/m['m00']
                #y = m['m01']/m['m00']
                #z = [x,y]

                f = np.array(w[i-1][0])
                g = np.array(w[i][0])
                h = abs(f - g)
                print(h)





                # eeadd code to show acquired image
                # cv2.circle(image_processed, (int(x),int(y)), 5, 255, 5)
                cv2.circle(image_processed, (int(x), int(y)), 10, (0, 0, 255), -1)
                cv2.imshow(window_name2, image_processed)
                cv2.circle(image, (int(x), int(y)), 10, (0, 0, 255), -1)
                cv2.imshow(window_name, image)
                # add code to wait for a key press
                cv2.waitKey(20)



if __name__ == '__main__':
    main()









