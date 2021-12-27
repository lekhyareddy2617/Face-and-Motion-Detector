from datetime import datetime
import cv2,time,pandas

first_frame=None
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=["Start","End"]) #DataFrame used for storing time values during which object detection and movement happens

video=cv2.VideoCapture(0,cv2.CAP_DSHOW)

while True:
    check,frame=video.read()
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)
    if first_frame is None: #for first image/frame of video
        first_frame=gray
        continue
    delta_frame=cv2.absdiff(first_frame,gray) #diff btwn first and other frames
    thresh_delta=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1] #convert the difference with value<30 to black and if value>30, pixels turned to white
    thresh_delta=cv2.dilate(thresh_delta,None,iterations=0) #same as prev line
    cnts,_=cv2.findContours(thresh_delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #defines area to add borders

    for contour in cnts: 
        if cv2.contourArea(contour)<1000: #remove noise and shadows; if area>1000 pixels, part is kept white
            continue
        status=1 #change in status when object is detected
        (x,y,w,h)=cv2.boundingRect(contour) #creates rectangle
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    status_list.append(status)
    status_list=status_list[-2:] #second last value

    if(status_list[-1]==1 and status_list[-2]==0):
        times.append(datetime.now())
    if(status_list[-1]==0 and status_list[-2]==1):
        times.append(datetime.now())
    
    cv2.imshow("Frame",frame)
    cv2.imshow("Capturing",gray)
    cv2.imshow("Delta",delta_frame)
    cv2.imshow("Thresh",thresh_delta)

    key=cv2.waitKey(1)
    if key==ord('q'):
        break

print(status_list)
print(times)

for i in range(0,len(times),2):
    df=df.append({"Start":times[i-1],"End":times[i]},ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows

