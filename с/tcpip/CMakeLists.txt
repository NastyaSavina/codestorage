cmake_minimum_required(VERSION 3.15)
project(tcpip C)

set(CMAKE_C_STANDARD 99)

add_executable(tcpip server.c client.c v2/server.c v2/client.c)