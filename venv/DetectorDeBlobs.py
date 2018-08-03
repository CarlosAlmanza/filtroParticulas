# -*- coding: utf-8 -*-

import numpy as np
import cv2
from math import *
from random import randint

class Blobs:

    def __init__(self):
        # Criação do detector de blob
        self.params = cv2.SimpleBlobDetector_Params()
        self.configuracao()

    def configuracao(self):
        # Change thresholds
        self.params.minThreshold = 0
        self.params.maxThreshold = 50

        # Filter by Area.
        self.params.filterByArea = True
        self.params.minArea = 150

        # Filter by Circularity
        self.params.filterByCircularity = False
        self.params.minCircularity = 0.4

        # Filter by Convexity
        self.params.filterByConvexity = True
        self.params.minConvexity = 0.4

        # Filter by Inertia
        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.03

        # Criando um detector com estes parametros
        ver = (cv2.__version__).split('.')
        if int(ver[0]) < 3:
            self.detector = cv2.SimpleBlobDetector(self.params)
        else:
            self.detector = cv2.SimpleBlobDetector_create(self.params)

    def detecte(self, frame):
        # Detecta os blobs na imagem
        self.keypoints = self.detector.detect(frame)
        return self.keypoints

    def centroDeMassa(self, blobs):
        # Calcula o centro de massa de cada blob e marca no frame
        x = 0
        y = 0
        for blob in blobs:
            x = blob.pt[0]
            y = blob.pt[1]
            s = blob.size

        x = int(round(x))
        y = int(round(y))

        return (y, x)