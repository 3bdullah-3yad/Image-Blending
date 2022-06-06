import cv2

def show(image):
    cv2.imshow("", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img1 = cv2.imread(r"D:\Projects\Computer Vision\Image Blending\1.jpg")
img2 = cv2.imread(r"D:\Projects\Computer Vision\Image Blending\2.jpg")
img1.shape # (492, 750, 3)
img2.shape # (500, 750, 3)
img2 = cv2.resize(img2, (750, 492))
img1.shape == img2.shape # True
show(img1)
show(img2)


# Gaussian pyramid for the first image
im1 = img1.copy()
pyr1 = [im1]
for i in range(4):
    pyr1.append(cv2.pyrDown(pyr1[-1]))
show(pyr1[3])


# Gaussian pyramid for the second image
im2 = img2.copy()
pyr2 = [im2]
for i in range(4):
    pyr2.append(cv2.pyrDown(pyr2[-1]))
show(pyr2[3])


# Difference of Gaussian for pyr1
laps1 = [pyr1[-1]]
for i in range(4, 0, -1):
    rows, cols, _ = pyr1[i-1].shape
    lap = cv2.subtract(pyr1[i-1], cv2.pyrUp(pyr1[i], dstsize=(cols, rows)))
    laps1.append(lap)
show(laps1[4])


# Difference of Gaussian for pyr2
laps2 = [pyr2[-1]]
for i in range(4, 0, -1):
    rows, cols, _ = pyr2[i-1].shape
    lap = cv2.subtract(pyr2[i-1], cv2.pyrUp(pyr2[i], dstsize=(cols, rows)))
    laps2.append(lap)
show(laps2[4])



import numpy as np

# Image Blending
blended_imgs = []
for pic1, pic2 in zip(laps1, laps2):
    rows, cols, _ = pic1.shape
    stacked_img = np.hstack((pic1[:, 0:cols//2], pic2[:, cols//2:]))
    blended_imgs.append(stacked_img)
    

final_img = blended_imgs[0]
for i in range(1, 5):
    rows, cols, _ = blended_imgs[i].shape
    final_img = cv2.pyrUp(final_img, dstsize=(cols, rows))
    final_img = cv2.add(blended_imgs[i], final_img)
    

show(final_img)
cv2.imwrite(r"D:\Projects\Computer Vision\Image Blending\Blended.jpg",
            final_img)    
    