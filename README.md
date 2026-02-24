Hand Gesture Mouse Control

Control your computer mouse using hand gestures detected via webcam.
This project uses MediaPipe hand tracking, OpenCV, and PyAutoGUI to translate gestures into cursor movement, clicks, scrolling, and system actions.

Features

	•	Move mouse with right hand index finger
	•	Left-hand gestures for:
	•	Click (pinch)
	•	Drag (gesture hold)
	•	Scroll up/down (thumb gestures)
	•	Mission Control trigger (macOS)
	•	Smooth cursor movement
	•	Multi-hand detection

Uses webcam input to track both hands and map gestures to mouse controls.

----------------------------------------------------------------------------------------------------------------------------------

Requirements

	•	Python 3.9–3.11
  
	•	Webcam
  
	•	macOS / Windows / Linux (PyAutoGUI compatible)
  

----------------------------------------------------------------------------------------------------------------------------------

Controls

Right Hand

	•	Index finger movement -> Move cursor
	•	Open hand -> Stop Mouse

  
Left Hand

	•	Thumb + index pinch -> Click
	•	Spiderman gesture -> Drag
	•	Thumbs up -> Scroll up
	•	Thumbs down -> Scroll down
	•	Thumb + pinky -> Mission Control (macOS)
