import subprocess
import sys

subprocess.call([sys.executable, '/home/john/PycharmProjects/EVNews/Electrek2.py'])
print("Electrek2 updated")
subprocess.call([sys.executable, '/home/john/PycharmProjects/EVNews/insideevs2.py'])
print("insideevs2 updated")
subprocess.call([sys.executable, '/home/john/PycharmProjects/EVNews/teslarati2.py'])
print("teslarati2 updated")
subprocess.call([sys.executable, '/home/john/PycharmProjects/EVNews/cleantechnica2.py'])
print("cleantechnica2 updated")
subprocess.call([sys.executable, '/home/john/PycharmProjects/EVNews/electrive2.py'])
print("electrive2 updated")
subprocess.call([sys.executable, '/home/john/PycharmProjects/EVNews/greencarguide2.py'])
print("greencarguide2 updated")
subprocess.call([sys.executable, '/home/john/PycharmProjects/EVNews/greencarreports2.py'])
print("greencarreports2 updated")
subprocess.call([sys.executable, '/home/john/PycharmProjects/EVNews/chargedevs2.py'])
print("chargedevs2 updated")

print("done")