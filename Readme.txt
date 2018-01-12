The proxy server takes 1 or 2 arguments but a minimum of 1 argument which is the port on which the proxy runs on.
We need to set the proxy settings in the browser as well to send requests to 1037.
When the program is run, the proxy creates a socket on specified port and binds it. Once done, it prints proxy running on port followed by port number. At this point, the proxy waits on acpeting requests. Multithreading is implemented here.
Everytime a request is recieved, the proxy checks for http1.0 and get request.
If the conditions are satisfied, the server checks in the blocked.txt if it need to block the request. If it is a blocked site, the proxy blocks the site and doesnt forward the request to the server.
If any of the conditions are not satisfied, the proxy sends an error code to the client browser.
If all the conditions are satisfied, the proxy calls the server proxy class along with the server address read from the request and the port. If no port is given, it is set to port 80. 
The server first sets the port number and address and then calls the check proxy class.
Here, the proxy checks the cache and finds if the webpage is alreay cached.
If the webpage is cached, the proxy retrives information from the file and sends its to the client.
In case the webpage is not cached, the proxy calls the create_socket function. This function opens a server socket and connects to the server using the serveraddress and port.
After connecting to the server, the proxy modifies the request and adds another line to request sent by client. This line added is cache-control. This is either set to private or public depending on the sites mentioned in the private.txt file. 
After this, the proxy creates the folder for each website and file for each file requested. If the name of the file is not given, it is set as index file. This is usually the main page file.
The request is then forwarded to the server. The server then responds to the request and this data is first checked if it contains anything related to pokemon and sends it to the browser if it doesnt contain anything related to pokemon. After sending, this data is written into the file created before.
The file and data are only written if the cache-control mentioned before is set to public. 
All of the coding is done using classes.Tried decoding the file after reading or decoding the data after recieving from the server but was giving errors.