import threading

# acquire = acquires one unit from the semaphore counter to do work, waits otherwise
# release = releases one unit to the semaphore counter, allowing other threads to do work

NUM_CUSTOMERS = 3

print_protected = threading.Semaphore(1)    # Avoid print mixing by using a semaphore
curr_customer = None                        # Current customer being served
doorbell = threading.Semaphore(0)           # Customer rings the doorbell to let the teller know they've arrived

teller_queue = []                                   # Queue of tellers that are ready          
teller_queue_protected = threading.Semaphore(1)     # Semaphore to protect the teller queue
num_ready_tellers = threading.Semaphore(0)          # Number of tellers that are ready

def say(msg):       # Print function protected by a semaphore
    print_protected.acquire()
    print(msg)
    print_protected.release()

def teller(tid):
    say(f"Teller {tid} []: ready to serve")                                     # Teller ready
    for _ in range(NUM_CUSTOMERS):                                              # Serve a fixed number of customers
        teller_queue_protected.acquire()                                       
        teller_queue.append(tid)                                                # Add teller to the queue
        teller_queue_protected.release()                                        # Add one teller to the queue                                        
        num_ready_tellers.release()                                             # Increment the number of ready tellers
        say(f"Teller {tid} []: waiting for a customer")                         # Teller waiting
        doorbell.acquire()                                                      # Sleep until customer rings the doorbell
        say(f"Teller {tid} [Customer {curr_customer}]: serving a customer")     # Teller serving customer

def customer(cid):
    global curr_customer                                        # Use global variable at the top of the file
    num_ready_tellers.acquire()                                 # Take one teller from the queue if available, wait otherwise                        
    teller_queue_protected.acquire()
    tid = teller_queue.pop(0)                                   # Get the teller at the front of the queue
    teller_queue_protected.release()
    curr_customer = cid                                         # Give teller the customer ID
    say(f"Customer {cid} [Teller {tid}]: selects teller")       # Changed 0 to tid  
    say(f"Customer {cid} [Teller {tid}]: introduces itself")    # Customer introduces themself
    doorbell.release()                                          # Customer rings the doorbell to notify the teller they've arrived

threads = [threading.Thread(target=teller, args=(0,))]               # One teller for now
for i in range(NUM_CUSTOMERS):
    threads.append(threading.Thread(target=customer, args=(i,)))    # 3 customers
for t in threads:
    t.start()       # Launch threads
for t in threads:
    t.join()        # Program pauses until threads finish, then exits