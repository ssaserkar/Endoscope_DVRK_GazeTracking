import cv2
import numpy as np

'''
This code identifies the largest contour of the input image as we're hoping that the resultant image can be identified 
accurately. Accordingly we are modifying bounding box of the tissue segmentation result.

The box around the segmented image would look black as the image is relatively bright in nature. 
However, as the image from the endoscope is a little darker, we have made the bounding box as 'white'

As of now, this is an independent code, however, in the future, I am planning to embed this 
feature as part of the neural network of UNet++ itself. 
The combination of UNet++ and the Region of Interest work has not been done before and can be published once we run 
for sufficient epochs and some modifications of certain hyper-parameters.
'''

# Read in the images from the result,
image = cv2.imread("/path/to/image1")  # path to the groundtruth or the semantically segmented image
image_copy = cv2.imread("/path/to/image2")  # path to the original image from the endoscope

# Define the specific color you want to detect in RGB values
rgb_color = np.array([255, 160, 165])  # colour corresponding to - Gall Bladder, since we're dealing with  
# laparoscopic cholecystectomy. 

# convert the RGB values to Hue, Saturation and Vibrance Colour Space
hsv_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2HSV)

# Define a range of colors around the specific color in the HSV color space
color_lower = np.array([hsv_color[0] - 10, 100, 100])
color_upper = np.array([hsv_color[0] + 10, 255, 255])

# Create a mask for the image based on the defined color range
mask = cv2.inRange(image, color_lower, color_upper)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through the contours and draw a bounding box around the largest one
if contours:
    c = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 2)  # Black bounding box
    cv2.rectangle(image_copy, (x, y), (x + w, y + h), (255, 255, 255), 2)  # White bounding box

# Show the images
cv2.imshow("Image 1", image)
cv2.imshow("Image 2", image_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
