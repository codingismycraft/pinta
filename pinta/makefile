####################################################################
# Used to build both the debug and the release versions
# of the pinta application.
#
# Assumes that the rapidjson repository is cloned under the
# ~/repos directory.
#
# To build the debug version: make debug
#  
# To build the release version: make release
# 
# To deploy to the ~/.pinta dir: make deploy
#
####################################################################

CPP=g++ -std=c++17

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

CPPFLAGS=-I$(HOME)/repos/rapidjson/include -I$(ROOT_DIR)/include
DEBUG_FLAGS=-g

SRC_DIR := $(ROOT_DIR)/src
SRC_FILES := $(wildcard $(SRC_DIR)/*.cpp)

OBJ_DEBUG_DIR := $(ROOT_DIR)/debug
OBJ_DEBUG_FILES := $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DEBUG_DIR)/%.o,$(SRC_FILES))
DEBUG_EXECUTABLE := $(OBJ_DEBUG_DIR)/pinta

debug: $(OBJ_DEBUG_FILES)
	g++ $(DEBUG_FLAGS) -o $(DEBUG_EXECUTABLE) $^

$(OBJ_DEBUG_DIR)/%.o: $(SRC_DIR)/%.cpp
	mkdir -p $(OBJ_DEBUG_DIR)
	g++ $(CPPFLAGS) $(DEBUG_FLAGS) -c -o $@ $<


OBJ_RELEASE_DIR := $(ROOT_DIR)/release
OBJ_RELEASE_FILES := $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_RELEASE_DIR)/%.o,$(SRC_FILES))
RELEASE_EXECUTABLE := $(OBJ_RELEASE_DIR)/pinta

release: $(OBJ_RELEASE_FILES)
	g++ $(RELEASE_FLAGS) -O -o $(RELEASE_EXECUTABLE) $^

$(OBJ_RELEASE_DIR)/%.o: $(SRC_DIR)/%.cpp
	mkdir -p $(OBJ_RELEASE_DIR)
	g++ $(CPPFLAGS) -c -O -o $@ $<

PINTA_HOME:= $(HOME)/.pinta
deploy: release
	echo $(HOME)
	mkdir -p $(PINTA_HOME)
	cp $(RELEASE_EXECUTABLE) $(PINTA_HOME)

clean:
	rm -rf $(OBJ_DEBUG_DIR) $(OBJ_RELEASE_DIR) 
