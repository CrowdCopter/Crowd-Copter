import cv2
import lk_track
import CoherentFilter
import numpy as np
import matplotlib.pyplot as plt
import random
import dropbox


d = 7 # from t -> t+d
K = 15  # K Nearest Neighbours
lamda = 0.6 # Threshold

trajectories, numberOfFrames, lastFrame = lk_track.FindTracks()
vis = lastFrame.copy()
numberOfTracks = len(trajectories)
trajectories = np.array(trajectories)
tracksTime = np.zeros((2,numberOfTracks),dtype=int)
for i in range(numberOfTracks):
    tracksTime[0,i] = trajectories[i][0][2] # the first time when each point is appeared
    tracksTime[1,i] = trajectories[i][-1][2] # the first time when each point is appeared
''' --------------for associate------'''
trackTimeLine= np.zeros((numberOfTracks, numberOfFrames), dtype=int)
for i in range(numberOfTracks):
	trackTimeLine[i,tracksTime[0,i]:tracksTime[1,i]] =1
trackClusterTimeLine= np.zeros((numberOfTracks, numberOfFrames), dtype=int)
'''-----------------------------------'''
for i in range(1,numberOfFrames):
    #currentIndex = np.asarray(np.where(tracksTime[0].all()<=i and tracksTime[1].all()>=i),dtype=np.int)
    #جيب المسارات الي هاد الفريم هو بدايتها او نهايتها او جزأ منها
    currentIndexTmp1 = np.asarray(np.where(np.in1d(tracksTime[0], [j for j in tracksTime[0] if i>=j])))
    currentIndexTmp2 = np.asarray(np.where(np.in1d(tracksTime[1], [j for j in tracksTime[1] if j>=i])))
    currentIndexTmp1=list(currentIndexTmp1[0])
    currentIndexTmp2=list(currentIndexTmp2[0])
    currentIndex = np.array(list(set(currentIndexTmp1).intersection(set(currentIndexTmp2))))
    includeSet=[trajectories[j] for j in currentIndex]
    '''coherence filtering clustering'''
    currentAllX, clusterIndex = CoherentFilter.CoherentFilter(includeSet, i , d, K, lamda)
    ''' --------------for associate------'''
    dotForeLabel=np.asarray(np.nonzero(clusterIndex != 0))
    dotBackLabel=np.asarray(np.nonzero(clusterIndex == 0))
    if dotForeLabel != []:
        trackClusterTimeLine[currentIndex[dotForeLabel],i] = clusterIndex[dotForeLabel]
    '''-----------------------------------'''
    if clusterIndex!=[]:
        numberOfClusters = max(clusterIndex)
        color = np.array([[0,255,128],[0,0,255],[0,255,0],[255,0,0],[255,255,255],[255,255,0],[255,156,0],[50,156,0],[0,156,50]])
        #color = np.random.randint(128, 255, (numberOfClusters+1, 3))
        #finalClusterIndex = currentAllX
        counter=0
        if i==numberOfFrames-8:
            for x, y in [[np.int32(currentAllX[0][k]),np.int32(currentAllX[1][k])] for k in range(len(currentAllX[0]))]:
                #currentAllXTuple = tuple([ tuple(x) for x in currentAllX])
                cv2.circle(lastFrame, (x,y), 5, color[clusterIndex[counter]].tolist(), -1)
                counter = counter+1
            #cv2.imshow('', vis)
            cv2.imwrite('result.jpg', lastFrame)

#for z in range(10):
#cv2.imshow('Run', vis)
cv2.imwrite('result.jpg', lastFrame)
plt.pause(1)
img = cv2.imread('result.jpg')

''' uploading the result to Dropbox'''
im=open('result.jpg','rb')
f=im.read()
dbx = dropbox.Dropbox('<auth>')
try:
    dbx.files_delete('/result.jpg')
    dbx.files_upload(f, '/result.jpg')

except:
    dbx.files_upload(f, '/result.jpg')
print(dbx.files_get_metadata('/result.jpg').server_modified)

cv2.imshow('result',img)
k = cv2.waitKey(0)
'''
    if i % 5 == 0:
        mask = np.zeros_like(frame_gray)
        mask[:] = 255
        for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
            cv2.circle(mask, (x, y), 5, 0, -1)'''
'''cv2.circle(img, center, radius, color, thickness=1, lineType=8, shift=0) → None
Draws a circle.

Parameters: 
img (CvArr) – Image where the circle is drawn
center (CvPoint) – Center of the circle
radius (int) – Radius of the circle
color (CvScalar) – Circle color
thickness (int) – Thickness of the circle outline if positive, otherwise this indicates that a filled circle is to be drawn
lineType (int) – Type of the circle boundary, see Line description
shift (int) – Number of fractional bits in the center coordinates and radius value'''
print("Allah thanks for every every thing")
''' جزء الرسم ناقص بدو تكميل لا تنسى'''
#for j in range(numberOfClusters):
#    matplotlib.pyplot.scatter(currentAllX(0,np.where(clusterIndex.all()==j)), currentAllX(1,np.where(clusterIndex.all()==j)), '+')
