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
    while True:
        _, image = capture.read()  # get an image from the camera
        image_processed = cv2.inRange(image, mins, maxs)
        
        m = cv2.moments(image_processed)
        print(m)
        # x = m['m10']/m['m00']
        # y = m['m01']/m['m00']
        # print('x=',x, 'y=',y)
        if m['m00'] == 0:
            pass
        else:

            x = m['m10']/m['m00']
            y = m['m01']/m['m00']

            # add code to show acquired image
            # cv2.circle(image_processed, (int(x),int(y)), 5, 255, 5)

            cv2.circle(image_processed, (int(x), int(y)), 10, (0, 0, 255), -1)
            cv2.imshow(window_name2, image_processed)
            cv2.circle(image, (int(x), int(y)), 10, (0, 0, 255), -1)
            cv2.imshow(window_name, image)
            # add code to wait for a key press
            cv2.waitKey(20)


if __name__ == '__main__':
    main()
