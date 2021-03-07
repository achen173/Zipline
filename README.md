# Zipline Challenge Question
Position: Junior Embedded Systems Software Engineer - Robotics Prototyping


## Build and Run Program
Python Version: 3.9.2
When you clone this repo, it should have the python virtual environment - "test_environment"

To Activate the virtual environment
* test_environment/bin/activate

To install dependencies
* pip install -r requirements

To run the autopilots
* python zip_sim.py python my_pilot.py

## Implementation

To avoid the trees, I use the 31 lidar samples to find the closest minimum "clear Y position" and transverse over to the position. Note that for changing position, I taken into account 3 things: wind in XY direction, current position, and the position where I want to be. For the package landing, I got the randomly generated XY coordinates from zip_sum file and passed that over to the autopilot as a parsed and formatted data so it can be in the lidar sample bit positions. With the XY coordinates, I can target the landing whenever it is in proximity (~35m X direction) and dropped the package when it is ~9m in X direction before the location. Note that if there is a tree within 35m and it is in the direction of the dropping location, the drone will crash because it will prioritze getting to that location. This is something that should be fixed for future implementation. Finally for the landing, I used the given RecoveryXY position and Wind-Y to detemine that lateral airspeed and when to send that command package. Below is a list of implementation requirements and an explaination is to why I met or did not met the goal. 

## External Requirements - These requirements must be met by your implementation in order for it to be considered readyfor production.


### Double-delivery rate less than 1 in 1000 flights (ZIPAA requirement to avoid liability)
 * This will never happen because after dropping a package, you won't be able to drop another one until after you pass the the current drop-location


### Crash rate less than 1 in 100 flights (ZAA safety requirement for certification)
 * For my implementation, the crash rate is probably above 1 in 100 flights because a target and a tree can be in close proximity. My code uses the fact that if a target drop is close (~35m), it will approach that location regardless if the tree is in the way. This is most likely where the crash will occur and a problem to be solved in future implementations  
 
 
### Parachute rate less than 1 in 10 flights (Budget for replacement hardware in operation)
 * Parachute rate will never happen because the autopolit is programmed to land on the landing zone when it comes within 35 meters. It is gaurantee to land unless there are trees within 35 meters which will be considered in crash rate not parachute rate


### Deliver at least 10% of packages on average (Contractual obligation with customer)
 * At least 10% of delivered packages is extremely likely unless there is a crash
