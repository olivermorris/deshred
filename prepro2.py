import cv2
import numpy as np
import os
import imutils
from easyocr import Reader
import time
a1 = 0
a2 = 1
counter = 0
diflist = []
areas = []
images = []
rotated_shreds = []
cropped_shreds = []
final_images = []
word_list = []
f_list = []
idx = 0


scan = cv2.imread('test3.jpeg')

height = scan.shape[0]
width = scan.shape[1]
DrawnContours = np.zeros(shape=[height, width, 3], dtype=np.uint8)
blank_image2 = np.zeros(shape=[height, width, 3], dtype=np.uint8)

#grayscales the image
gray = cv2.cvtColor(scan, cv2.COLOR_BGR2GRAY)
gaus = cv2.GaussianBlur(gray, (3,3),0)

canny_output = cv2.Canny(gaus,50,50)

StripConts, hierarchy= cv2.findContours(canny_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(DrawnContours, StripConts, -1, (255,255,255),12)
cv2.imwrite('opencv.jpeg',DrawnContours)
DrawnContoursgray = cv2.cvtColor(DrawnContours, cv2.COLOR_BGR2GRAY)
DrawConts, hierarchy= cv2.findContours(DrawnContoursgray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


sorted_contours= sorted(DrawConts, key=cv2.contourArea, reverse= True)

for contour in sorted_contours:
        measure = cv2.contourArea(contour)
        areas.append(measure)
        print(measure)


for area in areas:
    try:
        dif = areas[a1]-areas[a2]
        diflist.append(dif)
        a1 += 1
        a2 += 1
    except:
        break

maximum = max(diflist)

del diflist[0]


number = (diflist.index(maximum)+2)

print(number)


for c in sorted_contours:
    if idx >= number:
        break
    else:
        x,y,w,h = cv2.boundingRect(c)
        new_img=scan[y:y+h,x:x+w]
        images.append(new_img)
        idx+=1

for image in images:
        try:
            shred_gaus = cv2.GaussianBlur(image, (3,3),0)
            shred_canny_output = cv2.Canny(shred_gaus, 130, 130)
            ShredCont, hierarchy = cv2.findContours(shred_canny_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            sorted_contours= sorted(ShredCont, key=cv2.contourArea, reverse= True)
            cnt = sorted_contours[1]
            rect = cv2.minAreaRect(cnt)
            angle = rect[2]
            if angle < 0:
                rotguide = -90 +abs(angle)
                print(rotguide)
            else:
                rotguide = 90 - angle
                print(rotguide)
            rotated_shred = imutils.rotate_bound(image, rotguide)
            rotated_shreds.append(rotated_shred)
            cv2.imwrite('rotated_shred.jpeg',rotated_shred)

        except:
            counter = 100
for rotated_shed in rotated_shreds:
    final_gray = cv2.cvtColor(rotated_shed, cv2.COLOR_BGR2GRAY)
    gaus_img = cv2.GaussianBlur(final_gray, (3,3),0)
    ret, binarycont = cv2.threshold(gaus_img, 0, 255, cv2.THRESH_BINARY)
    ret, binarytext = cv2.threshold(gaus_img, 200, 255, cv2.THRESH_BINARY)
    LargeCont, hierarchy = cv2.findContours(binarycont, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_Large_Cont = sorted(LargeCont, key=cv2.contourArea, reverse= True)
    x,y,w,h = cv2.boundingRect(sorted_Large_Cont[0])
    new_img=binarytext[y:y+h,x:x+w]
    final_images.append(new_img)

cv2.imwrite('binary.jpeg',final_images[0])




def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()

# construct the argument parser and parse the arguments
'''
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argumenti("-l", "--langs", type=str, default="en",
	help="comma separated list of languages to OCR")
ap.add_argument("-g", "--gpu", type=int, default=-1,
	help="whether or not GPU should be used")
args = vars(ap.parse_args())
'''

# break the input languages into a comma separated list
for show_image in final_images:
    langs = ('en').split(",")
    print("[INFO] OCR'ing with the following languages: {}".format(langs))

    # load the input image from disk
    imageread = show_image
    # OCR the input image using EasyOCR
    print("[INFO] OCR'ing input image...")
    reader = Reader(langs)
    results = reader.readtext(imageread)

    # loop over the results
    for (bbox, text, prob) in results:
        word_list.append(text)
    print(word_list)
    word_list.append("J(&?`^")
    # show the output image
print(word_list)
