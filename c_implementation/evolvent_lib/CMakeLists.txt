cmake_minimum_required(VERSION 3.25)
project(evolvent C)

set(CMAKE_C_STANDARD 23)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_library(evolvent SHARED library.c)
add_executable(sample sample.c)
target_link_libraries(sample evolvent)