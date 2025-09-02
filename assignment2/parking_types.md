Car Dimensions: 60 x 40


| Parking Type | Width (cm) | Depth (cm) |
|--|--|--|
| Perpendicular | 20 | 30 |
| Parallel | 60 | 20 |
| Angled (45°) | 20 | 30 |

robot dimensions: https://sites.google.com/site/gask3t/lego-ev3/the-missing-commentaries/ev3-beyond-basics-exercises-7-11 

motor metrics: https://www.oreilly.com/library/view/learning-lego-mindstorms/9781783985029/ch02s02.html 

Math for speed per second:

1. Dimensions:
- Wheel Diameter: 5.6 cm
- Wheel Circumference = pi * diameter = ~17.6 cm

2. Max motor RPM (large motor):
- 170 RPM

3. Convert RPM to cm/s at 100% power:
- 170 rotations/min * 17.6 cm/rotation = ~2992 cm/min
- Divide by 60 -> ~49.9 cm/s

4. Estimate for % power:
- Power percentage = wheel speed (self.tank.on(20, 20)) -> 20%
- 49.9 cm/s * 0.20 = ~9.97 cm/s


# Speed calibration script
How to use:

- Put the robot at the start of a measured 50 cm line.

- Run the script.

- Let the robot drive, and when it reaches the 50 cm mark, press Enter to stop it.

- You'll get the actual speed in cm/s for that power level.

You can test at multiple power levels (e.g., 10%, 20%, 30%) to build a small table of speeds if you want even better accuracy.
