import cv2
import mediapipe as mp
import math
from send_sinals.pt import abrir_fechar

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

        handPoints = []

        if handLandmarks:
            for points in handLandmarks:
                mp_desenho.draw_landmarks(frame, points, mp_maos.HAND_CONNECTIONS)
                for id, coord in enumerate(points.landmark):
                    h, w, _ = frame.shape
                    cx, cy = int(coord.x * w), int(coord.y * h)
                    handPoints.append([cx, cy])

            if handPoints:
                polegar_distance = math.sqrt((handPoints[17][0] - handPoints[4][0]) ** 2 +
                                            (handPoints[17][1] - handPoints[4][1]) ** 2)

                indicador_distance = math.sqrt((handPoints[5][0] - handPoints[8][0]) ** 2 +
                                                (handPoints[5][1] - handPoints[8][1]) ** 2)

                medio_distance = math.sqrt((handPoints[9][0] - handPoints[12][0]) ** 2 +
                                            (handPoints[9][1] - handPoints[12][1]) ** 2)

                anelar_distance = math.sqrt((handPoints[13][0] - handPoints[16][0]) ** 2 +
                                            (handPoints[13][1] - handPoints[16][1]) ** 2)

                minimo_distance = math.sqrt((handPoints[20][0] - handPoints[17][0]) ** 2 +
                                            (handPoints[20][1] - handPoints[17][1]) ** 2)

                if polegar_distance > 135:
                    abrir_fechar(12, 1)
                else:
                    abrir_fechar(12, 0)

                if indicador_distance > 70:
                    abrir_fechar(11, 1)
                else:
                    abrir_fechar(11, 0)

                if medio_distance > 82:
                    abrir_fechar(10, 1)
                else:
                    abrir_fechar(10, 0)

                if anelar_distance > 85:
                    abrir_fechar(9, 1)
                else:
                    abrir_fechar(9, 0)

                if minimo_distance > 65:
                    abrir_fechar(8, 1)
                else:
                    abrir_fechar(8, 0)

        cv2.imshow('Mãos detectadas: ', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Liberando a captura de vídeo e fechando as janelas
cap.release()
cv2.destroyAllWindows()
