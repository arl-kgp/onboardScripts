import cv2

cap=cv2.VideoCapture(0)#Access default WebCam

width,height=1920,1080 #Aspect ratio of Video to be saved
fps=10 #required fps 
fourcc = cv2.cv.CV_FOURCC('D','I','V','X')#FourCC code for AVI format
w = cv2.VideoWriter('out1.AVI', fourcc, fps, (width, height), 1)#see blog

#raw_input('Press Enter to start saving video ,and Esc to Stop and Quit')

while(True):
    
    f,frame=cap.read()
    frame=cv2.resize(frame,(width,height)) 
    w.write(frame)#write frame to video file
    #cv2.imshow('frame',frame)
    #cv2.waitKey(100)

cap.release()

cv2.destroyAllWindows()
