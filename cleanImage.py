#!/usr/bin/env python
# coding: utf-8

# In[2]:


minWordLength = 30
minCharLength = 10
maxCharLength = 25
optBrightness = 0.96119084618392
optThresh = 200#change this to 200


# In[3]:


import cv2
import numpy as np


# In[4]:

def getCleaned(file):
	def seperateCols(img):
		blue = []
		green = []
		red = []
		for i in range(len(img)):
			tBlue = []
			tGreen = []
			tRed = []
			for j in range(len(img[0])):
				col = img[i,j]
				tBlue.append(col[0])
				tGreen.append(col[1])
				tRed.append(col[2])
			blue.append(tBlue)
			green.append(tGreen)
			red.append(tRed)
		return (np.array(blue),np.array(green),np.array(red))



	# In[5]:


	def getThresh(img):
		isColor = False
		if(len(img[0,0])==3):
			isColor = True
		br = getBrightness(img, isColor)
		thresh = optThresh/optBrightness*br
		return thresh


	# In[6]:



	def getBrightness(img,isColor = False):
		total = 0
		if(isColor):
			img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		for i in img:
			total+=sum(i)
		avg = total/(255*len(img)*len(img[0]))
		return avg


	# In[7]:




	# In[8]:


	def threshhold(img, tc, mc=(0,0,0), gc=(255,255,255)):
		#first is the threshhold value, the second is the one to demote all
		#the values lesser than thresh hold and the last is for the one to promote to if it is greater
		(t_r,t_g,t_b) = tc
		(mr,mg,mb) = mc
		(gr,gg,gb) = gc
		for i in range(len(img)):
			for j in range(len(img[0])):
				col = img[i,j]
				if (col[2]<=t_r) and (col[1]<=t_g) and (col[0]<=t_b):
					img[i,j] = [mb,mg,mr]
				else:
					img[i,j] = [gb,gg,gr]
		img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		return img


	# In[10]:


	def notEmpty(img):
		emp = True
		for i in img:
			for j in i:
				if j == 255:
					emp = False
		return not emp


	# In[11]:


	def op(tmp):
		tmp = cv2.erode(tmp,np.ones((3,3)),iterations = 1)
		tmp = cv2.dilate(tmp,np.ones((2,2)),iterations = 1)
		return tmp


	# In[12]:


	img = cv2.imread(file)


	thresh = getThresh(img)

	img = threshhold(img,(thresh,thresh,thresh))

	skel = np.zeros([len(img),len(img[0])],dtype = np.uint8)
	tmp = 255 - img
	print(tmp.shape,skel.shape)
	while notEmpty(tmp):
		skel = cv2.bitwise_or(skel, cv2.bitwise_and(tmp,cv2.bitwise_not(op(tmp))))
		tmp = cv2.erode(tmp,np.ones((3,3)),iterations = 1)
	img = 255-skel

	return img


