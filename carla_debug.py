import faulthandler; faulthandler.enable()
import carla, random

client = carla.Client('localhost', 2000)
client.set_timeout(30.0)
world = client.get_world()
print("1 world ok", flush=True)

m = world.get_map()
print("2 get_map ok", flush=True)

tm = client.get_trafficmanager(8000)
print("3 trafficmanager ok", flush=True)

bp = world.get_blueprint_library().filter('vehicle.tesla.model3')[0]
sp = random.choice(m.get_spawn_points())
car = world.spawn_actor(bp, sp)
print("4 spawn ok", flush=True)

car.set_autopilot(True, tm.get_port())
print("5 autopilot ok", flush=True)
car.destroy()