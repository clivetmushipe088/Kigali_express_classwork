# Kigali Express

## Problem

Kigali Express has 10,000 drivers. Every customer request searched the list of drivers one by one, which made lookups slow.

Our fix was to convert the list into a dictionary where the keys are driver IDs. Looking up a driver then takes O(1) time instead of O(N).

## How to run

```
python3 driver_lookup.py
```

`drivers.json` is the raw list we convert. Keep it next to the script, the program stops with a message if it is missing.

## Search methods

**Linear search, O(N):** checks each driver one by one.

**Binary search, O(log N):** splits a sorted list in half each step. The list has to stay sorted.

**HashMap, O(1):** the mapping loop runs once to build a dictionary `{driver_id: driver}`. Each lookup after that is a single step.

```python
def build_driver_map(drivers):
    driver_map = {}
    for driver in drivers:
        driver_map[driver["id"]] = driver
    return driver_map


def find_driver_fast(driver_map, driver_id):
    return driver_map.get(driver_id)
```

## How many drivers each method checks

| Method | Average | Worst case |
|---|---|---|
| Linear | 5,001 | 10,000 |
| Binary | 13 | 14 |
| HashMap | 1 | 1 |

## Results

10,000 drivers, 1,000 random requests:

| Method | Setup | Per lookup | Speed-up |
|---|---|---|---|
| Linear Search | - | ~93 µs | 1x |
| Binary Search | ~0.4 ms (sort) | ~1.0 µs | ~94x |
| HashMap | ~0.3 ms (build) | ~0.06 µs | ~1,500x |

