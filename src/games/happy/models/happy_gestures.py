import cv2
import mediapipe as mp

gesture_move = 0

def happy_start_gesture_recognition():
    global gesture_move

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.7) as hands:
        previous_x = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Nie można odczytać obrazu z kamery")
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    wrist = hand_landmarks.landmark[0]  # Nadgarstek
                    current_x = wrist.x

                    if previous_x is not None:
                        if current_x < previous_x - 0.02:  # Ruch w lewo
                            gesture_move = 1
                        elif current_x > previous_x + 0.02:  # Ruch w prawo
                            gesture_move = -1
                        else:  # Brak ruchu
                            gesture_move = 0

                    previous_x = current_x

            cv2.imshow('Hand Tracking', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

def get_happy_move_from_gesture():
    return gesture_move
