import cv2  
import numpy as np
import matplotlib.pyplot as plt

from settings import Settings


cv2.imwrite('a.jpg', np.array([[0, 255], [255, 0]]))