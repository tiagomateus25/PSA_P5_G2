#!/usr/bin/env python3

# ------------------------------------------------------------
# Library's import
# ------------------------------------------------------------
import cv2
import argparse
import numpy as np
import json
import pprint
from colorama import Fore, Back, Style

# ------------------------------------------------------------
# Variables initialization
# ------------------------------------------------------------
window_name_segmentation = 'Segmentation'                                                                               # Set window name.
tkb_Names = ['min B', 'max B', 'min G', 'max G', 'min R', 'max R']                                                      # Variable with trackbars names (according to RGB).
tkb_max_value = 256                                                                                                     # Set trackbar maximum value.
tkb_min_init_value = 100                                                                                                # Set trackbar minimum initial value.


# ------------------------------------------------------------
# Functions
# ------------------------------------------------------------
def on_min_B_value_trackbar(val):
    max_B_H_value = cv2.getTrackbarPos(tkb_Names[1], window_name_segmentation)                                          # Get trackbar position (Blue/Hue maximum value).
    min_B_H_value = min(max_B_H_value - 1, val)                                                                         # Set minimum Blue/Hue value allowed.
    cv2.setTrackbarPos(tkb_Names[0], window_name_segmentation, min_B_H_value)                                           # Set trackbar position (Blue/Hue minimum value).


def on_max_B_value_trackbar(val):
    min_B_H_value = cv2.getTrackbarPos(tkb_Names[0], window_name_segmentation)                                          # Get trackbar position (Blue/Hue minimum value).
    max_B_H_value = max(val, min_B_H_value + 1)                                                                         # Set maximum Blue/Hue value allowed.
    cv2.setTrackbarPos(tkb_Names[1], window_name_segmentation, max_B_H_value)                                           # Set trackbar position (Blue/Hue maximum value).


def on_min_G_value_trackbar(val):
    max_G_S_value = cv2.getTrackbarPos(tkb_Names[3], window_name_segmentation)                                          # Get trackbar position (Green/Saturation maximum value).
    min_G_S_value = min(max_G_S_value - 1, val)                                                                         # Set minimum Green/Saturation value allowed.
    cv2.setTrackbarPos(tkb_Names[2], window_name_segmentation, min_G_S_value)                                           # Set trackbar position (Green/Saturation minimum value).


def on_max_G_value_trackbar(val):
    min_G_S_value = cv2.getTrackbarPos(tkb_Names[2], window_name_segmentation)                                          # Get trackbar position (Green/Saturation minimum value).
    max_G_S_value = max(val, min_G_S_value + 1)                                                                         # Set maximum Green/Saturation value allowed.
    cv2.setTrackbarPos(tkb_Names[3], window_name_segmentation, max_G_S_value)                                           # Set trackbar position (Green/Saturation maximum value).


def on_min_R_value_trackbar(val):
    max_R_V_value = cv2.getTrackbarPos(tkb_Names[5], window_name_segmentation)                                          # Get trackbar position (Red/Value maximum value).
    min_R_V_value = min(max_R_V_value - 1, val)                                                                         # Set minimum Red/Value value allowed.
    cv2.setTrackbarPos(tkb_Names[4], window_name_segmentation, min_R_V_value)                                           # Set trackbar position (Red/Value minimum value).


def on_max_R_value_trackbar(val):
    min_R_V_value = cv2.getTrackbarPos(tkb_Names[4], window_name_segmentation)                                          # Get trackbar position (Red/Value minimum value).
    max_R_V_value = max(val, min_R_V_value + 1)                                                                         # Set maximum Red/Value value allowed.
    cv2.setTrackbarPos(tkb_Names[5], window_name_segmentation, max_R_V_value)                                           # Set trackbar position (Red/Value maximum value).


def testDevice(capture, source):
    if capture is None or not capture.isOpened():                                                                                           # Check if camera index it's valid.
        print(Fore.YELLOW + Style.BRIGHT + 'Color segmentation Finished. Unable to open video source: ' + str(source) + Style.RESET_ALL)    # Program finished message.
        exit()                                                                                                                              # Stops the program.


def main():
    # ------------------------------------------------------------
    # INITIALIZATION
    # ------------------------------------------------------------
    global tkb_Names

    parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
    parser.add_argument('-cn', '--camera_number', type=int, help='Camera number (Default = 0).', default=0)
    args = vars(parser.parse_args())

    if args.get('camera_number') < 0:                                                                                   # Check if 'camera_number' input is valid.
        print(Fore.RED + Style.BRIGHT + 'error: Invalid input argument!' + Style.RESET_ALL)                             # Error message.
        exit()                                                                                                          # Stops the program.

    print('\n========== PSR Ar Paint - Color Segmenter(Grupo 2) ==========\n')  # Initial message.
    print('    => To change camera, use -cn or --camera_number (default is 0)')  # Initial message.
    print('    => There are 6 Trackbars available to change the RGB parameters')  # Initial message.
    print('    => Trackbar min B changes the minimum value of ' + Fore.BLUE + Style.BRIGHT + 'blue ' + Style.RESET_ALL )  # Initial message.
    print('    => Trackbar max B changes the maximum value of ' + Fore.BLUE + Style.BRIGHT + 'blue ' + Style.RESET_ALL)  # Initial message.
    print('    => Trackbar min G changes the minimum value of ' + Fore.GREEN + Style.BRIGHT + 'green ' + Style.RESET_ALL)  # Initial message.
    print('    => Trackbar max G changes the maximum value of ' + Fore.GREEN + Style.BRIGHT + 'green ' + Style.RESET_ALL)  # Initial message.)  # Initial message.
    print('    => Trackbar min R changes the minimum value of ' + Fore.RED + Style.BRIGHT + 'red ' + Style.RESET_ALL )  # Initial message.
    print('    => Trackbar max R changes the maximum value of ' + Fore.RED + Style.BRIGHT + 'red ' + Style.RESET_ALL)  # Initial message.
    print('\n=> Keys that you can press.')  # Preliminary notes
    print('    => ' + Fore.YELLOW + Style.BRIGHT + '"w" ' + Style.RESET_ALL + 'or ' + Fore.YELLOW + Style.BRIGHT + '"W" ' + Style.RESET_ALL + 'key -> Save the chosen RGB parameters and exits program!')  # Preliminary notes
    print('    => ' + Fore.YELLOW + Style.BRIGHT + '"q" ' + Style.RESET_ALL + 'or ' + Fore.YELLOW + Style.BRIGHT + '"Q" ' + Style.RESET_ALL + 'key -> Exits program without saving RGB parameters!')  # Preliminary notes

    capture = cv2.VideoCapture(args.get('camera_number'))
    testDevice(capture, args.get('camera_number'))                                                                      # Call 'testDevice' function to check if selected camera is available.

    cv2.namedWindow(window_name_segmentation, cv2.WINDOW_AUTOSIZE)                                                      # Window Setup.

    cv2.createTrackbar(tkb_Names[0], window_name_segmentation, tkb_min_init_value, tkb_max_value, on_min_B_value_trackbar)        # Create trackbars (Minimum Blue/Hue color).
    cv2.createTrackbar(tkb_Names[1], window_name_segmentation, tkb_max_value, tkb_max_value, on_max_B_value_trackbar)             # Create trackbars (Maximum Blue/Hue color).
    cv2.createTrackbar(tkb_Names[2], window_name_segmentation, tkb_min_init_value, tkb_max_value, on_min_G_value_trackbar)        # Create trackbars (Minimum Green/Saturation color).
    cv2.createTrackbar(tkb_Names[3], window_name_segmentation, tkb_max_value, tkb_max_value, on_max_G_value_trackbar)             # Create trackbars (Maximum Green/Saturation color).
    cv2.createTrackbar(tkb_Names[4], window_name_segmentation, tkb_min_init_value, tkb_max_value, on_min_R_value_trackbar)        # Create trackbars (Minimum Red/Value color).
    cv2.createTrackbar(tkb_Names[5], window_name_segmentation, tkb_max_value, tkb_max_value, on_max_R_value_trackbar)             # Create trackbars (Maximum Red/Value color).

    # ------------------------------------------------------------
    # EXECUTION
    # ------------------------------------------------------------
    while True:
        _, image = capture.read()                                                                                       # Get an image from the camera and store them at "image" variable.
        if image is None:                                                                                               # Check if there are no camera image.
            print(Fore.YELLOW + Style.BRIGHT + 'Video is over, terminating.' + Style.RESET_ALL)                         # Test finished message.
            break                                                                                                       # Break/Stops the loop.

        B_min = cv2.getTrackbarPos(tkb_Names[0], window_name_segmentation)                                              # Get trackbars positions (Minimum Blue/Hue color).
        B_max = cv2.getTrackbarPos(tkb_Names[1], window_name_segmentation)                                              # Get trackbars positions (Maximum Blue/Hue color).
        G_min = cv2.getTrackbarPos(tkb_Names[2], window_name_segmentation)                                              # Get trackbars positions (Minimum Green/Saturation color).
        G_max = cv2.getTrackbarPos(tkb_Names[3], window_name_segmentation)                                              # Get trackbars positions (Maximum Green/Saturation color).
        R_min = cv2.getTrackbarPos(tkb_Names[4], window_name_segmentation)                                              # Get trackbars positions (Minimum Red/Value color).
        R_max = cv2.getTrackbarPos(tkb_Names[5], window_name_segmentation)                                              # Get trackbars positions (Maximum Red/Value color).

        mins = np.array([B_min, G_min, R_min])                                                                          # Gets minimum RGB/HSV color values from dictionary.
        maxs = np.array([B_max, G_max, R_max])                                                                          # Gets maximum RGB/HSV color values from dictionary.
        image_processed = cv2.inRange(image, mins, maxs)                                                                # Process original image/video according to RGB/HSV color values range.

        cv2.imshow(window_name_segmentation, image_processed)                                                           # Display the processed image/video.

        # ------------------------------------------------------------
        # TERMINATION
        # ------------------------------------------------------------
        key = cv2.waitKey(20)

        if (key == ord('q')) or (key == ord('Q')) or (cv2.getWindowProperty(window_name_segmentation, 1) == -1):        # Check if user pressed the 'q' key or closed the window.
            print(Fore.YELLOW + Style.BRIGHT + 'Color segmentation Finished without store data in json file.' + Style.RESET_ALL)  # Program finished message.
            exit()                                                                                                      # Stops the program.
        elif (key == ord('w')) or (key == ord('W')):                                                                    # Check if user pressed the 'w' key.

            ranges = {'B': {'max': B_max, 'min': B_min},                                                                # Dictionary to store minimum and maximum RGB/HSV color values (Blue/Hue).
                      'G': {'max': G_max, 'min': G_min},                                                                # Dictionary to store minimum and maximum RGB/HSV color values (Green/Saturation).
                      'R': {'max': R_max, 'min': R_min}}                                                                # Dictionary to store minimum and maximum RGB/HSV color values (Red/Value).

            dict_result = {'limits': ranges}                                                                            # Creation of the dictionary.

            file_name = 'limits.json'                                                                                   # Creation of .json file.
            print('\n============================= Results =============================\n')                            # Results message.
            json.dump(dict_result, open(file_name, 'w'))                                                                # Save results at .json file.
            pp = pprint.PrettyPrinter(indent=1)                                                                         # Set the dictionary initial indentation.
            pp.pprint(dict_result)                                                                                      # Print the entire dictionary.
            break                                                                                                       # Break/Stops the loop.


if __name__ == '__main__':
    main()
