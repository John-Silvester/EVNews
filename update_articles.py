import subprocess
import sys
import concurrent.futures
import time

start = time.perf_counter()


def get_new_articles(outlet):
    subprocess.call([sys.executable, outlet])
    return f'Done Updating...{outlet}'


with concurrent.futures.ThreadPoolExecutor() as executor:
    outlets = ['Electrek.py', 'insideevs.py', 'teslarati.py',
               'cleantechnica.py', 'electrive.py', 'reneweconomy.py',
               'greencarguide.py', 'greencarreports.py', 'chargedevs.py',
               'evobsession.py', 'thevergecars.py']
    # , 'autoblog2.py'
    results = executor.map(get_new_articles, outlets)

    for result in results:
        print(result)


finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')
