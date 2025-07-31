# import cv2
# import numpy as np
# import mediapipe as mp
# import pyautogui
# import math, time, os
# from PIL import ImageGrab
# from reportlab.pdfgen import canvas as pdf_canvas
# from reportlab.lib.pagesizes import A4

# # ------------------ Setup ------------------
# mp_hands = mp.solutions.hands
# mp_draw = mp.solutions.drawing_utils
# hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)

# cap = cv2.VideoCapture(0)

# # Get screen resolution
# screen = ImageGrab.grab()
# screen_w, screen_h = screen.size

# canvas = np.zeros((screen_h, screen_w, 3), np.uint8)

# # Brush settings
# brush_color = (0, 255, 0)
# brush_thickness = 10
# eraser_thickness = 50
# colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 255)]
# color_index = 0

# prev_x, prev_y = 0, 0
# snapshots = []

# # Shape Drawing
# shape_mode = False
# draw_circle = False
# start_point = None

# # Create output folder
# if not os.path.exists("output"):
#     os.makedirs("output")

# print("🎨 PPT Annotation + Shapes Instructions:")
# print("1 Finger → Draw/Shape | 2 Fingers → Erase | 3 Fingers → Next Slide")
# print("4 Fingers → Previous Slide / Change Color | 5 Fingers → Clear")
# print("Press M → Toggle Shape Mode | Press C → Switch Rectangle/Circle")
# print("S → Save Annotated Slide | P → Export All to PDF | Q → Quit")

# # ------------------ PDF Saving Function ------------------
# def save_as_pdf(image_files, output_file):
#     c = pdf_canvas.Canvas(output_file, pagesize=A4)
#     for img_path in image_files:
#         c.drawImage(img_path, 0, 0, width=595, height=842)  # Fit to A4
#         c.showPage()
#     c.save()

# # ------------------ Main Loop ------------------
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame = cv2.flip(frame, 1)
#     h, w, _ = frame.shape

#     # Mediapipe processing
#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     result = hands.process(rgb)

#     fingers_up = 0
#     x_tip, y_tip = 0, 0

#     temp_canvas = canvas.copy()  # For shape preview

#     if result.multi_hand_landmarks:
#         for hand_landmarks in result.multi_hand_landmarks:
#             mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#             # Landmark list
#             landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]

#             # Finger Tips
#             tip_ids = [4, 8, 12, 16, 20]
#             fingers = []

#             # Thumb
#             fingers.append(1 if landmarks[tip_ids[0]][0] > landmarks[tip_ids[0] - 1][0] else 0)
#             # Other four fingers
#             for i in range(1, 5):
#                 fingers.append(1 if landmarks[tip_ids[i]][1] < landmarks[tip_ids[i] - 2][1] else 0)

#             fingers_up = fingers.count(1)
#             x_tip, y_tip = landmarks[8]

#             # Convert to screen coordinates
#             screen_x = int(x_tip * (screen_w / w))
#             screen_y = int(y_tip * (screen_h / h))

#             # Dynamic Brush Size (Thumb-Index Distance)
#             distance = math.hypot(landmarks[4][0] - x_tip, landmarks[4][1] - y_tip)
#             brush_thickness = int(np.interp(distance, [20, 200], [5, 50]))

#             # ------------------ Gesture Modes ------------------
#             if fingers_up == 1:  # Draw or Shape
#                 if shape_mode:
#                     if start_point is None:
#                         start_point = (screen_x, screen_y)
#                     else:
#                         if draw_circle:
#                             radius = int(math.hypot(screen_x - start_point[0], screen_y - start_point[1]))
#                             cv2.circle(temp_canvas, start_point, radius, brush_color, brush_thickness)
#                         else:
#                             cv2.rectangle(temp_canvas, start_point, (screen_x, screen_y), brush_color, brush_thickness)
#                 else:  # Freehand Drawing
#                     if prev_x == 0 and prev_y == 0:
#                         prev_x, prev_y = screen_x, screen_y
#                     cv2.line(canvas, (prev_x, prev_y), (screen_x, screen_y), brush_color, brush_thickness)
#                     prev_x, prev_y = screen_x, screen_y

#             elif fingers_up == 0 and shape_mode and start_point is not None:
#                 # Finalize Shape
#                 if draw_circle:
#                     radius = int(math.hypot(screen_x - start_point[0], screen_y - start_point[1]))
#                     cv2.circle(canvas, start_point, radius, brush_color, brush_thickness)
#                 else:
#                     cv2.rectangle(canvas, start_point, (screen_x, screen_y), brush_color, brush_thickness)
#                 start_point = None

#             elif fingers_up == 2:  # Eraser Mode
#                 cv2.circle(canvas, (screen_x, screen_y), eraser_thickness, (0, 0, 0), -1)
#                 prev_x, prev_y = 0, 0
#                 start_point = None

#             elif fingers_up == 3:  # Next Slide
#                 pyautogui.press("right")
#                 time.sleep(0.3)
#                 prev_x, prev_y = 0, 0
#                 start_point = None

#             elif fingers_up == 4:  # Previous Slide + Change Color
#                 color_index = (color_index + 1) % len(colors)
#                 brush_color = colors[color_index]
#                 pyautogui.press("left")
#                 time.sleep(0.3)
#                 prev_x, prev_y = 0, 0
#                 start_point = None

#             elif fingers_up == 5:  # Clear Canvas
#                 canvas = np.zeros_like(canvas)
#                 prev_x, prev_y = 0, 0
#                 start_point = None

#             else:
#                 prev_x, prev_y = 0, 0

#     # ------------------ Capture PPT Screen ------------------
#     screen = ImageGrab.grab()
#     slide = np.array(screen)
#     slide = cv2.cvtColor(slide, cv2.COLOR_RGB2BGR)

#     # ------------------ Combine Canvas with Slide ------------------
#     annotated_slide = cv2.addWeighted(slide, 1, temp_canvas, 0.5, 0)

#     cv2.imshow("PPT Annotation + Shapes", cv2.resize(annotated_slide, (1280, 720)))

#     # ------------------ Key Controls ------------------
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('m'):
#         shape_mode = not shape_mode
#         print(f"Shape Mode {'ON' if shape_mode else 'OFF'}")
#     elif key == ord('c'):
#         draw_circle = not draw_circle
#         print(f"Drawing {'Circle' if draw_circle else 'Rectangle'}")
#     elif key == ord('s'):  # Save annotated slide
#         filename = f"output/slide_annotated_{len(snapshots)+1}.png"
#         cv2.imwrite(filename, annotated_slide)
#         snapshots.append(filename)
#         print(f"✅ Saved {filename}")
#     elif key == ord('p') and snapshots:  # Export PDF
#         save_as_pdf(snapshots, "output/annotated_slides.pdf")
#         print("📄 Exported annotated_slides.pdf")
#     elif key == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import math
import time
import os
try:
    import pygetwindow as gw
except ImportError:
    gw = None
from PIL import ImageGrab
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import A4

# ------------------ Setup ------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)

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
colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 255)]
color_index = 0

prev_x, prev_y = 0, 0
snapshots = []
cursor_positions = []  # For smoothing

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
print("1 Finger → Draw (Shape in shape mode) or Move Cursor (Cursor mode)")
print("2 Fingers → Click (Cursor mode) | 3 Fingers → Next Slide")
print("4 Fingers → Previous Slide / Change Color | 5 Fingers → Clear Canvas")
print("Press M → Toggle Shape Mode | Press C → Switch Rectangle/Circle")
print("Press R → Toggle Cursor Mode | Press T → Test Draw | S → Save Slide | P → Export PDF | Q → Quit")

# ------------------ PDF Saving Function ------------------
def save_as_pdf(image_files, output_file):
    c = pdf_canvas.Canvas(output_file, pagesize=A4)
    for img_path in image_files:
        c.drawImage(img_path, 0, 0, width=595, height=842)
        c.showPage()
    c.save()

# ------------------ Focus PowerPoint ------------------
def focus_powerpoint():
    if gw:
        try:
            windows = gw.getWindowsWithTitle("PowerPoint")
            if windows:
                windows[0].activate()
                print("Focused PowerPoint window")
            else:
                print("PowerPoint window not found")
        except Exception as e:
            print(f"Error focusing PowerPoint: {e}")
    pyautogui.hotkey("alt", "tab")
    time.sleep(0.2)
    pyautogui.click(screen_w // 2, screen_h // 2)

# ------------------ Main Loop ------------------
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
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Landmark list
            landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]

            # Finger Tips
            tip_ids = [4, 8, 12, 16, 20]
            fingers = []

            # Thumb (handle both left and right hands)
            thumb_tip = landmarks[tip_ids[0]][0]
            thumb_ip = landmarks[tip_ids[0] - 1][0]
            fingers.append(1 if thumb_tip > thumb_ip or thumb_tip < thumb_ip else 0)
            for i in range(1, 5):
                fingers.append(1 if landmarks[tip_ids[i]][1] < landmarks[tip_ids[i] - 2][1] else 0)

            fingers_up = fingers.count(1)
            x_tip, y_tip = landmarks[8]

            # Convert to display and screen coordinates
            screen_x = int(x_tip * (display_w / w))
            screen_y = int(y_tip * (display_h / h))
            screen_x = max(0, min(screen_x, display_w - 1))
            screen_y = max(0, min(screen_y, display_h - 1))

            cursor_x = int(x_tip * (screen_w / w))
            cursor_y = int(y_tip * (screen_h / h))
            cursor_x = max(0, min(cursor_x, screen_w - 1))
            cursor_y = max(0, min(cursor_y, screen_h - 1))

            # Smooth cursor movement
            cursor_positions.append((cursor_x, cursor_y))
            if len(cursor_positions) > 5:
                cursor_positions.pop(0)
            avg_cursor_x = int(sum(x for x, _ in cursor_positions) / len(cursor_positions))
            avg_cursor_y = int(sum(y for _, y in cursor_positions) / len(cursor_positions))

            # Dynamic Brush Size
            distance = math.hypot(landmarks[4][0] - x_tip, landmarks[4][1] - y_tip)
            brush_thickness = int(np.interp(distance, [20, 200], [5, 50]))

            # Draw cursor point
            cv2.circle(temp_canvas, (screen_x, screen_y), 5, (255, 0, 0), -1)

            # Debug
            print(f"Fingers up: {fingers_up}, Draw coords: ({screen_x}, {screen_y}), Cursor coords: ({avg_cursor_x}, {avg_cursor_y})")

            # ------------------ Gesture Modes ------------------
            if fingers_up == 1:
                if cursor_mode:
                    print(f"Moving cursor to ({avg_cursor_x}, {avg_cursor_y})")
                    pyautogui.moveTo(avg_cursor_x, avg_cursor_y)
                elif shape_mode:
                    print(f"Drawing shape at ({screen_x}, {screen_y})")
                    if start_point is None:
                        start_point = (screen_x, screen_y)
                        print(f"Shape started at {start_point}")
                    else:
                        if draw_circle:
                            radius = int(math.hypot(screen_x - start_point[0], screen_y - start_point[1]))
                            cv2.circle(temp_canvas, start_point, radius, brush_color, brush_thickness)
                        else:
                            cv2.rectangle(temp_canvas, start_point, (screen_x, screen_y), brush_color, brush_thickness)
                else:
                    print(f"Drawing freehand at ({screen_x}, {screen_y})")
                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = screen_x, screen_y
                    cv2.line(canvas, (prev_x, prev_y), (screen_x, screen_y), brush_color, brush_thickness)
                    prev_x, prev_y = screen_x, screen_y

            elif fingers_up == 0 and shape_mode and start_point is not None:
                print(f"Finalizing shape at ({screen_x}, {screen_y})")
                if draw_circle:
                    radius = int(math.hypot(screen_x - start_point[0], screen_y - start_point[1]))
                    if radius > 10:
                        cv2.circle(canvas, start_point, radius, brush_color, brush_thickness)
                else:
                    if abs(screen_x - start_point[0]) > 10 and abs(screen_y - start_point[1]) > 10:
                        cv2.rectangle(canvas, start_point, (screen_x, screen_y), brush_color, brush_thickness)
                start_point = None

            elif fingers_up == 2 and cursor_mode:
                print(f"Clicking at ({avg_cursor_x}, {avg_cursor_y})")
                pyautogui.click(avg_cursor_x, avg_cursor_y)
                time.sleep(0.5)
                prev_x, prev_y = 0, 0
                start_point = None

            elif fingers_up == 3:
                print("Next slide triggered: Sending keys")
                focus_powerpoint()
                pyautogui.press("right")
                pyautogui.press("space")
                pyautogui.press("n")
                pyautogui.press("enter")
                pyautogui.press("pgdn")
                time.sleep(1.5)
                prev_x, prev_y = 0, 0
                start_point = None

            elif fingers_up == 4:
                print("Previous slide triggered: Sending keys")
                color_index = (color_index + 1) % len(colors)
                brush_color = colors[color_index]
                focus_powerpoint()
                pyautogui.press("left")
                pyautogui.press("p")
                pyautogui.press("pgup")
                time.sleep(1.5)
                prev_x, prev_y = 0, 0
                start_point = None

            elif fingers_up == 5:
                print("Clear canvas triggered")
                canvas = np.ones((display_h, display_w, 3), np.uint8) * 255
                prev_x, prev_y = 0, 0
                start_point = None

            else:
                prev_x, prev_y = 0, 0

    # ------------------ Capture PPT Screen ------------------
    screen = ImageGrab.grab()
    slide = np.array(screen)
    slide = cv2.cvtColor(slide, cv2.COLOR_RGB2BGR)
    slide = cv2.resize(slide, (display_w, display_h))

    # ------------------ Combine Canvas with Slide ------------------
    annotated_slide = cv2.addWeighted(slide, 0.6, temp_canvas, 1.0, 0)

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
        print(f"Cursor Mode: {'ON' if cursor_mode else 'OFF'}")
    elif key == ord('t'):  # Test drawing
        print("Test drawing triggered")
        cv2.line(canvas, (100, 100), (300, 300), brush_color, brush_thickness)
    elif key == ord('s'):
        filename = f"output/slide_annotated_{len(snapshots)+1}.png"
        cv2.imwrite(filename, annotated_slide)
        snapshots.append(filename)
        print(f"Saved {filename}, Total snapshots: {len(snapshots)}")
    elif key == ord('p') and snapshots:
        print(f"Exporting {len(snapshots)} snapshots to PDF")
        save_as_pdf(snapshots, "output/annotated_slides.pdf")
        print("Exported annotated_slides.pdf")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()