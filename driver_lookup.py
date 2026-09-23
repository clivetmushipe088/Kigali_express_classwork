import json
import os
import random
import timeit

# Seed the random generator so the sample of customer requests is the
# same every time we run this.
random.seed(42)

DATA_FILE = "drivers.json"


# 1. Load the raw list of drivers

def load_drivers():
    # Look for the file next to this script, not wherever we ran it from.
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, DATA_FILE)

    if not os.path.exists(path):
        raise SystemExit("Could not find " + DATA_FILE + " next to this script.")

    with open(path) as f:
        return json.load(f)


# 2. LINEAR SEARCH - O(N)

def find_driver_slow(drivers, driver_id):
    for driver in drivers:
        if driver["id"] == driver_id:
            return driver

    return None


def count_steps_slow(drivers, driver_id):
    steps = 0

    for driver in drivers:
        steps += 1
        if driver["id"] == driver_id:
            return steps

    return steps


# 3. BINARY SEARCH - O(log N)

def sort_drivers(drivers):
    # Binary search only works on a sorted list, so we sort once.
    return sorted(drivers, key=lambda driver: driver["id"])


def find_driver_binary(sorted_drivers, driver_id):
    low = 0
    high = len(sorted_drivers) - 1

    while low <= high:
        middle = (low + high) // 2
        middle_id = sorted_drivers[middle]["id"]

        if middle_id == driver_id:
            return sorted_drivers[middle]
        elif middle_id < driver_id:
            low = middle + 1          # answer is in the right half
        else:
            high = middle - 1         # answer is in the left half

    return None


def count_steps_binary(sorted_drivers, driver_id):
    steps = 0
    low = 0
    high = len(sorted_drivers) - 1

    while low <= high:
        steps += 1
        middle = (low + high) // 2
        middle_id = sorted_drivers[middle]["id"]

        if middle_id == driver_id:
            return steps
        elif middle_id < driver_id:
            low = middle + 1
        else:
            high = middle - 1

    return steps


# 4. THE MAPPING LOOP - build the dictionary once

def build_driver_map(drivers):
    driver_map = {}

    for driver in drivers:
        driver_map[driver["id"]] = driver

    return driver_map

    # Short version of the same loop:
    #     return {driver["id"]: driver for driver in drivers}


# 5. HASHMAP LOOKUP - O(1)

def find_driver_fast(driver_map, driver_id):
    # .get() returns None instead of crashing on an unknown ID.
    return driver_map.get(driver_id)


# 6. Run the comparison

def main():
    print()
    print("=" * 66)
    print("  KIGALI EXPRESS - DRIVER LOOKUP")
    print("=" * 66)

    drivers = load_drivers()
    print("\nLoaded from:", DATA_FILE)
    print("Drivers in the system:", len(drivers))
    print("Example driver:", drivers[0])

    # setup costs (these happen once) 
    sort_time = timeit.timeit(lambda: sort_drivers(drivers), number=10) / 10
    build_time = timeit.timeit(lambda: build_driver_map(drivers), number=10) / 10

    sorted_drivers = sort_drivers(drivers)
    driver_map = build_driver_map(drivers)

    print("\nSorted list ready. Time to sort once: {:.2f} ms".format(sort_time * 1000))
    print("Dictionary built. Time to build once: {:.2f} ms".format(build_time * 1000))

    # all three must agree before we time anything
    test_ids = [1000, 3500, 7777, 10999, 99999]
    for test_id in test_ids:
        found = find_driver_slow(drivers, test_id)
        assert find_driver_binary(sorted_drivers, test_id) == found
        assert find_driver_fast(driver_map, test_id) == found
    print("Correctness check: all three methods agree. OK")

    # how many drivers does each method check? 
    last_id = drivers[-1]["id"]
    middle_id = drivers[len(drivers) // 2]["id"]

    print("\n" + "-" * 66)
    print("  HOW MANY DRIVERS DOES EACH METHOD CHECK?")
    print("-" * 66)
    print("{:<18}{:>12}{:>12}".format("Method", "Average", "Worst case"))
    print("{:<18}{:>12}{:>12}".format(
        "Linear",
        count_steps_slow(drivers, middle_id),
        count_steps_slow(drivers, last_id)))
    print("{:<18}{:>12}{:>12}".format(
        "Binary",
        count_steps_binary(sorted_drivers, middle_id),
        count_steps_binary(sorted_drivers, last_id)))
    print("{:<18}{:>12}{:>12}".format("HashMap", 1, 1))

    # the timing
    # The same 1000 random customer requests for all three methods.
    requests = [random.choice(drivers)["id"] for _ in range(1000)]

    def run_slow():
        for driver_id in requests:
            find_driver_slow(drivers, driver_id)

    def run_binary():
        for driver_id in requests:
            find_driver_binary(sorted_drivers, driver_id)

    def run_fast():
        for driver_id in requests:
            find_driver_fast(driver_map, driver_id)

    print("\nTiming {} lookups with each method, please wait...".format(len(requests)))

    runs = 3
    slow_each = timeit.timeit(run_slow, number=runs) / runs / len(requests)
    binary_each = timeit.timeit(run_binary, number=runs) / runs / len(requests)
    fast_each = timeit.timeit(run_fast, number=runs) / runs / len(requests)

    # results
    rows = [
        ("Linear Search", "O(N)", "-", slow_each),
        ("Binary Search", "O(log N)", "{:.2f} ms (sort)".format(sort_time * 1000), binary_each),
        ("HashMap", "O(1)", "{:.2f} ms (build)".format(build_time * 1000), fast_each),
    ]

    print("\n" + "=" * 66)
    print("  RESULTS")
    print("=" * 66)
    print("{:<16}{:<11}{:<17}{:>12}{:>9}".format(
        "Method", "Big-O", "Setup", "Per lookup", "Speed-up"))
    print("-" * 66)

    for name, big_o, setup, per_lookup in rows:
        print("{:<16}{:<11}{:<17}{:>9.2f} us{:>8.0f}x".format(
            name, big_o, setup, per_lookup * 1_000_000, slow_each / per_lookup))

    print("-" * 66)

    # when does building the dictionary pay for itself?
    saved_per_lookup = slow_each - fast_each
    break_even = build_time / saved_per_lookup

    print("\nBuilding the dictionary costs {:.2f} ms once.".format(build_time * 1000))
    print("Each lookup then saves {:.2f} us.".format(saved_per_lookup * 1_000_000))
    print("So it pays for itself after about {:,.0f} lookups.\n".format(break_even))


if __name__ == "__main__":
    main()
