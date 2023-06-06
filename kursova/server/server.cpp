#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>
#include <cstring>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

// Structure for storing note information
class Note {
public:
    std::string title;
    std::string content;

    Note(std::string title, std::string content) {
        this->title = title;
        this->content = content;
    }
};

// Structure for storing user information
class User {
public:
    std::string username;
    std::string password;
    std::vector<Note> notes{};

    User(std::string username, std::string password) {
        this->username = username;
        this->password = password;
    }
};

// Database to store users and their notes
std::map<std::string, User> users;

bool doesUserContainNoteWithTitle(User user, std::string noteTitle) {
    for (const auto& note : user.notes) {
        if (note.title == noteTitle)
            return true;
    }
    return false;
}

// Function to handle client requests
void handleClientRequest(SOCKET clientSocket) {
    char buffer[1024];
    memset(buffer, 0, sizeof(buffer));

    // Receive client message
    int bytesRead = recv(clientSocket, buffer, sizeof(buffer) - 1, 0);
    if (bytesRead == SOCKET_ERROR) {
        perror("Error in recv");
        return;
    }

    std::string request(buffer);

    // Parse the client request
    std::istringstream iss(request);
    std::string command;
    iss >> command;

    if (command == "register") {

        std::string username, password;
        iss >> username >> password;

        // Check if the username is already taken
        if (users.find(username) == users.end()) {
            User newUser(username, password);

            users.insert(std::make_pair(username, newUser));

            // Send registration success message to the client
            std::string response = "Registration was successful!";
            send(clientSocket, response.c_str(), response.length(), 0);
        }
        else {
            // Send registration failure message to the client
            std::string response = "Username already taken!";
            send(clientSocket, response.c_str(), response.length(), 0);
        }
    }

    else if (command == "login") {

        std::string username, password;
        iss >> username >> password;

        auto it = users.find(username);
        if (it != users.end() && it->second.password == password) {
            // Send login success message to the client
            std::string response = "Login was successful!";
            send(clientSocket, response.c_str(), response.length(), 0);
        }
        else {
            std::string response = "Incorrect login or password!";
            send(clientSocket, response.c_str(), response.length(), 0);
        }
    }

    else if (command == "view_notes") {
        std::string username, password;
        iss >> username >> password;

        // Check if the username and password are correct
        auto it = users.find(username);
        if (it != users.end() && it->second.password == password) {
            User& user = it->second;

            // Construct a response with all notes
            std::string response;
            for (const auto& note : user.notes) {
                response += note.title + "\n";
                std::cout << note.title << std::endl;
            }

            // Send the response to the client
            send(clientSocket, response.c_str(), response.length(), 0);
        }
        else {
            // Send authentication failure message to the client
            std::string response = "Invalid username or password!";
            send(clientSocket, response.c_str(), response.length(), 0);
        }
    }

    else if (command == "add_note") {
        std::string username, password, noteTitle, noteContent;
        iss >> username >> password >> noteTitle;
        std::getline(iss, noteContent);

        auto it = users.find(username);
        if (it != users.end() && it->second.password == password) {
            User& user = it->second;

            if (!doesUserContainNoteWithTitle(user, noteTitle)) {
                user.notes.push_back(Note(noteTitle, noteContent));

                std::string response = "Note was successfully added!";
                send(clientSocket, response.c_str(), response.length(), 0);
            }
            else {
                std::string response = "Note with that title already exists";
                send(clientSocket, response.c_str(), response.length(), 0);
            }
        }
    }

    else if (command == "delete_note") {
        std::string username, password, noteTitle;
        iss >> username >> password >> noteTitle;

        auto it = users.find(username);
        if (it != users.end() && it->second.password == password) {
            User& user = it->second;

            if (doesUserContainNoteWithTitle(user, noteTitle)) {
                auto note = std::find_if(user.notes.begin(), user.notes.end(), 
                    [noteTitle](const Note& note) {
                    return note.title == noteTitle;
                    });

                if (note != user.notes.end()) {
                    user.notes.erase(note);
                    std::string response = "Note was successfully deleted!";
                    send(clientSocket, response.c_str(), response.length(), 0);
                }
                
                else{
                    std::string response = "Smth went wrong";
                    send(clientSocket, response.c_str(), response.length(), 0);
                }
            }
            else {
                std::string response = "Smth went wrong";
                send(clientSocket, response.c_str(), response.length(), 0);
            }
        }
    }

    else if (command == "view_note_content") {
        std::string username, password, noteTitle;
        iss >> username >> password >> noteTitle;

        auto it = users.find(username);
        if (it != users.end() && it->second.password == password) {
            User& user = it->second;

            if (doesUserContainNoteWithTitle(user, noteTitle)) {
                auto note = std::find_if(user.notes.begin(), user.notes.end(),
                    [noteTitle](const Note& note) {
                        return note.title == noteTitle;
                    });

                std::string response = "";
                if (note != user.notes.end())
                    response = note->content;
                
                send(clientSocket, response.c_str(), response.length(), 0);
            }
        }
    }

    else if (command == "save_note_content") {
        std::string username, password, noteTitle, noteContent;
        iss >> username >> password >> noteTitle;

        std::stringstream ss;
        std::string line;

        while (std::getline(iss, line)) {
            // Append each line to the stringstream
            ss << line << '\n';
        }

        noteContent = ss.str();

        std::cout << noteContent;

        auto it = users.find(username);
        if (it != users.end() && it->second.password == password) {
            User& user = it->second;

            if (doesUserContainNoteWithTitle(user, noteTitle)) {
                auto noteIt = std::find_if(user.notes.begin(), user.notes.end(),
                    [&](const Note& note) { return note.title == noteTitle; });

                if (noteIt != user.notes.end()) {
                    Note& note = *noteIt;
                    note.content = noteContent;

                    std::string response = "Note was successfully edited!";
                    send(clientSocket, response.c_str(), response.length(), 0);
                }

                else {
                    std::string response = "Smth went wrong";
                    send(clientSocket, response.c_str(), response.length(), 0);
                }
            }
            else {
                std::string response = "Smth went wrong";
                send(clientSocket, response.c_str(), response.length(), 0);
            }
        }
    }

    else {
        // Send invalid command message to the client
        std::string response = "Invalid command!";
        send(clientSocket, response.c_str(), response.length(), 0);
    }

    closesocket(clientSocket);
}

int main() {
    // Initialize Winsock
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cout << "Failed to initialize Winsock.\n";
        return 1;
    }

    // Create a TCP socket
    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == INVALID_SOCKET) {
        std::cout << "Failed to create socket.\n";
        WSACleanup();
        return 1;
    }

    // Bind the socket to a specific address and port
    sockaddr_in serverAddress{};
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_port = htons(1234);
    serverAddress.sin_addr.s_addr = INADDR_ANY;

    if (bind(serverSocket, reinterpret_cast<sockaddr*>(&serverAddress), sizeof(serverAddress)) == SOCKET_ERROR) {
        std::cout << "Failed to bind socket.\n";
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    // Listen for client connections
    if (listen(serverSocket, 5) == SOCKET_ERROR) {
        std::cout << "Failed to listen on socket.\n";
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    std::cout << "Server started. Listening for connections..." << std::endl;

    while (true) {
        // Accept a client connection
        sockaddr_in clientAddress{};
        int clientAddressSize = sizeof(clientAddress);
        SOCKET clientSocket = accept(serverSocket, reinterpret_cast<sockaddr*>(&clientAddress), &clientAddressSize);
        if (clientSocket == INVALID_SOCKET) {
            std::cout << "Failed to accept client connection.\n";
            continue;
        }

        // Handle client request in a separate thread or process
        handleClientRequest(clientSocket);
    }

    // Close the server socket
    closesocket(serverSocket);

    // Cleanup Winsock
    WSACleanup();

    return 0;
}
