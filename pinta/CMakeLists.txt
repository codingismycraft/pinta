cmake_minimum_required(VERSION 3.20)
project(pinta)

set(CMAKE_CXX_STANDARD 17)
set(INCLUDE_DIR ./include)
set(RAPIDJSON_DIR /home/john/repos/rapidjson/include)

include_directories(${RAPIDJSON_DIR})
include_directories(${INCLUDE_DIR})

add_executable(pinta src/main.cpp include/utils.h src/utils.cpp include/std_include.h include/settings.h src/settings.cpp src/git_history.cpp include/pinta.h src/export_graph.cpp src/graph.cpp)

add_custom_command(TARGET pinta
        POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:pinta> /home/john/.pinta)