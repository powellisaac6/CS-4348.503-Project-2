# 10-25-2026 11:45 AM
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

# 10-26-2026 4:08 PM
Right now my code only works for 1 teller.
For this session I want to launch 3 tellers.
3 tellers will not work with my current implementation.
A new instance of curr_customer could replace the current one.
So, I think curr_customer would be better as a list.
Also, the wrong teller could wake if only a single doorbell is used.
Doorbells would probably also be better as a list.

The fixed loop won't work anymore because a single teller may not reach the number of people needing to be served.
Therefore, I will need some kind of logic for the tellers to determine when to quit.
A shared counter protected by a semaphore would be a good solution.
That way each teller can view and update the total number of people that have been served.
After the last customer has been served, the tellers that are still asleep will have to wake up so the program can exit.
I have yet to figure out how I will approach that.
I will have to see what works best when I'm coding.

I'll test with 3 customers first, then 10.
To ensure it runs properly, I'll make sure to run it several times.

# 10-26-2026 7:30 PM
This one took me a bit longer than expected.
I started right before class so I was only able to get about 30 minutes of focused time before quitting.
I ended up staying at the school after class to finish my work.

I implemented as planned.
Both the doorbell and curr_customer variables were turned into lists.
I found a solution for waking the tellers after the last customer has been served.
Basically the teller that serves the last customer sets the closing_time variable to true.
This teller then rings the doorbells of all of the other tellers so they can wake up.

There were two issues during this session.
I forgot to make global variables for cust_served and closing_time in the teller function.
This led to an UnboundLocalError which caused about 10 minutes of troubleshooting.
I eventually figured out how to handle it after doing some google searches on the error.

I also forgot to add [tid] on the "serving a customer" line which caused the whole list of customers to print out on one line instead of individually.

I tested with 3 customers, then 10 as I said I would.
Works as intended.

Next session, I'll work on fully implementing the handshake between customer and teller.

# 10-27-2026 11:34 AM
For this session, I want to work on the actual customer-teller transaction.
The teller will ask the customer which transaction they want.
Then, the customer will randomly give the teller either a withdrawal or deposit transaction.
The teller will tell the customer when done.
Lastly, the teller will mark itself available after the customer leaves.

Right now the teller goes back to the teller queue straight after introducing itself.
If I continue with this logic, a customer could be sent to a busy teller.
That is not what I want.
So, I will need to change the logic so the teller returns to the queue after the customer leaves.

I also think I need to make a list of semaphores for each object's action since they'll be shared.
For instance, a teller will ask the customer what their transaction is.
So, each teller will get its own asking semaphore and share it with the current customer.
A list tracking each teller's current transaction type should be implemented as well.

I'm not quite sure how many action semaphores I'll need.
I'll start with the asking one mentioned earlier.

Again I'll test with 3 customers first, then 10, and run it multiple times to ensure it's working properly.

# 10-27-2026 1:31 PM
Everything I planned for this session is complete.
I created 4 action lists:

- Asking: Teller asks customer for transaction.
- Giving: Customer gives teller transaction.
- Finishing: Teller handles and finishes transaction.
- Leaving: Customer leaves.

Each list has an entry per teller.

I also added a list for the type of transaction each teller is currently working on (curr_transaction).

The logic to add a ready teller back to the queue was already at the beginning of the teller loop, so I ended up just adding the transaction logic after.
This way a teller will only rejoin the queue after the customer leaves.

The only real issue I ran into was that I forgot to put "import random" at the start of my code but that was a simple fix.

I tested with 3 customers, then 10, and ran it multiple times.
Everything works as intended.

Next session I plan to work on the manager and safe.

# 10-27-2026 5:25 PM
Decided to begin another session today.
I'm going to work on the manager and safe.
The safe will process every transaction, while the manager will approve withdrawals.
Only 2 tellers can access the safe at a time and only one teller can access the manager at a time.
So, I'll do semaphore(2) for the safe and semaphore(1) for the manager.

For withdrawals, I think I'll have the teller release the manager before acquiring the safe.
The idea is to avoid prolonged resource hogging from a single teller.

I also need to add the random durations of sleeping for the manager and safe.
I'm not too sure how to program this since I haven't really experimented with timers in python before. 
I assume that there's a library that I can combine with random to implement this.

I'll test with 3 customers first, then 10 and 50, and run it multiple times to ensure it's working properly.
I also need to make sure that there aren't more than two tellers using the safe at a time.