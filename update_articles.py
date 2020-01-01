import subprocess
import sys

subprocess.call([sys.executable, 'Electrek2.py'])
print("Electrek2 updated")
subprocess.call([sys.executable, 'insideevs2.py'])
print("insideevs2 updated")
subprocess.call([sys.executable, 'teslarati2.py'])
print("teslarati2 updated")
subprocess.call([sys.executable, 'cleantechnica2.py'])
print("cleantechnica2 updated")
subprocess.call([sys.executable, 'electrive2.py'])
print("electrive2 updated")
subprocess.call([sys.executable, 'greencarguide2.py'])
print("greencarguide2 updated")
subprocess.call([sys.executable, 'greencarreports2.py'])
print("greencarreports2 updated")
subprocess.call([sys.executable, 'chargedevs2.py'])
print("chargedevs2 updated")

print("done")