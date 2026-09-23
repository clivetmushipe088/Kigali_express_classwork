# Kigali Express

## Problem

Kigali Express has 10,000 drivers. Every customer request searched the list of drivers one by one, which made lookups slow.

Our fix was to convert the list into a dictionary where the keys are driver IDs. Looking up a driver then takes O(1) time instead of O(N).

## How to run

```
python3 driver_lookup.py
```

No installation needed, standard library only. Tested on Python 3.14.

## Files

```
driver_lookup.py    all three search methods and the benchmark
drivers.json        the 10,000 sample drivers
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

Building the dictionary takes about 0.3 ms and only happens once. It pays for itself after about 3 lookups. Timings will vary from one computer to another.

## Notes

- Our driver IDs are already in order in the file, so the sort is faster than it would normally be. On shuffled data the sort takes longer, but the per-lookup times stay about the same.
- Binary search needs the list sorted and kept sorted. Adding a driver means inserting it in the right place, not just appending.
- The dictionary has to be updated whenever a driver is added or removed, otherwise it goes stale:
  ```python
  drivers.append(new_driver)
  driver_map[new_driver["id"]] = new_driver
  ```
- `find_driver_fast` uses `.get()` so an unknown ID returns `None` instead of raising `KeyError`.
