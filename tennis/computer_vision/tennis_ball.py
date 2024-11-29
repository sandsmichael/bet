# coding=utf8
'''
python tennis_ball.py --output video/tennis.avi
python tennis_ball.py --video london.mp4 --output video/london_tracked.avi  
'''
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
ap.add_argument("-o", "--output", type=str, default=64,
	help="max buffer size")
ap.add_argument("-p", "--picamera", type=int, default=-1,
                help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=20,
                help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="XVID",
                help="codec of output video")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
    # Initialize an array of FourCC, video writer, frame window width, height, 0
	fourcc = cv2.VideoWriter_fourcc(*args["codec"])
	writer = None
	(h, w) = (None, None)
	zeros = None

else:
	vs = cv2.VideoCapture(args["video"])
	width = vs.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = vs.get(cv2.CAP_PROP_FRAME_HEIGHT)
	size = (width, height)
	print(size)
	fourcc = cv2.VideoWriter_fourcc(*args["codec"])
	writer = None

# allow the camera or video file to warm up
time.sleep(6)

while True:
    # grab the current frame
	frame = vs.read()
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
    # Check whether the writer is None
	if writer is None:
        # Get the space size (width and height) of the frame, and instantiate the video stream writer
		(h, w) = frame.shape[:2]
		writer = cv2.VideoWriter(args["output"], fourcc, args["fps"],(w * 2, h * 2), True)
		zeros = np.zeros((h, w), dtype="uint8")
	(B, G, R) = cv2.split(frame)
	R = cv2.merge([zeros, zeros, R])
	G = cv2.merge([zeros, G, zeros])
	B = cv2.merge([B, zeros, zeros])

    # if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	#frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
    # otherwise, grab a reference to the video file

    # find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	# update the points queue
	pts.appendleft(center)

    # loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # Build the original image of output frame in the upper left corner red channel upper right corner green channel lower right corner blue channel lower left corner
	output = np.zeros((h * 2, w * 2, 3), dtype="uint8")
	output[0:h, 0:w] = frame
	output[0:h, w:w * 2] = R
	output[h:h * 2, w:w * 2] = G
	output[h:h * 2, 0:w] = B
    # Write frame to video
	writer.write(output)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break


# Define the codec and create VideoWriter object
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()
# otherwise, release the camera
else:
    vs.release()

# close all windows
cv2.destroyAllWindows()
writer.release()
