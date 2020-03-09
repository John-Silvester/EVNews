import subprocess
import sys
import concurrent.futures
import time

start = time.perf_counter()


def get_new_articles(outlet):
    subprocess.call([sys.executable, outlet])
    return f'Done Updating...{outlet}'


with concurrent.futures.ThreadPoolExecutor() as executor:
    outlets = ['Electrek2.py', 'insideevs2.py', 'teslarati2.py',
               'cleantechnica2.py', 'electrive2.py', 'reneweconomy2.py',
               'greencarguide2.py', 'greencarreports2.py', 'chargedevs2.py',
               'evobsession2.py', 'thevergecars2.py']
    # , 'autoblog2.py'
    results = executor.map(get_new_articles, outlets)

    for result in results:
        print(result)


finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')
