''' Cortes Martinez Dilan
    5BV1
    Vision Artificial
    Segunda Evaluacion Practica'''
from re import I
import cv2
import numpy as np
import math

'''Declaracion de Funciones'''
def Redimencionar(imagen, scala): #Reescalamos la imagen original con el fin de trabajar de manera mas optima
    filas, columnas = imagen.shape[:2] 
    dsize = (int(filas * scala / 100), int(columnas* scala / 100))
    imagen_redimensionada = cv2.resize(imagen, dsize)
    return imagen_redimensionada
def conversion_HSV(img):  #Realizamos una conversion de modelo de color RGB -> HSV
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  hsv[...,2] = 255
  print("Imagen convertida a HSV y modificada en color:")
  cv2.imshow(hsv)
  return hsv

def conversion_RGB(hsv):  #Revertimos la conversion de modelo de color HSV -> RGB
  img2 = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
  im_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
  print("Imagen convertida a RGB desde HSV:")
  cv2.imshow(im_rgb)
  return img2

def umbral_gris(img): #Aplicamos una umbralizacion para generar una mascara
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  ret, thresh = cv2.threshold(gray, 127, 255, 0)
  print("Imagen umbralizada:")
  cv2.imshow(thresh)

  print('\n')
  return thresh

def busca_contornos(thresh):  #Con la mascara, determinamos las cooerdanas donde se encuentran los bordes de los objetos (jitomates)
  
  contours, _ = cv2.findContours(thresh, cv2.RETR_TREE,
                               cv2.CHAIN_APPROX_SIMPLE)
  longest = 0
  sec_lon = 0
  thi_lon = 0
  fou_lon = 0
  fiv_lon = 0

  for i in range(0,len(contours)):
    if(len(contours[i]) > longest):
      longest = len(contours[i])
      index_longest = i
    else:
      if(len(contours[i]) > sec_lon):
        sec_lon = len(contours[i])
        dos_index_longest = i
      else:
        if(len(contours[i]) > thi_lon):
          thi_lon = len(contours[i])
          tre_index_longest = i
        else:
          if(len(contours[i]) > fou_lon):
            fou_lon = len(contours[i])
            cua_index_longest = i
          else:
            if(len(contours[i]) > fiv_lon):
              fiv_lon = len(contours[i])
              cin_index_longest = i

  Contorno_1 = contours[index_longest]
  x, y, w, h = cv2.boundingRect(Contorno_1)

  Contorno_2 = contours[dos_index_longest]
  x2, y2, w2, h2 = cv2.boundingRect(Contorno_2)

  Contorno_3 = contours[tre_index_longest]
  x3, y3, w3, h3 = cv2.boundingRect(Contorno_3)

  Contorno_4 = contours[72]
  x4, y4, w4, h4 = cv2.boundingRect(Contorno_4)

  return Contorno_1, Contorno_2, Contorno_3, Contorno_4

def dibuja_lineas(Contorno, No_objeto, Imagen): #Ya con los bordes, determinamos el punto de interes junto con su contraparte y trazamos una linea recta

  Recta = cv2.minAreaRect(Contorno)
  caja = cv2.boxPoints(Recta)
  caja = np.int0(caja)

  print("Coordenadas de el objeto ", No_objeto)

  for i in range(0, len(caja)):
    print(caja[i])
  print("\n")

  x_1 = (caja[0][0] + caja[3][0])/2
  x_1 = int(x_1)
  print("Coordenada en X1 del segmento del objeto ",x_1)

  y_1 = (caja[0][1] + caja[3][1])/2
  y_1 = int(y_1)
  print("Coordenada en Y1 del segmento del objeto ",y_1)

  x_2 = (caja[1][0] + caja[2][0])/2
  x_2 = int(x_2)
  print("Coordenada en X2 del segmento del objeto ",x_2)

  y_2 = (caja[1][1] + caja[2][1])/2
  y_2 = int(y_2)
  print("Coordenada en Y2 del segmento del objeto ",y_2)

  punto_de_inicio = (x_1, y_1)
  punto_de_fin = (x_2, y_2)
  image = cv2.line(Imagen, punto_de_inicio, punto_de_fin, (255, 0, 255), 2 )
  distance1 = math.sqrt((x_2 - x_1)**2+(y_2 - x_1)**2)
  print("El segmento 1 que corta al objeto tiene como longitud ",distance1)
  print("\n")
  return

Imagen_original = cv2.imread("/content/Jit1.JPG", cv2.IMREAD_COLOR) #Cargamos la imagen al programa
Imagen_redimencionada = Redimencionar(Imagen_original, 30)  #Realizamos un reescalamiento al 30%
cv2.imshow(Imagen_redimencionada)
Image_hsv = conversion_HSV(Imagen_redimencionada) # Realizamos una conversion a HSV y aislamos el color de los objetos de interes
Image_RGB = conversion_RGB(Image_hsv) #Regresamos la imagen al modelo RGB
Image_gris = umbral_gris(Image_RGB) #Realizamos una conversion a escala de gris y generamos la mascara por medio de una umbralizacion
Contorno_1, Contorno_2, Contorno_3, Contorno_4 = busca_contornos(Image_gris)  #Buscamos los contornos de los 4 objetos, los dos m??s grandes se almacenan en los objetos 1 y 2
dibuja_lineas(Contorno_1, 4, Imagen_redimencionada) #Buscamos el punto de interes y trazamos la primer linea 
dibuja_lineas(Contorno_2, 2, Imagen_redimencionada) #Buscamos la segunda linea de interes y trazamos la segunda linea
cv2.imshow(Imagen_redimencionada) #Mostramos la imagen ya modificada con las lineas tazadas