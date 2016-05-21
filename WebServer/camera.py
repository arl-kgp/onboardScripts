import cv2


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        self.video.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

    def __del__(self):
        self.video.release()

    def get_frame(self, frames):        
        for i in range(0, frames):
            success = self.video.grab()
            cv2.waitKey(50)
        success, image = self.video.retrieve()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tostring()

    def self_delay(self, value):
        cv2.waitKey(value)
