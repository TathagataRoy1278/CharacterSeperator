#!/usr/bin/env python
# coding: utf-8

# In[43]:


minLineLength = 5


# In[44]:


import numpy as np
import cv2


# In[45]:
def getLines(img):

	


	# In[46]:


	def getFandNorm(img):
		freqBlack = []
		ctr = 0
		for i in img:
			ctr = 0
			for j in i:
				if j==0:
					ctr+=1
			freqBlack.append(ctr)
		maxi = max(freqBlack)
		for i in range(len(freqBlack)):
			freqBlack[i]=freqBlack[i]/maxi
		return freqBlack

	freq = getFandNorm(img)
	##plt.plot(freq)
	#plt.show()


	# In[51]:



	def smooth(y, box_pts):
		box = np.ones(box_pts)/box_pts
		y_smooth = np.convolve(y, box, mode='same')
		return y_smooth

	smtd = smooth(freq,1)
	##plt.plot(smtd)


	# In[53]:


	def sepComponents(smtd, sensi):
		for i in range(1,len(smtd)-1):
			if(smtd[i]<=sensi):
				smtd[i] = 0
		return smtd
	smtd = sepComponents(smtd,0.03)
	##plt.plot(smtd)
	print(smtd[1])


	# In[54]:


	def getComponents(smtd,minLength):
		ini = 0
		words = []
		word = False
		for i in range(len(smtd)):
			if(word):
				if(smtd[i] == 0 and i-ini>minLength):
					words.append((ini,i))
					word = False
			else:
				if(smtd[i]>0):
					word = True
					ini = i
		if smtd[-1]>0 and len(smtd) - 1 - ini>minLength: # checking if the last word has been left out
			words.append((ini,len(smtd)-1))
		return words
	sents = getComponents(smtd,minLineLength)


	# In[55]:


	sents


	# In[56]:


	def saveComponents(img,comps):
		imgs = []
		ctr = 0
		for i in comps:
			tmp = img[i[0]:i[1],:]
			imgs.append(tmp)
		return imgs
	sentsImg = saveComponents(img,sents)


	# In[57]:


	def showImgs(imgs):
		for i in range(len(imgs)):
			cv2.imshow(str(i),imgs[i])
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	#showImgs(sentsImg)

	return sentsImg
	# In[42]:





