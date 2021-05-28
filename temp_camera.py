import picamera
import time
#import threading
import multiprocessing

# def start():
#     with picamera.PiCamera() as camera:
#         camera.resolution = (2592, 1944)
#         time.sleep(1) # Camera warm-up time
#         for filename in enumerate(camera.capture_continuous('./data/image-{timestamp:%Y-%m-%d-%H-%M-%S}.jpg')):
#             #print("Captured {}".format(filename))
#             time.sleep(5)

def start():
    for i in range(10000):
        with picamera.PiCamera() as camera:
            camera.resolution = (2592, 1944)
            time.sleep(1) # Camera warm-up time
            filename = './data/image-x-%02d.jpg' % i
            camera.capture(filename)
            print('Captured %s' % filename)
        
        time.sleep(4)
            


#thread = threading.Thread(target=start, name="PictureCapturerThread")
#thread.start()

#p = multiprocessing.Process(target=start)
#p.start()
#time.sleep(15)
#p.kill()

start()