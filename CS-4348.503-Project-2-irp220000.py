import threading
import random

# acquire = acquires one unit from the semaphore counter to do work, waits otherwise
# release = releases one unit to the semaphore counter, allowing other threads to do work

NUM_CUSTOMERS = 10
NUM_TELLERS = 3

print_protected = threading.Semaphore(1)                            # Avoid print mixing by using a semaphore
curr_customer = [None] * NUM_TELLERS                                # Current customer being served (one slot per teller)
curr_transaction = [None] * NUM_TELLERS

# Each teller has a doorbell
doorbells = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]    # Customer rings the doorbell to let the teller know they've arrived

asking = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
giving = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
finishing = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]
leaving = [threading.Semaphore(0) for _ in range(NUM_TELLERS)]

teller_queue = []                                   # Queue of tellers that are ready          
teller_queue_protected = threading.Semaphore(1)     # Semaphore to protect the teller queue
num_ready_tellers = threading.Semaphore(0)          # Number of tellers that are ready

cust_served = 0                                     # Total number of customers served
cust_served_protected = threading.Semaphore(1)      # Protect with semaphore
closing_time = False                                # Close the bank once all customers have been served

def say(msg):       # Print function protected by a semaphore
    print_protected.acquire()
    print(msg)
    print_protected.release()

def teller(tid):
    global cust_served, closing_time
    say(f"Teller {tid} []: ready to serve")             # Teller ready
    for _ in range(NUM_CUSTOMERS):                      # Serve a fixed number of customers
        teller_queue_protected.acquire()                                       
        teller_queue.append(tid)                        # Add teller to the queue
        teller_queue_protected.release()                # Add one teller to the queue                                        
        num_ready_tellers.release()                     # Increment the number of ready tellers
        say(f"Teller {tid} []: waiting for a customer") # Teller waiting
        doorbells[tid].acquire()                        # Sleep until customer rings the doorbell

        # Close if all customers have been served
        if closing_time:    
            return
        
        say(f"Teller {tid} [Customer {curr_customer[tid]}]: serving a customer") # Teller serving customer

        # Teller asks customer for transaction
        say(f"Teller {tid} [Customer {curr_customer[tid]}]: asks for transaction")
        asking[tid].release()

        # Wait for customer to give transaction
        giving[tid].acquire()

        # Teller handles and finishes transaction
        say(f"Teller {tid} [Customer {curr_customer[tid]}]: handling {curr_transaction[tid]} transaction")
        say(f"Teller {tid} [Customer {curr_customer[tid]}]: finishes {curr_transaction[tid]} transaction.")
        say(f"Teller {tid} [Customer {curr_customer[tid]}]: wait for customer to leave.")
        finishing[tid].release()

        # Wait for customer to leave
        leaving[tid].acquire()
        
        cust_served_protected.acquire()
        cust_served = cust_served + 1               # Increment number of customers served
        last_cust = cust_served >= NUM_CUSTOMERS    # Return true if last customer

        if last_cust:
            closing_time = True                     # Begin closing time

        cust_served_protected.release()

        if last_cust:
            for doorbell in doorbells:
                doorbell.release()                  # Wake each teller so the program can exit
            return

def customer(cid):
    num_ready_tellers.acquire()                                 # Take one teller from the queue if available, wait otherwise                        
    teller_queue_protected.acquire()
    tid = teller_queue.pop(0)                                   # Get the teller at the front of the queue
    teller_queue_protected.release()
    curr_customer[tid] = cid                                    # Give teller the customer ID
    say(f"Customer {cid} [Teller {tid}]: selects teller")       # Changed 0 to tid  
    say(f"Customer {cid} [Teller {tid}]: introduces itself")    # Customer introduces themself
    doorbells[tid].release()                                    # Customer rings the doorbell to notify the teller they've arrived

    # Wait for teller to ask for a transaction
    asking[tid].acquire()

    # Customer gives transaction
    curr_transaction[tid] = random.choice(["deposit", "withdrawal"])
    say(f"Customer {cid} [Teller {tid}]: asks for {curr_transaction[tid]} transaction")
    giving[tid].release()

    # Wait for teller to finish
    finishing[tid].acquire()

    # Customer leaves
    say(f"Customer {cid} [Teller {tid}]: leaves teller")
    leaving[tid].release()


threads = []
for i in range(NUM_TELLERS):
    threads.append(threading.Thread(target=teller, args=(i,)))      # 3 tellers
for i in range(NUM_CUSTOMERS):
    threads.append(threading.Thread(target=customer, args=(i,)))    # 3 customers
for t in threads:
    t.start()       # Launch threads
for t in threads:
    t.join()        # Program pauses until threads finish, then exits