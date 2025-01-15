import cv2
import mediapipe as mp

space = 0
up = 0
down = 0

def skijump_start_gesture_recognition():
    global space
    global up
    global down

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.7) as hands:
        previous_y = None

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

                    # Sprawdzenie gestu "zaciśniętej pięści"
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]

                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

                    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

                    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]

                    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

                    # Gest pięści: wszystkie końcówki palców blisko ich MCP
                    if (
                            # abs(thumb_tip.y - thumb_mcp.y) < 0.1 and
                            abs(index_tip.y - index_mcp.y) < 0.1 and
                            abs(middle_tip.y - middle_mcp.y) < 0.1 and
                            abs(ring_tip.y - ring_mcp.y) < 0.1 and
                            abs(pinky_tip.y - pinky_mcp.y) < 0.1
                    ):
                        space = 1
                    else:
                        space = 0
                        
                    print(space)

                    # Wykrywanie ruchów w górę i w dół
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    current_y = wrist.y

                    if previous_y is not None:
                        if current_y < previous_y - 0.02:
                            down = 1
                            up = 0
                        elif current_y > previous_y + 0.02:
                            down = 0
                            up = 1
                        else:
                            up = 0
                            down = 0

                    previous_y = current_y

            cv2.imshow('Hand Tracking', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

def get_skijump_move_from_gesture():
    return space, up, down
