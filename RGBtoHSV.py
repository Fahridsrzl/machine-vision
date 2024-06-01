import cv2
import numpy as np

# Baca gambar RGB sebagai format BGR
bgr_img = cv2.imread(r'C:\Users\Fahmi\OneDrive\Documents\Raspi\Documents\Penelitian\Gambar\Kamera1\Ori\09-Aug-2023(13;06 WIB).jpg')
# Ubah gambar BGR menjadi gambar HSV
hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

lower = np.array([17, 5, 151])
upper = np.array([52, 130, 243]) 
mask = cv2.inRange(hsv_img,lower,upper)
kernel = np.ones((1, 1), np.uint8) #untuk operasi blur, erosi, dilasi
erosion = cv2.erode(mask, kernel, iterations=1) #operasierosi
dilation = cv2.dilate(erosion, kernel, iterations=1) #operasidilasi
bitwise = cv2.bitwise_and(bgr_img, bgr_img, mask=dilation) #bitwise(n)

# Simpan gambar dengan nama file yang diinginkan
cv2.imwrite('threshold.jpg', hsv_img)
