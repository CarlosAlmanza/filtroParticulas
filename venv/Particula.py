# -*- coding: utf-8 -*-

class Particula:

    def __init__(self, coordY, coordX, peso):
        self.x = coordX
        self.y = coordY
        self.w = peso

    def setX(self, coordX):
        self.x = coordX

    def setY(self, coordY):
        self.y = coordY

    def setPeso(self, peso):
        self.w = peso

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPeso(self):
        return self.w
