#include <stdio.h>

#include"data_structs.cpp"

#define BUFF_SIZE 1024 // MAX UDP packet size is 1500 bytes
#define SERV_PORT 9999

// Define color escape codes for colorful text
#define RESET   "\033[0m"
#define BOLD    "\033[1m"
#define RED     "\033[0;31m"
#define GREEN   "\033[0;32m"
#define YELLOW  "\033[0;33m"
#define BLUE    "\033[0;34m"
#define MAGENTA "\033[0;35m"
#define CYAN    "\033[0;36m"
#define WHITE   "\033[0;37m"


int UDP_PORT[4] = {7070, 7071, 7072, 7073};
bool usedPort[4]; // to check if the port on the server is used or not

// define list of current game rooms
Room *rooms = NULL;
int playerCount = 0; // keep count of total players in the room

/*---------------------------------------------
Defining functions
-----------------------------------------------
*/

// function to find the available port of the server to use for handling client
// - output: index of port number available, -1 if there are no available ports from server
int findAvailablePort() {
    for(int i = 0; i < 4; i++){
        if(usedPort[i] == false) return i;
    }

    return -1;
}

// 
void updateListPlayer() {

}

// - function to handle case client wants to register
void sendResponse1(int clientfd){

}

// - function to handle case client wants to login
void sendResponse2(int clientfd){

}
// - function to handle case client wants to get list room
void sendResponse3(int clientfd){

}

// - function to handle case client wants to create room
void sendResponse4(int clientfd){
    

}

// - function to handle a request from client
// 
// dependencies: sendResponse1, sendResponse2, sendResponse3, sendResponse4, sendResponse5
void handleRequest(int clientfd, char buff[]) {
    int recvBytes;
    char message_type;

    // get first byte to determine which request
    if( (recvBytes = recv(clientfd, buff, 1, 0)) < 0){
        perror("Error");
    } else if(recvBytes == 0){
        fprintf(stdout, "Server closes connection\n");
        return;
    }
    message_type = buff[0];

    //
    if(message_type == '1'){
        // register request from client
        // sendResponse1(clientfd);

    } else if(message_type == '2'){
        // login request from client

    } else if(message_type == '3'){
        // get list room request from client

    } else if(message_type == '4'){
        // create room request from client
        sendResponse4(clientfd);

    } else if(message_type == '5'){
        // join room request from client

    }

    return;
}

/*---------------------------------------------
Main function to handle server logic
-----------------------------------------------
*/

int main (int argc, char *argv[]) {
    int cli_udp_port_index; // index of port from server to assign to subprocess to handle client
    pid_t pid; // test pid
    int rcvBytes, sendBytes;
    int connectfd;
    char buff[BUFF_SIZE + 1];
    struct sockaddr_in servaddr;
    struct sockaddr_in cliaddr; // list of clients addresses
    socklen_t addr_len = sizeof(struct sockaddr_in); // size of address structure, in this case size of IPv4 structure
    char cli_addr[100];
    char *result; // result string to return to client
    char errorString[10000]; // actual string return to client (used in case of error)
    char data[500]; 
    int sockfd; // sockfd for listening on TCP on general server

    //Step 1: Construct socket using SOCK_STREAM (TCP)
    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0){
        perror("Error constructing socket: ");
        return 0;
    }
    fprintf(stdout, GREEN "[+] Successfully created TCP socket\n" RESET);

    //Step 2: Bind address to socket
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET; // user IPv4
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY); // set server to accept connection from any network interface (IPv4 only)
    servaddr.sin_port = htons(SERV_PORT); // set port of the server

    if(bind(sockfd, (struct sockaddr *) &servaddr, sizeof(servaddr))){
        perror(RED "Error binding TCP socket: " RESET);
        return 0;
    }

    // Step 3: Listen for incoming connections 
    // backlog = 10 -> accept at most 10 connections at a time
    if(listen(sockfd, 10) < 0){
        perror(RED "Error listening on TCP socket" RESET);
        return 1;
    }

    printf(GREEN "[+] Server started. Listening on port: %d using SOCK_STREAM (TCP), listening socket id: %d\n" RESET, SERV_PORT, sockfd);

    //Step 4: Accept and handle client connections
    while(1){
        // ------------------------ ACCEPT NEXT CONNECTION -----------------------------
        // accept connections waiting in the queue
        // create a new file descriptor
        connectfd = accept(sockfd, (struct sockaddr *) &cliaddr, &addr_len);
        if(connectfd < 0){
            perror(RED "Error accepting new connection from new client" RESET);
            continue;
        }
        
        // reset the buff
        memset(buff, 0, sizeof(buff));

        // receive data from this connection
        if( (rcvBytes = recv(connectfd, buff, BUFF_SIZE, 0)) == -1){
            perror(RED "Error receiving data from client: " RESET);
            continue;
        }

        buff[rcvBytes] = '\0';

        // now the last character in buff is \n -> makes the string len + 1, 
        // we need to remove this character
        if(buff[strlen(buff) - 1] == '\n') buff[strlen(buff) - 1] = '\0';

        printf("Received from client: %s\n", buff);

        // handle client request
        // handleRequest(connectfd, buff);

        // print
        printf(GREEN "connected socket id: %d\n" RESET, SERV_PORT, connectfd);


    }

    return 0;
}
