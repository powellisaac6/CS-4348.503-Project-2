# 10-25-2026 11:45 PM
These are my initial thoughts.
The project seems to simulate a bank.
The bank opens when 3 tellers are ready.
Customers show up at random times. 
If a teller is available to handle a customer's transaction, it does so right away.
If not, the customer must wait in line.
The customer can either deposit or withdraw.
Each transaction takes some amount of time in ms.
The teller informs the customer the transaction has been completed and the customer leaves.
The teller calls the next customer.
Once 50 customers have been served, the bank closes.

This project is meant to practice semaphores.
Since the customers and the tellers are threads, we can make something like the door as a semaphore only allowing 2 customers in the bank at a time.
Other shared resources like the manager and the safe could also be modeled as such.

I plan to break this project into small steps.
First I'll focus on the customer-teller communication logic.
After that, I'll add logic for the manager.
Then the safe, then the door.
I haven't really thought about how the customer will find a free teller yet, but I'll figure that out as I go in my first session.

NOTE: I'm planning on changing how I do the devlog for this project.
For each session, I'll do an opening entry before coding and a closing entry after coding. 
That way I can maintain a continuous flow instead of having to split my attention between coding and writing. 
My timestamps will reflect when I started the entry, not when I committed it.

# 10-25-2026 12:09 PM
My goals for the first session:

1. Threads launch.
2. Customers introduce themselves to the tellers.
3. Program ends smoothly.

I'll write a teller function and a customer function first.
I need to make sure it prints in the correct format (EX: Customer 10 [Teller 0]: message).
I'll start off with one customer meeting one teller.
After that works, I'll scale up to several.
I'm thinking about using a queue for the tellers.
Each teller will have a unique ID.
When that teller is ready, it will add its ID to a shared queue.
The customer will pick the ID at the front of the queue.
I'll protect the queue with a semaphore since it's a shared resource.
I'll have the program stop after 3 customers have been helped for now.

# 10-25-2026 2:33 PM
I finished all three goals for the session.
My first commit, I created a basic implementation for the threads then exited the program cleanly.
I also protected the print function with a semaphore using the say function.
My second commit, I implemented the doorbell semaphore which allowed the customer to notify the teller when they had arrived to the bank.
My third and final commit, I implemented the teller queue which a teller would join when they were ready to handle a customer's transaction.
The last commit also included the handling of several customers.

I had a few errors during my last commit.
I forgot a bracket at the end of a line which led to a few minutes of troubleshooting.
Overall, it wasn't too hard to fix with debugging.
Not too much of an error, but I forgot I was going to change each say(f"Customer {cid} [Teller 0]: message") line from a static Teller 0 to a dynamic Teller {tid}.
I just double checked my code before committing and noticed that. 
Doesn't necessarily change the output but I wanted to make sure that was fixed for next session.

This session helped me understand how semaphores work better now that I've actually used them firsthand. 
Each time a shared resource is used, the thread using it takes one unit from the semaphore counter if it is available.
Otherwise, it waits.
Then when the thread is done, it adds one unit back to the semaphore counter.
This seems useful for future projects where resource management is essential.

My code is rather simple right now since only one teller is handling multiple customers.
Next session, I'm going to focus on multiple teller handling.
Each teller will need a cid slot and its own doorbell most likely.
A fixed loop will probably not work next time since the work will be divided among tellers, so I will also need to develop a solution for that.