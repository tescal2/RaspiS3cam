#!/usr/bin/env python
from datetime import datetime
from time import sleep
import picamera
import os
import tinys3
import yaml

# testing
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# photo props
image_width = cfg['image_settings']['horizontal_res']
image_height = cfg['image_settings']['vertical_res']
file_extension = cfg['image_settings']['file_extension']
photo_interval = cfg['image_settings']['photo_interval']  # Interval between photo (in seconds)

# camera setup
camera = picamera.PiCamera()
camera.resolution = (image_width, image_height)
camera.awb_mode = cfg['image_settings']['awb_mode']

# camera warm-up time
sleep(2)  # Delay for (2 seconds).

while True:
    os.system('clear')
    unicorn = """
                                        /
                             __       //
                             -\= \=\ //
                           --=_\=---//=--
                         -_==/  \/ //\/--
                          ==/   /O   O\==--
              _ _ _ _     /_/    \  ]  /--
            /\ ( (- \    /       ] ] ]==-
           (\ _\_\_\-\__/     \  (,_,)--
          (\_/                 \     \-
          \/      /       (   ( \  ] /)
          /      (         \   \_ \./ )
          (       \         \      )  )
          (       /\_ _ _ _ /---/ /\_  )
           \     / \     / ____/ /   \  )
            (   /   )   / /  /__ )   (  )
            (  )   / __/ '---`       / /
            \  /   \ \             _/ /
            ] ]     )_\_         /__\/
            /_\     ]___\
           (___)
                  Raspberry Pi Selfie Booth 
                     
    """
    print unicorn
    print 'Hello and Welcome to the AWS Breakout Session! This Selfie Booth was created to capture your sentiment! '
    # Capture Selfie Sentiment
    sleep(4)
    print ' '
    file_name = raw_input("Please enter your first name: ")
    print ' '
    print 'Thank you, ' + file_name + '!'
    sleep(2)
    print ' '
    print 'Now it is time to show us whether you are HAPPY, SAD, or ANGRY'
    # Build filename string
    filepath = file_name + file_extension
    sleep(4)

    if cfg['debug'] == True:
        print 'Capturing Sentiment in: '
        sleep(1)
        print '3'
        sleep(1)
        print '2'
        sleep(1)
        print '1'
        sleep(1)
        print 'Cheese!'
        print ' '

    # Take Photo
    camera.capture(filepath)

    if cfg['debug'] == True:
        print 'Uploading ' + filepath + ' to secure AWS-backed storage!'
        print ' '

    # Upload to S3
    conn = tinys3.Connection(cfg['s3']['access_key_id'], cfg['s3']['secret_access_key'])
    f = open(filepath, 'rb')
    conn.upload(filepath, f, cfg['s3']['bucket_name'],
                headers={
                    'x-amz-meta-cache-control': 'max-age=60'
                })

    # Cleanup
    if os.path.exists(filepath):
        os.remove(filepath)

        # sleep
##sleep(photo_interval)
    print 'Secure Upload Complete!'
    sleep(2)
    print ' '
    print 'Selfie will be added to our Patient Sentiment Analysis Demo and deleted shortly after.'
    sleep(7)
    print ' '
    print 'Enjoy the sesion!'
    sleep(2)

## the below commented out code forces a loop exit used for testing purposes
##    raise SystemExit