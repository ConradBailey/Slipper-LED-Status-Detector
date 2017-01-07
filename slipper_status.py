#!/usr/bin/python2

# Copyright (C) 2017 Conrad Bailey
# This software is distributed under the GNU General Public License.
# See the file COPYING for details.

from keys import *
import cv2
import numpy as np
import subprocess
import requests
import tempfile
import os

def main():
  tmpname = tempfile.mkstemp(suffix='.jpg')[1]
  raspistill = ['/opt/vc/bin/raspistill','-w','320','-h','240','-t','1','-o',tmpname]
  try:
    subprocess.check_call(raspistill)
  except Exception as e:
    print 'Error taking the photo'
    return 1

  img = cv2.imread(tmpname,0)
  if (cv2.mean(img)[0] < 20):
    night()
  else:
    subprocess.check_call(raspistill + ['-ex','spotlight','-ss','20000'])
    day(cv2.imread(tmpname))

  os.remove(tmpname)
  return

def day(img):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]

  params = cv2.SimpleBlobDetector_Params()
  params.blobColor = 255;
  params.filterByArea = False
  params.filterByCircularity = False
  params.filterByConvexity = False
  params.filterByInertia = False

  detector = cv2.SimpleBlobDetector_create(params)

  keypoints = detector.detect(thresh)

  height,width,depth = img.shape
  for keypoint in keypoints:
    mask = np.zeros((height,width), np.uint8)
    cv2.circle(mask, (int(keypoint.pt[0]),int(keypoint.pt[1])), int(keypoint.size/2), (255,255,255), -1)
    mean = cv2.mean(img,mask=mask)
    if (mean[0] <= mean[2]):
      print 'Charging'
      return 0

  print 'Charged'

  ifttt_url = 'https://maker.ifttt.com/trigger/slippers_charged/with/key/{}'.format(IFTTT_MAKER_KEY)
  try:
    requests.post(ifttt_url)
  except:
    print 'Error making POST request to {}'.format(ifttt_url)
    return 1

  try:
    subprocess.check_call(['/usr/bin/systemctl','stop','slipper_status.timer'])
  except:
    print 'Error ending service'
    return 1

  return 0

def night():
  print 'night mode'
  return

if __name__ == "__main__":
  main()

