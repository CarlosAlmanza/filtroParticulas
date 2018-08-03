# -*- coding: utf-8 -*-

import numpy as np
import cv2
from math import *
from random import randint

import FiltroDeParticulas as F
import DetectorDeBlobs as D

larguraVideo = 800 # Largura da janela de exibição - coordenada x
alturaVideo = 500  # Altura da janela de exibição - coordenada y
pos_X_janela = 200 # Posição x da janela da exibição no monitor
pos_Y_janela = 100 # Posição y da janela da exibição no monitor
numPart = 500      # Numero de particulas que serão utilizadas

# Define a janela de exibição das imagens com tamanho original do video
nomeJanela = 'Janela de Exibicao'
cv2.namedWindow(nomeJanela, cv2.WINDOW_AUTOSIZE)

# Posiciona a janela nestas coordenadas do monitor
cv2.moveWindow(nomeJanela, pos_X_janela, pos_Y_janela)

#Criacao do filtro de particulas
filtroDeParticulas = F.Filtro()

#Criação do detector de blobs
DetectorDeBlobs = D.Blobs()

# Leitura do video
cap = cv2.VideoCapture('videoUmAlev.avi')

i = 0
time = 150

while(True):
    # Captura primeiro/mais_um frame e retorna um boolean, se há frame então ret recebe TRUE senão FALSE.
    ret, frame = cap.read()

    # Redimensionamento dos frames do video
    frame = cv2.resize(frame, (larguraVideo, alturaVideo))

    # Conversão do frame em tons de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Suavização do frame, VALORES: 31 foi definido aleatoriamente
    suave = cv2.GaussianBlur(gray, (31, 31), 0)

    # Binarização da imagem, VALORES: 45 e 255 foram definidos aleatoriamente
    (T, bin) = cv2.threshold(suave, 45, 255, cv2.THRESH_BINARY)

    # Detectar os blobs do frame binario
    blobs = DetectorDeBlobs.detecte(bin)

    # Marca os blobs na imagem original, cor verde
    frameComBlobs = cv2.drawKeypoints(frame, blobs, np.array([]), (0, 255, 0),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Captura as coordenadas do centro de massa de cada blob
    y_blob, x_blob= DetectorDeBlobs.centroDeMassa(blobs)
    #y_centroMassa, x_centroMassa = DetectorDeBlobs.centroDeMassa(blobs, frame)

    # Marca o centro de massa do blob, cor verde e quadrado 3x3
    frameComBlobs[y_blob:y_blob+3, x_blob:x_blob+3] = (0, 255, 0)

    # INICIO DO RASTREAMENTO, RASTREIA APENAS SE HÁ BLOBS/PEIXE
    if blobs != []:
        # Controle para inicializar as particulas apenas uma vez
        if i == 0:
            filtroDeParticulas.inicializacao(y_blob, x_blob, numPart)
            i = 1

        filtroDeParticulas.predicao()

        filtroDeParticulas.atualizaPesos(y_blob, x_blob)

        filtroDeParticulas.correcao()

        # Captura as coordenadas do centro de massa da media ponderada das particulas
        y_medioParts, x_medioParts = filtroDeParticulas.centroDeMassa()

        # Marca o centro de massa calculado pelo filtro de particulas, cor branca
        # frame[y:y+3, x:x+3] = (255, 255, 255)
        frameComBlobs[y_medioParts:y_medioParts + 3, x_medioParts:x_medioParts + 3] = (255, 255, 255)

        # Desenhando as particulas no frame
        particulas = filtroDeParticulas.getParticulas()
        for j in range(len(particulas)):
            xPart = particulas[j].getX()
            yPart = particulas[j].getY()
            # Particulas que ultrapassam os limites da janela de exibição não são marcadas no frame
            if xPart > 0 and xPart < larguraVideo and yPart > 0 and yPart < alturaVideo:
                frameComBlobs[yPart, xPart] = (255, 0, 0)
                #frame[y, x] = (255, 0, 0)

    # Exibindo o frame
    cv2.imshow(nomeJanela, frameComBlobs)
    #cv2.imshow(nomeJanela, frame)

    # Velocidade do video e tecla de parada de execusão
    if cv2.waitKey(time) & 0xFF == ord('q'):
        if time == 0:
            break
        time = 0
        #break

# Acabou os frames ou deu erro, pare a captura.
cap.release()
cv2.destroyAllWindows()