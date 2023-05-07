# * exemplo 12 do site:
# <https://www.programcreek.com/python/example/81596/cv2.compareHist>
# * tutorial do openCV:
# <https://docs.opencv.org/3.4/dc/df6/tutorial_py_histogram_backprojection.html>
import glob
import numpy as np
import cv2 as cv
from os import path


for objeto in glob.glob('./objetos/*.png'):
    roi = cv.imread(objeto)
    oname = path.basename(objeto).split('.')[0]
    if roi is None:
        print(f'Falha lendo imagem do objeto \'{objeto}\'')
        continue
    # pegar cor hsv
    #hsv_objeto = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
    # pegar histograma do objeto
    hist_objeto = cv.calcHist(
        [roi], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 200]
    )
    # normalizar histograma do objeto
    cv.normalize(hist_objeto, hist_objeto, 0, 255, cv.NORM_MINMAX)

    # para cada imagem efetuar a busca
    for imagem in glob.glob('./imagens/*.jpg'):
        tname = path.basename(imagem).split('.')[0]

        print(f'> Busca \'{oname}\' em \'{tname}\'')

        alvo = cv.imread(imagem)
        if alvo is None:
            print(f'Falha lendo imagem \'{imagem}\'')
            continue
        #hsv_alvo = cv.cvtColor(alvo, cv.COLOR_BGR2HSV)

        # essa funcao utiliza o calcHist com o algoritmo de swain e ballard
        dst = cv.calcBackProject(
            [alvo], [0, 1, 2], hist_objeto, [0, 256, 0, 256, 0, 200], 0.81
        )

        # o resto eh para remover o que nao faz parte do objeto encontrado
        disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        cv.filter2D(dst, -1, disc, dst)
        ret, thresh = cv.threshold(dst, 30, 255, 0)
        thresh = cv.merge((thresh, thresh, thresh))
        res = cv.bitwise_and(alvo, thresh)
        res = np.vstack((alvo, thresh, res))
        print(f'>> Salvando em: ./resultados/{oname}with{tname}.jpg')
        cv.imwrite(f'./resultados/{oname}with{tname}.jpg', res)
