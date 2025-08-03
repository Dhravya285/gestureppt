Gesture-Based PPT Controller
This project enables you to control a PowerPoint presentation using hand gestures captured via a webcam. It supports slide navigation, freehand drawing, shape annotations, and cursor control, with the ability to save annotated slides as images and export them as a PDF. The project uses MediaPipe for hand tracking, OpenCV for video processing, and PyAutoGUI for system control.
Features

Slide Navigation: Move to the next slide (3 fingers) or previous slide (4 fingers).
Freehand Drawing: Draw on slides with 1 finger (green pencil brush, adjustable thickness).
Shape Drawing: Draw rectangles or circles (toggle with m and c keys).
Cursor Control: Move the system cursor (1 finger) and click (2 fingers) when in cursor mode (toggle with r).
Save and Export: Save annotated slides as PNGs (s key) and export to PDF (p key).
Clear Canvas: Clear annotations with 5 fingers.

Requirements

Python 3.7+
Dependencies:
opencv-python
mediapipe
pyautogui
Pillow
reportlab
pygetwindow (for PowerPoint focus)


Hardware: Webcam, Windows OS (tested on Windows, may work on macOS with adjustments).
Software: Microsoft PowerPoint (slide show mode).

Installation

Clone or Download:
Download the main.py script or clone the repository.


Install Dependencies:pip install opencv-python mediapipe pyautogui Pillow reportlab pygetwindow


Verify Webcam: Ensure your webcam is connected and functional.
Prepare PowerPoint: Have a presentation ready in slide show mode (F5).

Usage

Run the Script:python main.py

The script will initialize the webcam and display instructions in the terminal:🎨 PPT Annotation + Cursor Control Instructions:
1 Finger → Draw (Shape in shape mode) or Move Cursor (Cursor mode)
2 Fingers → Click (Cursor mode) | 3 Fingers → Next Slide
4 Fingers → Previous Slide / Change Color | 5 Fingers → Clear Canvas
Press M → Toggle Shape Mode | Press C → Switch Rectangle/Circle
Press R → Toggle Cursor Mode | Press T → Test Draw | S → Save Slide | P → Export PDF | Q → Quit


Open PowerPoint:
Start your presentation in slide show mode (F5) and maximize the window.


Perform Gestures:
Drawing: Show 1 finger (index up, others down) to draw. Ensure cursor mode is off (r to toggle off).
Shapes: Press m to enable shape mode, c to toggle rectangle/circle. Show 1 finger to start, move, hide fingers to finalize.
Cursor Control: Press r to enable cursor mode. Show 1 finger to move cursor, 2 fingers to click.
Navigation: Show 3 fingers for next slide, 4 fingers for previous slide (also changes drawing color).
Clear Canvas: Show 5 fingers to clear annotations.
Save/Export: Press s to save a snapshot, p to export snapshots as PDF.
Test Drawing: Press t to draw a test line to verify rendering.
Quit: Press q to exit.


Monitor Output:
Check the OpenCV window ("PPT Annotation + Cursor Control") for the PowerPoint slide, annotations, and a red cursor dot.
Watch the terminal for debug messages (e.g., Drawing freehand at (x, y), Next slide triggered).



Troubleshooting

Annotations Not Appearing:
Ensure Cursor Mode: OFF (press r).
Show 1 finger clearly (index up, others down) in good lighting.
Press t to test drawing. If no line appears, check OpenCV window rendering.
Verify terminal output shows Fingers up: 1 and Drawing freehand at (x, y).


Slides Not Changing:
Ensure PowerPoint is in slide show mode and focused.
Check for Next slide triggered or Previous slide triggered in terminal.
Manually test right/left keys in PowerPoint to confirm responsiveness.
If PowerPoint window not found appears, ensure PowerPoint is open and maximized.


Cursor Not Moving/Clicking:
Toggle cursor mode with r (Cursor Mode: ON).
Show 1 finger for movement, 2 fingers for clicking. Check for Moving cursor to (x, y) or Clicking at (x, y).


Hand Detection Issues:
Ensure good lighting and hand fully visible in webcam.
Adjust hand orientation (palm facing camera, fingers distinct).


Dependencies:
Install pygetwindow if PowerPoint focus fails (pip install pygetwindow).
Ensure all dependencies are installed correctly.



Notes

Canvas: Annotations appear on a white canvas overlaid on the PowerPoint slide in the OpenCV window.
Output: Snapshots are saved in the output/ folder as PNGs, and PDFs are exported there.
Performance: Lower webcam resolution (640x480) is used for better performance. Adjust if needed.
Windows-Specific: The alt+tab focus and pygetwindow are optimized for Windows. macOS users may need to modify focus logic.

Example Terminal Output
Fingers up: 1, Draw coords: (174, 370), Cursor coords: (261, 555)
Drawing freehand at (174, 370)
Fingers up: 3, Draw coords: (554, 501), Cursor coords: (831, 751)
Next slide triggered: Sending keys
Focused PowerPoint window
Fingers up: 2, Draw coords: (462, 262), Cursor coords: (693, 393)
Clicking at (693, 393)

Contributing
Feel free to submit issues or pull requests to improve gesture detection, add features, or support other presentation software.
License
This project is licensed under the MIT License.
