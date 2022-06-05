#!/usr/bin/python3
import cv2
import numpy as np


def main():
    frameWidth = 640
    frameHeight = 480
    cap = cv2.VideoCapture(2)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    while True:
        mins = np.array([110,50,50])
        max = np.array([130,255,255])
        success, img = cap.read()
        image_processed = cv2.inRange(img, mins, max)
        cv2.imshow('Coiso', image_processed)
        cv2.imshow('Result', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
if __name__ == "__main__":
    main()
