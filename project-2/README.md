# project2
Internet Technology Project 2

0. Please write down the full names and netids of all your team members.

Akash Kabra amk351

Jerry Zhang jz570

1. Briefly discuss how you implemented your recursive root and TLD server
   functionality.
   
Our basic TLD server utilizes a client side program, a root server, and two top-level servers, one for handling .edu and one for handling .com domain names. The root server is recursive by taking requests one by one from the client side. If the hostname matches an entry in the RS table, then host is found and the respective information is sent back to the client. If the hostname is not found in the RS table, then it looks for the last 4 letters of the hostname and sends it to either TS_EDU or TS_COM depending on which server might have the necessary details. Once in one of the TS server, it looks through its data and sends back it's respective information. If still not found, the TS simply returns a HOST NOT FOUND message for the RS to relay back to the client. 

2. Are there known issues or functions that aren't working currently in your
   attached code? If so, explain.

The programs are currently working as expected. 

3. What problems did you face developing code for this project?

Some of the challenges faced were finding a way for the root server to handle two listen ports at a time. We had to find a way to parse the domain and see if it ended in edu or com to send to the appropriate TS socket. The com and edu TS programs were edited to handle their respective domains. Also, at first it was a little difficult to make sure everything is sent to the right server depending on what the host was.

4. What did you learn by working on this project?

After implementing just two different TLD servers, we've realized just how massive the internet can be. On the client side, when users input a website domain, it gets sent to the root server. The only responsibility of the root server is to connect with the .com or .edu name servers to find information about the domain, and return that information to the client. In order for the root server to process multiple requests for example google searches it has to be efficient in bridging the client with the top-level domain server.
