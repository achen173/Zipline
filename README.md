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

## External Requirements - These requirements must be met by your implementation in order for it to be considered readyfor production.

### Double-delivery rate less than 1 in 1000 flights (ZIPAA requirement to avoid liability)
 * This will never happen because after dropping a package, you won't be able to drop another one until after you pass the the current drop-location

### Crash rate less than 1 in 100 flights (ZAA safety requirement for certification)
 * For my implementation, the crash rate is probably above 1 in 100 flights because a target and a tree can be in close proximity. My code uses the fact that if a target drop is close (~35m), it will approach that location regardless if the tree is in the way. This is most likely where the crash will occur and a problem to be solved in future implementations  
 
### Parachute rate less than 1 in 10 flights (Budget for replacement hardware in operation)
 * Parachute rate will never happen because the autopolit is programmed to land on the landing zone when it comes within 35 meters. It is gaurantee to land unless there are trees within 35 meters which will be considered in crash rate not parachute rate

### Deliver at least 10% of packages on average (Contractual obligation with customer)
 * At least 10% of delivered packages is extremely likely unless there is a crash
