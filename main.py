import cv2
import mediapipe as mp
import math

mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
w_img = cap.set(3, 640)
h_img = cap.set(4, 480)

with mp_maos.Hands(max_num_hands=1) as maos:
    while cap.isOpened():
        sucess, frame = cap.read()
        if not sucess:
            print("Não foi possível acessar a câmera!")
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = maos.process(img_rgb)
        handLandmarks = result.multi_hand_landmarks

        # Mapeando os pontos da mão
        handPoints = []

        if handLandmarks:
            # Mapear cada ponto
            for points in handLandmarks:
                # Desenhar o esqueleto
                mp_desenho.draw_landmarks(frame, points, mp_maos.HAND_CONNECTIONS)  # Corrigido para desenhar no 'frame'
                # Loop para mapear as coordenadas dos pontos NO OBJ -> points  
                for id, coord in enumerate(points.landmark):  # Corrigido 'points.handLandmarks' para 'points.landmark'
                    h, w, _ = frame.shape
                    cx, cy = int(coord.x * w), int(coord.y * h)
                    handPoints.append([cx, cy])  

            if handPoints:
                polegar_distance = math.sqrt((handPoints[17][0] - handPoints[4][0]) ** 2 +
                                             (handPoints[17][1] - handPoints[4][1]) ** 2)

                indicador_distance = math.sqrt((handPoints[5][0] - handPoints[8][0]) ** 2 +
                                                (handPoints[5][1] - handPoints[8][1]) **2)

                medio_distance = math.sqrt((handPoints[9][0] - handPoints[12][0]) ** 2 +
                                           (handPoints[9][1] - handPoints[12][1]) ** 2)

                anelar_distance = math.sqrt((handPoints[13][0] - handPoints[16][0]) ** 2 +
                                            (handPoints[13][1] - handPoints[16][1]) ** 2)

                minimo_distance = math.sqrt((handPoints[20][0] - handPoints[17][0]) ** 2 +
                                            (handPoints[20][1] - handPoints[17][1]) ** 2)
                
                #pulso_distance = handPoints[0][2]
                #print(f'Distancia da mao: {pulso_distance}')
                
                #print(f'Polegar: {int(polegar_distance)}')
                #print(f'Indicador: {int(indicador_distance)}')
                #print(f'Medio:  {int(medio_distance)}')
                #print(f'                                  Anelar: {int(anelar_distance)}')
                #print(f'Minimo: {int(minimo_distance)}')
                
                #if polegar_distance > 100:
                    #print(f'Polegar   levantado       {(int(polegar_distance)}')
                #else:
                    #print(f'Polegar    abaixado       {int(polegar_distance)}')                    

                #if indicador_distance > 50:
                    #print(f'Indicador levantado       {int(indicador_distance)}')
                #else:
                    #print(f'Indicador  abaixado       {int(indicador_distance)}')
                
                #if indicador_distance > 55:
                    #print(f'Indicador  levantado       {int(indicador_distance)}')
                #else:
                    #print(f'Indicador   abaixado       {int(indicador_distance)}')
                
                #if medio_distance > 65:
                    #print(f'Medio       levantado      {medio_distance}')
                #else:
                    #print(f'Medio        abaixado      {medio_distance}')
                    
                    
                #PROXIMO -> ANALISAR A DISTANCIA DO ANELAR DISTANTE DA CAMERA E VER SEU VALOR FECHADO.#

        cv2.imshow('Mãos detectadas: ', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Liberando a captura de vídeo e fechando as janelas
cap.release()
cv2.destroyAllWindows()
