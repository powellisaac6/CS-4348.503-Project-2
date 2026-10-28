# CS4348 Project 2

## Files
- CS-4348.503-Project-2-irp220000.py: A bank simulation containing 3 teller threads and 50 customer threads. This program was synchronized using semaphores.
- devlog.md: development log.

## How to run
python3 CS-4348.503-Project-2-irp220000.py

(On Windows: python CS-4348.503-Project-2-irp220000.py)

No inputs or arguments needed.

Program prints at each step, then ends at "The bank closes for the day."

## Notes
- Semaphores are used as locks (print, teller queue, counters, door, safe, manager) and signals (doorbells, asking/giving/finishing/leaving, bank_open).