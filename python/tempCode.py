
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(image,contours,-1,(0,255,0),-1)

cnt = contours[0]






(x,y), radius = cv2.minEnclosingCircle(cnt)
center =( int(x), int(y) )
radius = int(radius)
cv2.circle(image, center, radius, (0,255,0),2)
#x,y,w, h = cv2.boundingRect(cnt)
#box = cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
#cv2.drawContours(image, [box], 0, (0,0,255), 2)


# Shows car well. 
cv2.imwrite("BoxContours" + imName, image)
cv2.imshow(" Box contour Output", image)
cv2.waitKey(0)


cv2.imshow("Output", image)

cv2.waitKey(0)




