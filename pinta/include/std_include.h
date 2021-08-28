#pragma once

#include <cstdio>
#include <string>
#include <vector>
#include <map>
#include "rapidjson/document.h"

using STRING = std::string;
using STRINGREF = std::string&;
using CSTRING = const std::string;
using CSTRREF = const std::string&;
using STRVEC = std::vector<STRING>;
using SIZE = std::size_t;
using CSIZE = const std::size_t;
using DEPENDENCY_GRAPH = std::map<STRING, STRVEC>;