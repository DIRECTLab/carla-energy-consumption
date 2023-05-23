# EC Model Implementation in Carla

## Computing Power at the Wheels

```P_Wheels (t) = (m*a(t) + m*g*cos(theta)*(C_r/1000)*(c_1*v(t)+c_2) + (1/2)*rho_Air*A_f*C_D*(v(t)^2) + m*g*sin(theta)) * v(t)```

### Mass of Vehicle (`m`)
From `examples/vehicle_physics.py`:
```
vehicle = world.spawn_actor(vehicle_bp, vehicle_transform)
physics_vehicle = vehicle.get_physics_control()
car_mass = physics_vehicle.mass
```

### Acceleration (`a(t)`)
```
vehicle.get_acceleration()
```

### Road Grade (`theta`)
```
v = vehicle.get_velocity()
horizontal_v = math.sqrt(v.x ** 2 + v.y ** 2)
if horizontal_v > 0.555556: # 2 km/h
# if horizontal_v > 0:
    grade = v.z / horizontal_v
    print(f"Road Grade: {grade}")
```

### Gravitational Acceleration (`g`)
9.8066 m/s^2

### Rolling Resistance Parameters (`C_r`, `c_1`, `c_2`)
"Vary as a function of the road surface type, road condition, and vehicle tire type"

C_r = 1.75

c_1 = 0.0328

c_2 = 4.575
