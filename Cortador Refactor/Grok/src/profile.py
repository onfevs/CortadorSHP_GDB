import time
import cProfile
from main import main

def profile_script():
    start = time.time()
    cProfile.run("main()", sort="cumulative")
    print(f"Tiempo total: {time.time() - start:.2f} segundos")

if __name__ == "__main__":
    profile_script()
