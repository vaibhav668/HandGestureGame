import cv2
import mediapipe as mp
import pyautogui

mp_drawing=mp.solutions.drawing_utils
mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.5)
cap=cv2.VideoCapture(0)
def count_fingers(hand_landmarks,frame_w,frame_h):
     finger_tips=[8,12,16,20]
     thumb_tip=4
     count=0
     for tip in finger_tips:
          if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
               count+=1
               
     if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 2].x:
          count+=1
     return count

while True:
        ret,frame=cap.read()
        if not ret:
            break
        frame=cv2.flip(frame,1)
        h,w,c=frame.shape
        rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results=hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                fingers=count_fingers(hand_landmarks,w,h)
                if fingers>=4:
                     pyautogui.keyDown("right")
                     pyautogui.keyUp("left")
                     cv2.putText(frame,"Zoom Zoom! Vaibhav is flying!",(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

                elif fingers==0:
                     pyautogui.keyDown("left")
                     pyautogui.keyUp("right")
                     cv2.putText(frame,"Vaibhav...car is going to stop/reverse",(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                else:
                    pyautogui.keyUp("left")
                    pyautogui.keyUp("right")
                    cv2.putText(frame," Vaibhav’s car waiting for orders",(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

        
        small_frame = cv2.resize(frame, (800, 600))
        cv2.imshow("Gesture Camera", small_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
           break
cap.release()
cv2.destroyAllWindows()

