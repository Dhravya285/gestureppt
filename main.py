import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import math
import time
import os
import warnings
from PIL import ImageGrab
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import A4

# Suppress Protobuf warning
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")

# ------------------ Setup ------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.4, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Set display resolution for canvas and slide
display_w, display_h = 1280, 720
canvas = np.ones((display_h, display_w, 3), np.uint8) * 255  # White canvas

# Get screen resolution for cursor control
screen = ImageGrab.grab()
screen_w, screen_h = screen.size

# Brush settings
brush_color = (0, 255, 0)
brush_thickness = 10
eraser_thickness = 50
colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 255)]
color_index = 0

prev_x, prev_y = 0, 0
snapshots = []
cursor_positions = []  # For smoothing
finger_counts = []  # For smoothing finger detection
current_slide_index = 0
last_fingers_up = -1
last_hand_time = time.time()
is_drawing_in_ppt = False  # Track PPT drawing state
last_navigation_time = 0  # For debouncing slide navigation

# Shape Drawing
shape_mode = False
draw_circle = False
start_point = None

# Cursor control
cursor_mode = False

# Create output folder
if not os.path.exists("output"):
    os.makedirs("output")
    print("Created output folder")

print("🎨 PPT Annotation + Cursor Control Instructions:")
print("1 Finger → Draw (Shape in shape mode) or Move Cursor/Draw in PPT (Cursor mode)")
print("2 Fingers → Erase (Canvas mode) or Click (Cursor mode) | 3 Fingers → Next Slide")
print("4 Fingers → Previous Slide / Change Color | 5 Fingers → Clear Canvas")
print("Press M → Toggle Shape Mode | Press C → Switch Rectangle/Circle")
print("Press R → Toggle Cursor Mode | Press T → Test Draw | S → Save Slide | P → Export PDF | Q → Quit")
print("Note: Manually focus PowerPoint in Slide Show mode (press F5) for slide navigation and annotations.")

# ------------------ PDF Saving Function ------------------
def save_as_pdf(image_files, output_file):
    c = pdf_canvas.Canvas(output_file, pagesize=A4)
    for img_path in image_files:
        c.drawImage(img_path, 0, 0, width=595, height=842)
        c.showPage()
    c.save()

# ------------------ Smooth Finger Count ------------------
def get_smoothed_fingers(fingers_up):
    finger_counts.append(fingers_up)
    if len(finger_counts) > 4:  # Stable detection
        finger_counts.pop(0)
    return max(set(finger_counts), key=finger_counts.count)

# ------------------ Main Loop ------------------
print("Starting program... Please manually focus PowerPoint and press F5 to enter Slide Show mode.")
time.sleep(3)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture video frame")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Mediapipe processing
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    fingers_up = 0
    x_tip, y_tip = 0, 0
    temp_canvas = canvas.copy()

    if result.multi_hand_landmarks:
        last_hand_time = time.time()
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]
            tip_ids = [4, 8, 12, 16, 20]
            fingers = []
            fingers.append(1 if landmarks[tip_ids[0]][0] > landmarks[tip_ids[0] - 1][0] else 0)
            for i in range(1, 5):
                fingers.append(1 if landmarks[tip_ids[i]][1] < landmarks[tip_ids[i] - 2][1] else 0)

            fingers_up = fingers.count(1)
            fingers_up = get_smoothed_fingers(fingers_up)
            x_tip, y_tip = landmarks[8]

            # Convert to display and screen coordinates
            screen_x = int(x_tip * (display_w / w))
            screen_y = int(y_tip * (display_h / h))
            screen_x = max(0, min(screen_x, display_w - 1))
            screen_y = max(0, min(screen_y, display_h - 1))

            cursor_x = int(x_tip * (screen_w / w))
            cursor_y = int(y_tip * (screen_h / h))
            cursor_x = max(10, min(cursor_x, screen_w - 10))
            cursor_y = max(10, min(cursor_y, screen_h - 10))

            # Smooth cursor movement
            cursor_positions.append((cursor_x, cursor_y))
            if len(cursor_positions) > 5:
                cursor_positions.pop(0)
            if cursor_positions:
                avg_cursor_x = int(sum(x for x, _ in cursor_positions) / len(cursor_positions))
                avg_cursor_y = int(sum(y for _, y in cursor_positions) / len(cursor_positions))
            else:
                avg_cursor_x, avg_cursor_y = cursor_x, cursor_y

            # Dynamic Brush Size
            distance = math.hypot(landmarks[4][0] - x_tip, landmarks[4][1] - y_tip)
            brush_thickness = int(np.interp(distance, [20, 200], [5, 50]))

            # Draw cursor point
            cv2.circle(temp_canvas, (screen_x, screen_y), 5, (255, 0, 0), -1)

            # Debug output
            if fingers_up != last_fingers_up:
                print(f"Fingers up: {fingers_up}, Draw coords: ({screen_x}, {screen_y}), Cursor coords: ({avg_cursor_x}, {avg_cursor_y})")
                last_fingers_up = fingers_up

            # ------------------ Gesture Modes ------------------
            if fingers_up == 1:
                if cursor_mode:
                    if not is_drawing_in_ppt:
                        print("Activating PowerPoint pen tool (ensure PowerPoint is focused in Slide Show mode)")
                        pyautogui.hotkey("ctrl", "p")
                        is_drawing_in_ppt = True
                    print(f"Moving cursor to ({avg_cursor_x}, {avg_cursor_y})")
                    pyautogui.moveTo(avg_cursor_x, avg_cursor_y)
                    if not pyautogui.mouseDown():
                        print("Starting mouse drag")
                        pyautogui.mouseDown()
                elif shape_mode:
                    if start_point is None:
                        start_point = (screen_x, screen_y)
                        print(f"Shape started at ({screen_x}, {screen_y})")
                        cv2.circle(temp_canvas, start_point, 15, (0, 255, 255), -1)  # Larger start point
                    else:
                        print(f"Previewing shape to ({screen_x}, {screen_y})")
                        if draw_circle:
                            radius = int(math.hypot(screen_x - start_point[0], screen_y - start_point[1]))
                            cv2.circle(temp_canvas, start_point, radius, brush_color, brush_thickness)
                        else:
                            cv2.rectangle(temp_canvas, start_point, (screen_x, screen_y), brush_color, brush_thickness)
                else:
                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = screen_x, screen_y
                    cv2.line(canvas, (prev_x, prev_y), (screen_x, screen_y), brush_color, brush_thickness)
                    prev_x, prev_y = screen_x, screen_y
            elif fingers_up == 0 and shape_mode and start_point is not None:
                print(f"Finalizing shape at ({screen_x}, {screen_y})")
                if draw_circle:
                    radius = int(math.hypot(screen_x - start_point[0], screen_y - start_point[1]))
                    if radius > 20:
                        cv2.circle(canvas, start_point, radius, brush_color, brush_thickness)
                        print(f"Circle drawn with radius {radius}")
                else:
                    if abs(screen_x - start_point[0]) > 20 and abs(screen_y - start_point[1]) > 20:
                        cv2.rectangle(canvas, start_point, (screen_x, screen_y), brush_color, brush_thickness)
                        print(f"Rectangle drawn from {start_point} to ({screen_x}, {screen_y})")
                start_point = None
            elif fingers_up == 2 and not cursor_mode:
                cv2.circle(canvas, (screen_x, screen_y), eraser_thickness, (255, 255, 255), -1)
                prev_x, prev_y = 0, 0
                start_point = None
            elif fingers_up == 2 and cursor_mode:
                print("Performing mouse click (ensure PowerPoint is focused)")
                pyautogui.click(avg_cursor_x, avg_cursor_y)
                time.sleep(0.5)
                prev_x, prev_y = 0, 0
                start_point = None
            elif fingers_up == 3 and time.time() - last_navigation_time > 1.5:
                print("Next slide (ensure PowerPoint is focused in Slide Show mode)")
                pyautogui.press("right")
                current_slide_index += 1
                last_navigation_time = time.time()
                prev_x, prev_y = 0, 0
                start_point = None
            elif fingers_up == 4 and time.time() - last_navigation_time > 1.5:
                color_index = (color_index + 1) % len(colors)
                brush_color = colors[color_index]
                print("Previous slide, new color:", brush_color, "(ensure PowerPoint is focused in Slide Show mode)")
                pyautogui.press("left")
                current_slide_index = max(0, current_slide_index - 1)
                last_navigation_time = time.time()
                prev_x, prev_y = 0, 0
                start_point = None
            elif fingers_up == 5:
                canvas = np.ones((display_h, display_w, 3), np.uint8) * 255
                prev_x, prev_y = 0, 0
                start_point = None
                print("Cleared canvas")
            else:
                prev_x, prev_y = 0, 0
    else:
        if is_drawing_in_ppt:
            print("Stopping PowerPoint drawing")
            pyautogui.mouseUp()
            pyautogui.hotkey("ctrl", "a")
            is_drawing_in_ppt = False
        if shape_mode and start_point is not None and time.time() - last_hand_time > 0.5:
            print(f"Finalizing shape (timeout) at ({screen_x}, {screen_y})")
            if draw_circle:
                radius = int(math.hypot(screen_x - start_point[0], screen_y - start_point[1]))
                if radius > 20:
                    cv2.circle(canvas, start_point, radius, brush_color, brush_thickness)
                    print(f"Circle drawn with radius {radius}")
            else:
                if abs(screen_x - start_point[0]) > 20 and abs(screen_y - start_point[1]) > 20:
                    cv2.rectangle(canvas, start_point, (screen_x, screen_y), brush_color, brush_thickness)
                    print(f"Rectangle drawn from {start_point} to ({screen_x}, {screen_y})")
            start_point = None

    # ------------------ Capture PPT Screen ------------------
    screen = ImageGrab.grab()
    slide = np.array(screen)
    slide = cv2.cvtColor(slide, cv2.COLOR_RGB2BGR)
    slide = cv2.resize(slide, (display_w, display_h))

    # ------------------ Combine Canvas with Slide ------------------
    annotated_slide = cv2.addWeighted(slide, 0.6, temp_canvas, 1.0, 0)

    # ------------------ Show Webcam Feed for Debugging ------------------
    cv2.imshow("Webcam Feed", frame)
    cv2.imshow("PPT Annotation + Cursor Control", annotated_slide)

    # ------------------ Key Controls ------------------
    key = cv2.waitKey(10) & 0xFF
    if key == ord('m'):
        shape_mode = not shape_mode
        print(f"Shape Mode: {'ON' if shape_mode else 'OFF'}")
    elif key == ord('c'):
        draw_circle = not draw_circle
        print(f"Drawing: {'Circle' if draw_circle else 'Rectangle'}")
    elif key == ord('r'):
        cursor_mode = not cursor_mode
        if is_drawing_in_ppt:
            print("Stopping PowerPoint drawing")
            pyautogui.mouseUp()
            pyautogui.hotkey("ctrl", "a")
            is_drawing_in_ppt = False
        print(f"Cursor Mode: {'ON' if cursor_mode else 'OFF'}")
    elif key == ord('t'):
        cv2.line(canvas, (100, 100), (300, 300), brush_color, brush_thickness)
        print("Test draw on canvas")
    elif key == ord('s'):
        filename = f"output/slide_annotated_{len(snapshots)+1}.png"
        cv2.imwrite(filename, annotated_slide)
        snapshots.append(filename)
        print(f"Saved {filename}, Total snapshots: {len(snapshots)}")
    elif key == ord('p') and snapshots:
        save_as_pdf(snapshots, "output/annotated_slides.pdf")
        print("Exported annotated_slides.pdf")
    elif key == ord('q'):
        if is_drawing_in_ppt:
            print("Stopping PowerPoint drawing")
            pyautogui.mouseUp()
            pyautogui.hotkey("ctrl", "a")
        break

cap.release()
cv2.destroyAllWindows()