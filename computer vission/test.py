#import necessary librares
import cv2 
import mediapipe as mp 
class handtracker:
    def __init__(self):
        self.mp_hands=mp.solutions.hands
        self.hands = self.mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=3 
        min_detection_confidence =0.6
        min_tracking_confidence=0.6
        ) 
        self.mp_draw=mp.solution.drawing_utils
        def find_hands(self,imag):
            img_rgb=cv2.cvtcolor(img, cv2.COLOR_BGR2RGB)
            self.result=self.hands.process(img_rgb)
        if self.result.multi_hands_landmarks:
            for hands_landmarks in self.results.multi_hand_landmark
                self.mp_draw.draw_landmarks(
                    imag,
                    hand_landmarks,_
                    self.mp_hands.HAND_CONNECTIONS
                    )
                return None
            def main():
                cp=cv2. videocapture(0)
                tracker=  HandTracker()
        last_x=None
        movement_buffer=[]
wave                
                