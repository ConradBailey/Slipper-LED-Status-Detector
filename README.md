# Slipper LED Status Detector

## The Problem
This Christmas my awesome girlfriend got me the best present: [heated slippers](https://www.firebox.com/Yeti-Heated-Slippers/p7228?mkt=en-us).

I _suffer_ from chronically cold feet in the winter, and these do just the trick. Mine came with batteries that charge via USB. While they're charging the LED is [red](https://www3.nd.edu/~cbailey8/blog/2017/01/06/detecting_led_changes_with_raspicam/red.jpg), but when they're full they switch to [blue](https://www3.nd.edu/~cbailey8/blog/2017/01/06/detecting_led_changes_with_raspicam/blue.jpg). I wanted a text alert when that happened so I didn't have to keep checking on them.

## The Solution
My whole process is outlined in my [blog post](https://www3.nd.edu/~cbailey8/blog/2017/01/06/detecting_led_changes_with_raspicam/).

## TL;DR

I used [OpenCV's Python bindings](http://docs.opencv.org/3.2.0/) to process pictures of my slipper batteries on a [Raspberry Pi](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/). I schedule that script with a [systemd timer](https://wiki.archlinux.org/index.php/Systemd/Timers) to run every minute; it sends me a text via [IFTTT](https://ifttt.com/discover) if they're done charging