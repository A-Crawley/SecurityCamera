# USAGE
# python motion.py
# arguments:
#   -r / --record [0,1]
#   -f / --feed [0,1]
#   -bb / --bounding_boxes [0,1]
#   -os / --occupation_stamp [0,1]
#   -ts / --time_stamp [0,1]
#   -ut / --unoccupied_ticks [25 <= x <= 2500]

# Requires
#
# python -m pip install opencv-python
# python -m pip install imutils

# import the necessary packages
import datetime
import time
from pathlib import Path
import argparse
import imutils
import cv2

FOOTAGE_FOLDER = 'security_footage'


class Settings:
    '''Houses the settings for the security camera'''

    def __init__(self):
        self.bounding_boxes = False
        self.feed = True
        self.occupation_stamp = True
        self.time_stamp = True
        self.record = False
        self.unoccupied_ticks = 100


class Camera:
    '''Defines a camera object'''

    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.output = None
        self.occupied = False
        self.root_folder = f'.\\{FOOTAGE_FOLDER}\\'

    def cleanup(self):
        '''Cleans up the camera'''
        self.capture.release()
        if self.output is not None:
            self.output.release()
        cv2.destroyAllWindows()

    def calculate_buffer(self, unoccupied_buffer: int, text: str) -> tuple:
        '''Calculates the remaining unoccupied buffer time'''
        if self.occupied is False and unoccupied_buffer > 0:
            self.occupied = True
            unoccupied_buffer -= 1
            return ("Occupied", unoccupied_buffer)
        return (text, unoccupied_buffer)

    def check_occupation(self, record: bool, frame):
        '''Checks to see if the room is occupied and records'''
        if self.occupied and record:
            if self.output is None:
                self.output = cv2.VideoWriter(
                    f'{self.root_folder}{datetime.datetime.now().date()}_{time.time()}.avi',
                    self.fourcc, 29.95, (640, 480))
                print("Created Video Writer")
            else:
                self.output.write(frame)
        else:
            if self.output is not None:
                self.output.release()
                self.output = None
                print("Wrote video to file")


def main(settings: Settings):
    '''Defines the main function of the security camera'''
    camera = Camera()

    # initialize the first frame in the video stream
    first_frame = None

    # Holds the unoccupied ticks amount
    unoccupied_buffer = settings.unoccupied_ticks

    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        ret, frame = camera.capture.read()
        text = "Unoccupied"

        camera.occupied = False

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if ret is None:
            break

        # resize the frame, convert it to grayscale, and blur it
        #frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if first_frame is None:
            first_frame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frame_delta = cv2.absdiff(first_frame, gray)
        thresh = cv2.threshold(frame_delta, 50, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=1)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 500:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            if settings.bounding_boxes:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"
            first_frame = gray
            camera.occupied = True
            if unoccupied_buffer != settings.unoccupied_ticks:
                unoccupied_buffer = settings.unoccupied_ticks

        text, unoccupied_buffer = camera.calculate_buffer(
            unoccupied_buffer, text)

        # draw the text and timestamp on the frame
        if settings.occupation_stamp:
            cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        if settings.time_stamp:
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0), 1)

        # Checks to see if the room is occupied and writes to a video file
        camera.check_occupation(settings.record, frame)

        # show the frame
        if settings.feed:
            cv2.imshow("Security Feed", frame)
            cv2.imshow("Thresh", thresh)
            cv2.imshow("Frame Delta", frame_delta)

        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

    # cleanup the camera and close any open windows
    camera.cleanup()


def custom_integer(x):
    value = int(x)
    if 25 <= value <= 2500:
        return value
    raise argparse.ArgumentTypeError(f'{x}: is not a valid integer')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Learning to parse arguments')
    parser.add_argument('-bb', '--bounding_boxes', default=0,
                        type=int, choices=[0, 1], help='Display the bounding boxes')
    parser.add_argument('-f', '--feed', default=0,
                        type=int, choices=[0, 1], help='Display the feeds')
    parser.add_argument('-os', '--occupation_stamp', default=0,
                        type=int, choices=[0, 1], help='Write the occupation stamp to frame')
    parser.add_argument('-ts', '--time_stamp', default=1,
                        type=int, choices=[0, 1], help='Write the time stamp to frame')
    parser.add_argument('-r', '--record', default=0,
                        type=int, choices=[0, 1], help='Record any motion that is tracked')
    parser.add_argument('-ut', '--unoccupied_ticks', default=50,
                        type=custom_integer,
                        help='The amount of ticks buffer between occupied and unoccupied statuses (25 <= x <= 2500)')
    args = parser.parse_args()

    Path(F'.\\{FOOTAGE_FOLDER}').mkdir(parents=True, exist_ok=True)

    camera_settings = Settings()

    camera_settings.bounding_boxes = args.bounding_boxes
    camera_settings.feed = args.feed
    camera_settings.occupation_stamp = args.occupation_stamp
    camera_settings.time_stamp = args.time_stamp
    camera_settings.record = args.record
    camera_settings.unoccupied_ticks = args.unoccupied_ticks

    main(camera_settings)
