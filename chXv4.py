#!/usr/bin/env python
# coding: utf-8

# In[7]:


minWordLength = 30
minCharLength = 3
maxCharLength = 25
optBrightness = 0.805
optX = 55
charWidth = 20
optY = 18

optBFT = 0.96119084618392#fro thinning
optThresh = 200
optSens = 0.02#for seperating words
optBFW = 0.9384214743589744# opt brightness for words
chars = []

import cv2
import numpy as np
def get(img):

    def getThresh(img):
        isColor = False
        try:
            if(len(img[0,0])==3):
                isColor = True
        except:
            pass
        br = getBrightness(img, isColor)
        thresh = optThresh/optBrightness*br
        return thresh

    def threshhold(img, tc, mc=0, gc=255):
        #first is the threshhold value, the second is the one to demote all
        #the values lesser than thresh hold and the last is for the one to promote to if it is greater
        for i in range(len(img)):
            for j in range(len(img[0])):
                col = img[i,j]
                if col<=tc:
                    img[i,j] = mc
                else:
                    img[i,j] = gc
        return img

    def getThickness(img):
        checked = []
        ctr = 0
        for i in range(len(img)):
            for j in range(len(img[0])):
                try:
                    if(img[i-1,j]==0 and not ((i-1,j) in checked)):
                        checked.append((i-1,j))
                        ctr+=1
                    if(img[i+1,j]==0 and (not ((i+1,j) in checked))):
                        checked.append((i+1,j))
                        ctr+=1
                    if img[i,j+1]==0 and (not ((i,j-1) in checked)):
                        checked.append((i,j-1))
                        ctr+=1
                    if img[i,j+1]==0 and (not ((i,j+1) in checked)):
                        checked.append(((i,j+1)))
                        ctr+=1
                except:
                    pass
        return ctr/(len(img)*len(img[0]))


    def getLineThickness(img):
        mid = int(len(img)/2)
        ini = True
        ctr = 0
        bl = 0
        for i in range(len(img[0])):
            if img[mid,i]==0:
                if ini:
                    ini = False
                    ctr+=1
                bl+=1
            if(not ini and img[mid,i]==255):
                ini = True
        return bl/ctr


    def getBrightness(img,isColor = False):
        total = 0
        if(isColor):
            img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        for i in img:
            total+=sum(i)
        avg = total/(255*len(img)*len(img[0]))
        return avg



    def getSmMinimas(arr):
        minimas = []
        indi = []
        for i in range(1,len(arr)-1):
            if((arr[i]<=arr[i-1] and arr[i]<=arr[i+1] )):
                minimas.append(arr[i])
                indi.append(i)
        if(len(minimas)==0):
            return -1
        return (indi[minimas.index(min(minimas))],indi,minimas)


    def getFandNorm(img):
        freqBlack = []
        ctr = 0
        for i in range(len(img[0])):
            ctr = 0
            for j in range(len(img)):
                if img[j][i]==0:
                    ctr+=1
            freqBlack.append(ctr)
        maxi = max(freqBlack)
        for i in range(len(freqBlack)):
            if maxi>0:
                freqBlack[i]=freqBlack[i]/maxi
        return freqBlack

    freqBlack = getFandNorm(img)
    #plt.figure(figsize=(10,10), dpi= 80, facecolor='w', edgecolor='k')
    ###plt.plot(freqBlack)
    #plt.show()


    import numpy as np
    def norm(arr):
        maxi = max(arr)
        for i in range(len(arr)):
            arr[i] = arr[i]/maxi
        return arr

    def smooth(y, box_pts):
        box = np.ones(box_pts)/box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth

    smtd = smooth(freqBlack,17)#generalize this part
    smtd = norm(smtd)
  

    ###plt.plot(smtd)

    def sepComponents(smtd, sensi):
        for i in range(1,len(smtd)-1):
            if(smtd[i]<=sensi):
                smtd[i] = 0
        return smtd

    smtd = sepComponents(smtd,optSens/(1-optBFW)*(1-getBrightness(img)))
    ###plt.plot(smtd)

    def getWords(smtd):# for getting words
        ini = 0
        words = []
        word = False
        for i in range(len(smtd)):
            if(word):
                if(smtd[i] == 0 and i-ini>minWordLength):
                    words.append((ini,i))
                    word = False
            else:
                if(smtd[i]>0):
                    word = True
                    ini = i
        if smtd[-1]>0 and len(smtd) - 1 - ini>minWordLength: # checking if the last word has been left out
            words.append((ini,len(smtd)-1))
        return words

    def getChars(smtd):
        ini = 0
        indi = []
        chars = []
        char = False
        for i in range(len(smtd)):
            #print(i,smtd[i])
            if(char):
                if(smtd[i] == 0 and i-ini>minCharLength):

                    print(ini,i)
                    if(i-ini<=maxCharLength):
                        chars.append((ini,i))
                    else:
                        tmp = smtd[ini:i]
                        (gMinima,indi,minimas)=getSmMinimas(tmp)

                        while(True):

                            if(not (gMinima==-1)):
                                if(gMinima>=minCharLength):
                                    print(gMinima)
                                    mid = ini+gMinima

                                    chars.append((ini,mid))
                                    chars.append((mid,i))#add here when changing for more than qual to three letters
                                    break
                            else:
                                chars.append((ini,i))
                                break
                            ind = minimas.index(min(minimas))
                            minimas.remove(min(minimas))
                            del indi[ind]
                            #add stuff here and above when changeing for more than three letters
                            gMinima = indi[minimas.index(min(minimas))]

                    char = False 
            else:
                if(smtd[i]>0):
                    char = True
                    ini = i-1
            if smtd[-1]>0 and len(smtd) - 1 - ini>minCharLength and i==len(smtd)-2: # checking if the last word has been left out
                smtd[-1]=0
        return chars


    words = getWords(smtd)

    words

    def saveComponents(img,comps):
        imgs = []
        ctr = 0
        for i in comps:
            tmp = img[:,i[0]:i[1]]
            imgs.append(tmp)

        return imgs
    wordsImg = saveComponents(img,words)
    len(wordsImg)

    for i in range(len(wordsImg)):
        im = wordsImg[i]
        size = (len(im[0])/(1-optBrightness),len(im)/(1-optBrightness))
        dr = 1 - getBrightness(im)
        print(int(size[0]*dr),int(size[1]*dr))
        size = (int(size[0]*dr),int(size[1]*dr))
        tmp = wordsImg[i]
        if size[0] != 0 and size[1] != 0:
            tmp = wordsImg[i] = cv2.resize(im,size,interpolation = cv2.INTER_CUBIC)
        wordsImg[i] = threshhold(tmp,170)

    ##showImgs(wordsImg)

    1-getBrightness(img)

    fInWords = []
    for i in range(len(wordsImg)):
        fInWords.append(getFandNorm(wordsImg[i]))

   
    for i in range(len(fInWords)):

        idx = i
        tmp = fInWords[idx]
        tmp = sepComponents(tmp,0.07)
     #   ##plt.plot(fInWords[0])
        charIds = getChars(tmp)
        ch = saveComponents(wordsImg[i],charIds)
        for j in ch:
            chars.append(j)


def getChars(sentsImg):
    for img in sentsImg:
        get(img)
    return chars