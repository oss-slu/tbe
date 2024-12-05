# Specify the minimum version for CMake
cmake_minimum_required(VERSION 3.10)

# Define the project name
project(tbe_c)

# Add the executable and its source files
add_executable(main
    ../src/main.c
    ../src/functions/isolate_header.c
    ../src/functions/output_TBE.c
)

target_include_directories(main PRIVATE ../include/)