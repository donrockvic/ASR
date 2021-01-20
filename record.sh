#!/bin/bash

sudo ffmpeg -f alsa -i hw:CARD=PCH,DEV=0 as.wav