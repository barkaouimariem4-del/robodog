# robodog

12-DOF quadruped controlled from a web page. Raspberry Pi 5, PCA9685, 12x DS3218MG servos.

## Web app (keyboard control)

Keys: W forward, S backward, A turn left, D turn right (Z and Q also work on AZERTY).
W + A or W + D: walk while turning.

### How it works
The page (`webapp/index.html`) sends the pressed keys to a Flask server
(`webapp/server.py`) running on the Raspberry Pi, which passes them to the gait code.

### Safety
- The robot stops when the key is released.
- The robot stops if the page loses focus.
- The server stops the robot if no message is received for 0.4 s.

### Run
    pip install flask
    python server.py
Then open http://<pi-address>:5000 in a browser on the same Wi-Fi.

### Status
Tested on a PC only. Connection to the walking code is planned for the build phase.
