'''This is some documentation'''
import datetime
import time
import cv2 as cv
import numpy as np


def within_range(percentage: int, value1: int, value2: int) -> bool:
    '''Checks to see if value1 is within percentage of value2'''
    perc = value1 * (percentage / 100)

    if value2 - perc < value1 < value2 + perc:
        return True
    else:
        return False


def get_frame_difference(old_frame, new_frame):
    '''Calculated the disserence between frames'''
    old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)
    new_gray = cv.cvtColor(new_frame, cv.COLOR_BGR2GRAY)
    diff = new_frame

    return diff


def get_frame(cap):
    '''Collects a frame from the camera'''
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
    return frame


def main():
    ''' This is the main method for this module '''
    cap = cv.VideoCapture(0)
    fourcc = cv.VideoWriter_fourcc(*"XVID")
    output = cv.VideoWriter(
        f'{datetime.datetime.now().date()}_{time.time()}.avi', fourcc, 20.0, (640, 480))

    while True:
        frame = get_frame(cap)
        output.write(frame)
        cv.imshow("Security Feed", frame)
        key = cv.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

    cap.release()
    output.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    # main()
    print(f'{datetime.datetime.now().date()}_{time.time()}.avi')
