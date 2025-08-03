Gesture-Based PowerPoint Controller
This project enables gesture-based control of Microsoft PowerPoint presentations using a webcam. It uses hand gestures to navigate slides, annotate presentations, draw on a virtual canvas, and save/export annotations. The system relies on MediaPipe for hand detection and PyAutoGUI for mouse/keyboard control, with all interactions targeting the currently active window (e.g., PowerPoint in Slide Show mode), which you must manually focus.
Features

Slide Navigation: Use 3 fingers to go to the next slide and 4 fingers to go to the previous slide (in PowerPoint Slide Show mode).
Canvas Drawing: Draw freehand lines (1 finger) or erase (2 fingers) on a virtual canvas overlaid on the presentation.
Shape Drawing: Draw rectangles or circles on the canvas in shape_mode (1 finger to start, 0 fingers to finalize).
PowerPoint Annotations: Draw directly in PowerPoint’s Slide Show mode using the pen tool (1 finger in cursor_mode).
Mouse Control: Move the cursor (1 finger in cursor_mode) or click (2 fingers in cursor_mode) in the active window.
Snapshot Saving: Save the current slide with canvas annotations as a PNG (S key).
PDF Export: Export saved snapshots to a PDF (P key).
Clear Canvas: Clear the canvas with 5 fingers.
Dynamic Brush: Brush size adjusts based on thumb-index finger distance; color changes with 4-finger gesture.

Prerequisites

Operating System: Windows (tested on Windows 10/11).
Hardware:
Webcam (internal or external).
Screen resolution of at least 1280x720 (adjustable in code).


Software:
Microsoft PowerPoint (2016, 2019, or 365) for slide navigation and annotations.
Python 3.8+.


Python Libraries:pip install opencv-python numpy mediapipe pyautogui pillow reportlab



Setup

Clone or Download:

Download main.py to your project folder.


Install Dependencies:
pip install opencv-python numpy mediapipe pyautogui pillow reportlab


Prepare PowerPoint:

Open a PowerPoint presentation (.pptx) with multiple slides.
Ensure PowerPoint is ready to enter Slide Show mode (manually press F5 when prompted).


Run the Script:

Run as administrator to ensure PyAutoGUI permissions:python main.py


On first run, an output folder is created for snapshots and PDFs.


Environment:

Ensure good lighting and a plain background for reliable hand detection.
Position your hand 1–2 feet from the webcam, palm facing the camera.



Usage

Start the Program:

Run main.py as administrator.
Two windows open: “Webcam Feed” (shows hand landmarks) and “PPT Annotation + Cursor Control” (shows the slide with canvas overlay).
Console displays instructions and prompts you to manually focus PowerPoint and press F5 for Slide Show mode.


Gestures and Controls:

1 Finger:
Default: Draw freehand lines on the canvas.
In cursor_mode (R key): Move cursor and draw in PowerPoint’s Slide Show mode (pen tool).
In shape_mode (M key): Start drawing a rectangle or circle (toggle with C key).


2 Fingers:
Default: Erase on the canvas.
In cursor_mode: Perform a mouse click in the active window.


3 Fingers: Next slide (PowerPoint must be focused in Slide Show mode).
4 Fingers: Previous slide and change brush color (PowerPoint must be focused).
5 Fingers: Clear the canvas.
Keys:
M: Toggle shape_mode (ON/OFF).
C: Switch between rectangle and circle in shape_mode.
R: Toggle cursor_mode (ON/OFF).
T: Test draw (draws a line on the canvas).
S: Save a snapshot of the slide with canvas annotations.
P: Export snapshots to a PDF (output/annotated_slides.pdf).
Q: Quit the program.




Manual Window Focus:

Manually focus PowerPoint and press F5 to enter Slide Show mode for slide navigation (3/4 fingers) or annotations (1/2 fingers in cursor_mode).
Use Alt+Tab or mouse clicks to switch to other applications if desired; gestures will affect the active window.



Testing Features
Follow these steps to test all features, ensuring no automatic tab-switching occurs and shape drawing works reliably.
Step 1: Verify Setup

Action: Run python main.py as administrator.
Expected: “Webcam Feed” and “PPT Annotation + Cursor Control” windows open. Console prints:Created output folder
Starting program... Please manually focus PowerPoint and press F5 to enter Slide Show mode.


Check: Hand landmarks appear in “Webcam Feed”. Manually focus PowerPoint and press F5.

Step 2: Test No Tab-Switching

Action: Hold up 1, 2, 3, 4, and 5 fingers briefly with PowerPoint or another window focused.
Expected: No window changes occur. Console shows finger counts, e.g.:Fingers up: 1, Draw coords: (x, y), Cursor coords: (x, y)

For 3/4 fingers (with PowerPoint focused):Next slide (ensure PowerPoint is focused in Slide Show mode)
Previous slide, new color: (r, g, b) (ensure PowerPoint is focused in Slide Show mode)


Check: Active window stays the same.

Step 3: Test Shape Drawing (Rectangle)

Action:
Press M to enable shape_mode (“Shape Mode: ON”).
Press C until “Drawing: Rectangle” appears.
Hold 1 finger, move hand, then close hand (0 fingers) or remove hand.


Expected:
Console prints:Shape Mode: ON
Fingers up: 1, Draw coords: (x, y), Cursor coords: (x, y)
Shape started at (x, y)
Previewing shape to (x, y)
Fingers up: 0, Draw coords: (x, y), Cursor coords: (x, y)
Finalizing shape at (x, y)
Rectangle drawn from (x1, y1) to (x2, y2)


Yellow dot, rectangle preview, and final rectangle appear in “PPT Annotation + Cursor Control”.
No tab-switching.


Check: Rectangle drawn in current brush color (default green).

Step 4: Test Shape Drawing (Circle)

Action:
Press C for “Drawing: Circle”.
Hold 1 finger, move hand, then close hand or remove hand.


Expected: Similar console output, ending with:Circle drawn with radius r


Circle drawn in “PPT Annotation + Cursor Control”.
No tab-switching.


Check: Circle appears in current brush color.

Step 5: Test Canvas Drawing and Erasing

Action:
Press M to disable shape_mode (“Shape Mode: OFF”).
Hold 1 finger to draw lines, 2 fingers to erase.


Expected: Lines drawn or erased on canvas. No tab-switching.
Check: Canvas updates in “PPT Annotation + Cursor Control”.

Step 6: Test PowerPoint Annotations

Action:
Manually focus PowerPoint in Slide Show mode.
Press R for cursor_mode (“Cursor Mode: ON”).
Hold 1 finger to draw, 2 fingers to click.


Expected:
Console prints:Activating PowerPoint pen tool (ensure PowerPoint is focused in Slide Show mode)
Moving cursor to (x, y)


Annotations appear in PowerPoint’s Slide Show window.
No tab-switching.


Check: Drawings appear in PowerPoint.

Step 7: Test Slide Navigation

Action:
Focus PowerPoint in Slide Show mode.
Hold 3 fingers for next slide, 4 fingers for previous slide.


Expected: Slides change; console prints:Next slide (ensure PowerPoint is focused in Slide Show mode)
Previous slide, new color: (r, g, b) (ensure PowerPoint is focused in Slide Show mode)


No tab-switching.


Check: Slides navigate correctly.

Step 8: Test Snapshot and PDF Export

Action: Draw shapes, press S to save snapshot, press P to export PDF.
Expected:
Snapshot saved (“Saved output/slide_annotated_1.png”).
PDF exported (“Exported annotated_slides.pdf”).
No tab-switching.


Check: Open PNG/PDF to verify shapes.

Step 9: Test Clear Canvas and Quit

Action: Hold 5 fingers to clear canvas, press Q to quit.
Expected:
Canvas clears (“Cleared canvas”).
Program exits on Q.
No tab-switching.


Check: Canvas resets; windows close.

Troubleshooting

No Webcam Feed:
Change cv2.VideoCapture(0) to 1 or 2 in main.py.
Ensure webcam is connected and not used by another app.


No Hand Landmarks:
Adjust lighting, position hand 1–2 feet away, or lower min_detection_confidence to 0.3:hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.3, min_tracking_confidence=0.5)




Shape Drawing Fails:
No Start Dot: Check console for “Shape started at (x, y)”. Verify 1 finger in “Webcam Feed”.
No Preview: Confirm “Previewing shape to (x, y)”. Adjust min_detection_confidence.
No Final Shape: Verify “Fingers up: 0” or “Finalizing shape (timeout)”. Reduce timeout:time.time() - last_hand_time > 0.3


Tiny Shapes: Lower minimum size:if radius > 10:  # For circles
if abs(screen_x - start_point[0]) > 10 and abs(screen_y - start_point[1]) > 10:  # For rectangles




Slide Navigation/Annotations Fail:
Ensure PowerPoint is focused in Slide Show mode (manually press F5).
Test Ctrl+P in PowerPoint to verify pen tool.


Gestures Mis-detected:
Increase smoothing window:if len(finger_counts) > 5:


Adjust min_detection_confidence to 0.3 or 0.5.


Performance Issues:
Reduce webcam resolution:cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)





Notes

Manual Focus: You must manually focus PowerPoint (or another app) for slide navigation and annotations. Use Alt+Tab or mouse clicks to switch windows.
Shape Drawing: Canvas-based, works regardless of active window.
PowerPoint Annotations: Not captured in snapshots; save the presentation manually to retain them.
Run as Administrator: Ensures PyAutoGUI can control mouse/keyboard.

Reporting Issues
If you encounter issues:

Details: Describe the problem (e.g., “Shapes don’t finalize”, “Slide navigation not working”).
Console Output: Share relevant messages (e.g., “Shape started”, “Next slide”).
Webcam Feed: Are landmarks visible for 1/0 fingers?
Active Window: Which window was focused?
System: Windows version, PowerPoint version, screen resolution.
