import threading

print_protected = threading.Semaphore(1)    # Avoid print mixing by using a semaphore

def say(msg):       # Print function protected by a semaphore
    print_protected.acquire()
    print(msg)
    print_protected.release()

def teller(tid):
    say(f"Teller {tid} []: ready for transactions.")        # Teller ready

def customer(cid):
    say(f"Customer {cid} []: requests a transaction.")      # Customer request

threads = [threading.Thread(target=teller, args=(0,)),      # Create threads
           threading.Thread(target=customer, args=(0,))]
for t in threads:
    t.start()       # Launch threads
for t in threads:
    t.join()        # Program pauses until threads finish, then exits.