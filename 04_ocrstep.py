# from https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052

import cv2
from PIL import Image
import csv
import numpy as np

### PART 3
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/Users/sethfrey/opt/anaconda3/envs/py39/bin/tesseract'
# load the original image
image = cv2.imread('Page_0.jpg')

line_items_coordinates = []
#row1col1
line_items_coordinates.append([(97,1840),(1332,1904)])
#row1col2
line_items_coordinates.append([(1329,1840),(1750,1904)])
#row2col1
line_items_coordinates.append([(97,1901),(1332,1965)])
#row2col2
#line_items_coordinates.append([(1331,1903),(1745,1960)])
line_items_coordinates.append([(1329,1901),(1750,1965)])
#row3col1
line_items_coordinates.append([(97,1961),(1332,2021)])
#row3col2
line_items_coordinates.append([(1329,1961),(1750,2021)])

with open('form7.csv', 'w', newline='') as csvfile:
    ocrout = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #fieldnames = ['ITEM', 'LAST YEAR (a)']
    #ocrout.writerow(fieldnames)

    ncolumns = 2
    row = 0
    row_content = []
    for i, c in enumerate(line_items_coordinates):
        # cropping image img = image[y0:y1, x0:x1]
        img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]    

        # previewing
        #plt.figure(figsize=(10,10))
        #plt.imshow(img)
        cv2.imwrite("./snippet{}.jpg".format(i), img)

        # convert the image to black and white for better OCR
        ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY)
        cv2.imwrite("./snippet_post{}.jpg".format(i), thresh1)

        # pytesseract image to string to get results
        tessout = pytesseract.image_to_string(thresh1, config='--psm 9')
        text = str(tessout).strip()
        ### this prevents truly empty cells from being read as if they have content.  basically the OCR will find characters even if no pixels are black, so this manually tells the script there's nothing there if too few cells have black pixels.  this could miss blank cells and it could misfire on cells with actual content, though currently the test is only 10 pixels, and it'll have to be in the hundreds to blank out cells with actual content.
        #print(thresh1.shape[0] * thresh1.shape[1], np.sum(img[:,:,0]/255 < 0.5), np.sum(thresh1[:,:,0]/255 < 0.5), np.sum(thresh1[10:(thresh1.shape[0]-10),10:(thresh1.shape[1]-10),0]/255 < 0.5), text)
        if np.sum(thresh1[10:(thresh1.shape[0]-10),10:(thresh1.shape[1]-10),0]/255 < 0.5) < 10:
            text = ''
        row_content.append( text)
        if (i+1) % ncolumns == 0:
            ocrout.writerow(row_content)
            row_content = []
