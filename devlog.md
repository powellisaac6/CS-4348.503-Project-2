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