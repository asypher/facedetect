annotations_dic = \
  {"lipsUpperOuter": [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291,78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308],
  "lipsLowerOuter": [146, 91, 181, 84, 17, 314, 405, 321, 375, 291,78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308],
  "lipsUpperInner": [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308],
  "lipsLowerInner": [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308],

  "rightEyeUpper0": [246, 161, 160, 159, 158, 157, 173],
  "rightEyeLower0": [33, 7, 163, 144, 145, 153, 154, 155, 133],
  "rightEyeUpper1": [247, 30, 29, 27, 28, 56, 190],
  "rightEyeLower1": [130, 25, 110, 24, 23, 22, 26, 112, 243],
  "rightEyeUpper2": [113, 225, 224, 223, 222, 221, 189],
  "rightEyeLower2": [113, 225, 224, 223, 222, 221, 189,226, 31, 228, 229, 230, 231, 232, 233, 244],
  "rightEyeLower3": [143, 111, 117, 118, 119, 120, 121, 128, 245],

  "rightEyebrowUpper": [35, 124, 46, 53, 52, 65,156, 70, 63, 105, 66, 107, 55, 193],
  "rightEyebrowLower": [35, 124, 46, 53, 52, 65],

  "leftEyeUpper0": [466, 388, 387, 386, 385, 384, 398],
  "leftEyeLower0": [263, 249, 390, 373, 374, 380, 381, 382, 362],
  "leftEyeUpper1": [467, 260, 259, 257, 258, 286, 414],
  "leftEyeLower1": [359, 255, 339, 254, 253, 252, 256, 341, 463],
  "leftEyeUpper2": [342, 445, 444, 443, 442, 441, 413],
  "leftEyeLower2": [446, 261, 448, 449, 450, 451, 452, 453, 464],
  "leftEyeLower3": [372, 340, 346, 347, 348, 349, 350, 357, 465],

  "leftEyebrowUpper": [383, 300, 293, 334, 296, 336, 285, 417,265, 353, 276, 283, 282, 295],
  "leftEyebrowLower": [265, 353, 276, 283, 282, 295],

  "midwayBetweenEyes": [168],

  "noseTip": [1],
  "noseBottom": [2],
  "noseRightCorner": [98],
  "noseLeftCorner": [327],

  "rightCheek": [50,101,36,206,207,187],
   #[117,118,101,36,205,187,137,234,117]
  "leftCheek": [330,266,426,427,411,280]
}

from .custompoly import customfillpoly
import cv2
import numpy as np
# import matplotlib.pyplot as plt
# from blendtest import *

def sort_poly_fill_list(chk):
  for i in range(len(chk)-1):
    if(chk[i+1][0] < chk[i][0]):
      break
  chkfirst  = chk[:i+1]
  chksecond = sorted(chk[i+1:],key=lambda k: [k[0], k[1]],reverse= True)
  print(chkfirst,chksecond)
  chkfirst.extend(chksecond)
  return chkfirst

def fill_part(image, keypoints, part,setcolor):
  temp = []
  for index in annotations_dic[part]:
    # print(index)
    temp.append((int(keypoints[index]['X']), int(keypoints[index]['Y'])))
    # temp.append(face_landmarks)
  # print(temp)
  if part == "leftCheek" or "rightCheek":
    mask = np.zeros((image.shape[0],image.shape[1],3))
    # chkfirst = sort_poly_fill_list(chk)
    temp = sort_poly_fill_list(temp)
    # cv2.fillPoly(image, np.int32([temp]), setcolor, lineType=cv2.LINE_AA)
    mask = cv2.fillPoly(mask, np.int32([temp]), (255, 255, 255), lineType=cv2.LINE_AA)
    image = do_blending(image,setcolor,mask)
    cv2.imshow("region mask"+str(part),mask)
    cv2.imwrite("mask"+str(part)+".png",mask)
  else:
    mask = np.zeros((image.shape[0],image.shape[1],3))
    # chkfirst = sort_poly_fill_list(chk)
    temp = sort_poly_fill_list(temp)
    cv2.fillPoly(image, np.int32([temp]), setcolor, lineType=cv2.LINE_AA)
    mask = cv2.fillPoly(mask, np.int32([temp]), (255, 255, 255), lineType=cv2.LINE_AA)
    # image = do_blending(image,setcolor,mask)
    cv2.imshow("region mask"+str(part),mask)
    cv2.imwrite("mask"+str(part)+".png",mask)


    # image = custompolyfill(image,temp)
  # plt.fill(temp[0], temp[1], 'k', alpha=0.3)
  #
  # with open(part+'.txt', 'w') as f:
  #   for item in temp:
  #     f.write("%s\n" % str(item))

  return image
#
# chk = [(206, 325),
# (212, 337),
# (221, 348),
# (234, 355),
# (250, 358),
# (266, 355),
# (278, 347),
# (287, 335),
# (292, 323),
# (296, 311),
# (209, 314),
# (215, 326),
# (220, 332),
# (228, 338),
# (237, 342),
# (250, 344),
# (262, 342),
# (272, 337),
# (279, 330),
# (283, 324),
# (289, 312),
# ]
#
# mask = np.zeros((400,400))
# chkfirst = sort_poly_fill_list(chk)
# mask = cv2.fillPoly(mask, np.int32([chkfirst]), (255, 255, 255))
# # mask = customfillpoly(mask,chk)
#
# mask2 = np.zeros((400,400))
# for x,y in chk:
#   cv2.circle(mask2,(x,y),1,255,1)
#
# cv2.imshow("mask1",mask)
# cv2.imshow("mask2",mask2)