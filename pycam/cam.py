
import numpy as np
import os
import cv2
import time
import smtplib
import sys

filename = 'video0.mp4'
frames_per_second = 10
res = '480p'


CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com",
    'gmail': '@gmail.com'
}
# put email and password to get emails
# add carriers or emails if you want above
#  like outlook etc.
EMAIL = "your email here"
PASSWORD = "password here"


def send_message(phone_number, carrier, message):
    recipient = phone_number + CARRIERS[carrier]
    auth = (EMAIL, PASSWORD)

    server = smtplib.SMTP("smtp.office365.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    server.sendmail(auth[0], recipient, message)
# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh


def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


# Standard Video Dimensions Sizes
STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]
    # change the current caputre device
    # to the resulting resolution
    change_res(cap, width, height)
    return width, height


# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}


def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['mp4']


cap = cv2.VideoCapture(1)
out = cv2.VideoWriter(filename, get_video_type(filename),
                      frames_per_second, get_dims(cap, res))
seconds = time.time()
x = 0
y = 0
arr = []
# initial message
# add your email name (everthing before @ symbol ONLY) below as the first parameter
send_message('put email name (everything before @ symbol)', 'gmail', 'new video')
while True:
    first = time.time()
    # records videos in intervals of 10 minutes
    # and saves them.
    if (time.time() - seconds) > 600:
        out.release()
        filename = 'video' + str(x) + '.mp4'
        out = cv2.VideoWriter(filename, get_video_type(
            filename), frames_per_second, get_dims(cap, res))
        x += 1
        send_message('put email name (everything before @ symbol)', 'gmail', 'new video')
        seconds = time.time()

    ret, frame = cap.read()
    out.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    sec = time.time()
    arr.append(sec-first)

print('avg', sum(arr)/len(arr))
cap.release()
out.release()
cv2.destroyAllWindows()
