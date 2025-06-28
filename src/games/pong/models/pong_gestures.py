import cv2
import mediapipe as mp

gesture_move = 0
hand_y_position_scaled = 0
received_data = None

# Rozmiar pionowy obszaru gry, zdefiniowany przez grę
GAME_HEIGHT = 600


def pong_start_gesture_recognition():
    global gesture_move, hand_y_position_scaled, received_data

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.7) as hands:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Nie można odczytać obrazu z kamery")
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            frame_height, frame_width, _ = frame.shape

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    wrist = hand_landmarks.landmark[9]
                    hand_y_pixel = int(wrist.y * frame_height)

                    # Skalujemy do zakresu gry (0-600)
                    hand_y_position_scaled = int((hand_y_pixel / frame_height) * GAME_HEIGHT)
                    
                    # print(hand_y_position_scaled)

                    # Pobieramy pozycję paletki
                    if received_data:
                        player_id = received_data.get('playerId')
                        state = received_data.get('state', {})

                        paddle_y = state.get('leftPaddleY') if player_id == 0 else state.get('rightPaddleY')
                        
                        max_delta=30

                        if paddle_y is not None:
                            delta = hand_y_position_scaled - paddle_y

                            if delta < -max_delta:
                                gesture_move = 1
                            elif delta > max_delta:
                                gesture_move = -1
                            else:
                                gesture_move = 0
                                
                            print(gesture_move)

            cv2.imshow('Hand Tracking', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


def get_pong_move_from_gesture(data):
    global received_data
    received_data = data
    return gesture_move
