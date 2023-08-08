# wheel
Modules for the steering wheel controller.


## Contents
- [calibrate_brake.py](./calibrate_brake.py) helps with calibrating the brake parameters in [wheel_config.ini](./wheel_config.ini). It can be run on its own, but requires the `scipy` package.

- [carla_control](./carla_control.py) conatins an interface between the steering wheel controller and a CARLA `VehicleControl`. 

- [control.py](./control.py) contains a generic intrface for the steering wheel controller. 

- [wheel_config.ini](./wheel_config.ini) stores configurations for the steering wheel's buttons, levers and pedals.
