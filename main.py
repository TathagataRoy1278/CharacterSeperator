import cleanImage
import LineSeperator
import chXv4
import cv2

chars = None

def get(file):
    global chars
    img = cleanImage.getCleaned(file)
    lines = LineSeperator.getLines(img)
    chars = chXv4.getChars(lines)
    print (chars,len(chars))

def showImgs(imgs):
    for i in range(len(imgs)):
        cv2.imshow(str(i),imgs[i])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    
def show():
    if len(chars)==0:
        raise Exception("CharactersNotLoaded")
    showImgs(chars)