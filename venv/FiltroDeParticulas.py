# -*- coding: utf-8 -*-

import numpy
from math import *
from random import randint

import Particula as P


class Filtro:

    def __init__(self):
        self.particulas = []

    def inicializacao(self, y_cMassa, x_cMassa, numPart):
        # Criacao das particulas, distanciam entre -15 e 15 do centro de massa do objeto, peso inicial = 20
        for x in range(numPart):
            part = P.Particula(y_cMassa + randint(-15, 15), x_cMassa + randint(-15, 15), 20)
            self.particulas.append(part)

    def getParticulas(self):
        return self.particulas

    # Como colocar um ruido gaussiano sendo que as coordenadas precisam ser decimais sem ponto flutuante
    def predicao(self):
        for i in range(len(self.particulas)):
            x = self.particulas[i].getX() + randint(-30, 0)  # + numpy.random.normal(0, 1)
            self.particulas[i].setX(x)

            y = self.particulas[i].getY() + randint(-25, 25)  # + numpy.random.normal(0, 1)
            self.particulas[i].setY(y)

    def atualizaPesos(self, y_cMassa, x_cMassa):
        # Calcula a distancia entre dois pontos, distancia entre particula e centro do objeto
        for i in range(len(self.particulas)):
            dist = sqrt((self.particulas[i].getX() - x_cMassa) ** 2 + (self.particulas[i].getY() - y_cMassa) ** 2)
            self.particulas[i].setPeso(dist)

    def correcao(self):
        particulas = []

        # Captura apenas as particulas que serão usadas na proxima iteração, devem ter peso menor que 40
        for i in range(len(self.particulas)):
            if self.particulas[i].getPeso() > 0 and self.particulas[i].getPeso() < 40:
                particulas.append(self.particulas[i])

        # Numero de particulas que serão criadas para manter o quantidade original
        numReposicoes = len(self.particulas) - len(particulas)
        self.particulas = particulas

        # Procura a particula mais proxima do objeto alvo
        maisProx = self.particulas[0]
        for i in range(len(self.particulas)):
            if self.particulas[i].getPeso() < maisProx.getPeso():
                maisProx = self.particulas[i]

        # Cria particulas a partir da particula mais proxima do objeto alvo,
        # distanciam entre -15 e 15 da particula mais proxima do objeto alvo, peso inicial = 20
        for i in range(numReposicoes):
            part = P.Particula(maisProx.getY() + randint(-15, 15), maisProx.getX() + randint(-15, 15), 20)
            self.particulas.append(part)

        # Iguala o peso de todas as particulas
        for i in range(len(self.particulas)):
            self.particulas[i].setPeso(20)

    def centroDeMassa(self):
        # Cacula a media ponderada de todas as particulas
        somaPesos = 0
        xNumerador = 0
        yNumerador = 0
        for i in range(len(self.particulas)):
            xNumerador = xNumerador + (self.particulas[i].getPeso() * self.particulas[i].getX())
            yNumerador = yNumerador + (self.particulas[i].getPeso() * self.particulas[i].getY())
            somaPesos = somaPesos + self.particulas[i].getPeso()

        x = xNumerador / somaPesos
        y = yNumerador / somaPesos
        return (int(round(y)), int(round(x)))