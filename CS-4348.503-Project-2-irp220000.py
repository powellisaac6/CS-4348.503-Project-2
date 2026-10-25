import threading

print_protected = threading.Semaphore(1)    # Avoid print mixing by using a semaphore
curr_customer = None                        # Current customer being served
doorbell = threading.Semaphore(0)           # Customer rings the doorbell to let the teller know they've arrived

def say(msg):       # Print function protected by a semaphore
    print_protected.acquire()
    print(msg)
    print_protected.release()

def teller(tid):
    say(f"Teller {tid} []: ready to serve")                                 # Teller ready
    say(f"Teller {tid} []: waiting for a customer")                         # Teller waiting
    doorbell.acquire()                                                      # Sleep until customer rings the doorbell
    say(f"Teller {tid} [Customer {curr_customer}]: serving a customer")     # Teller serving customer

def customer(cid):
    global curr_customer                                    # Use global variable at the top of the file
    curr_customer = cid                                     # Give teller the customer ID
    say(f"Customer {cid} [Teller 0]: selects teller")       # Hard coded 0 for now    
    say(f"Customer {cid} [Teller 0]: introduces itself")    # Customer introduces themself
    doorbell.release()                                      # Customer rings the doorbell to notify the teller they've arrived

threads = [threading.Thread(target=teller, args=(0,)),      # Create threads
           threading.Thread(target=customer, args=(0,))]
for t in threads:
    t.start()       # Launch threads
for t in threads:
    t.join()        # Program pauses until threads finish, then exits.