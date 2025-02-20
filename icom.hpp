#ifndef ICOM_H
#define ICOM_H

#include <string>

#define ICOM_BLOCK 0
#define ICOM_NONBLOCK 1

namespace icom {
    const char* get_version();

    class server {
        public:
            server(int port, unsigned int length_header, unsigned int length_chunk);
            void start();
            int server_thread();
            int send(std::string s);
            int recv(char* data, unsigned int length_data);
            int recv_nonblock(char* data, unsigned int length_data);
            void wait_for_connection();
            int close();
            bool is_connected();
        private:
            unsigned int length_header;
            unsigned int length_chunk;
            int port;
            int sockfd;
            int conn;
            bool connection_status;
    };
    
    class client {
        public:
            client(std::string ip, int port, unsigned int length_header, unsigned int length_chunk);
            int connect();
            int send(std::string s);
            int recv(char* data, unsigned int length_data);
            int recv_nonblock(char* data, unsigned int length_data);
            int close();
            bool is_connected();
        private:
            std::string ip;
            unsigned int length_header;
            unsigned int length_chunk;
            int port;
            //int sock;
            int conn;
            bool connection_status;
    };
}

#endif