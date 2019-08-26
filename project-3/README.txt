# project3
Internet Technology Project 2

0. Please write down the full names and netids of all your team members.

Jerry Zhang jz570
Akash Kabra amk351

1. Briefly discuss how you implemented the challenge-response functionality and
   the authenticated DNS query.
   
   The DNS has an "authentication" feature by checking the each challenge and digest recieved from the Client. 
   Since the AS does not read/open any files, it simply passes on the challenge to TS1 and TS2, which in return
   sends back a unique digest. One of these digests will match the digest provided by the client. This is because
   both the Client and the TS servers share a key. The Client reads a file with many keys, and each TS server only has one.
   The AS does not have any key information and can only see if the digests match. If a match is found the AS sends 
   the hostname of the TS that provided the matching digest back to the client. The client then can only send the query
   to that specified hostname. Which is how the AS serves as an authenticator and tells the Client which TS to send its
   specific query to.


2. Are there known issues or functions that aren't working currently in your
   attached code? If so, explain.

   There are no known issues with this program. Just to make sure everything is working properly, we made print statements
   and made sure everything is printing out where it should be, and keeping it in our final product as well. But our final answer
   will be in RESOLVED.txt. Everything is working properly and as intented.
   There are a few lines in place to check for proper arguments, however this is assuming "good" data will be inputted.
   Sometimes, port numbers have to be changed as well if there is an address in use error.


3. What problems did you face developing code for this project?

    Some problems we faced during the development of this code was getting all the programs to connect to each other because
    there were so many programs we had to connect. Each send and recieve request had to be in the exact order, otherwise
    information gets jumbled and doesn't work as intended. It would sometimes get confusing as to when to connect what 
    to what. We also had to make sure we use the right sockets to send and receive things and in the right order.


4. What did you learn by working on this project?

    Something we learned working on this project is the timeout feature for recv calls. If something doesn't come 
    through aftera given time, it would skip it and move on to the next thing in the progrm. This was very useful 
    because any of the two TS servers can be reached by a client without knowing which one it will be. 




