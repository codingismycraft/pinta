// Basic utilities.
#pragma once

#include "std_include.h"

using DEPENDENCY_GRAPH = std::map<STRING, STRVEC>;

STRING current_dir();

STRVEC get_directories(CSTRREF parent_dir);

STRVEC get_python_files(CSTRREF parent_dir);

STRING full_path_to_vertex(CSTRREF fullpath);

void parse_file(CSTRREF fullpath, FILE *output);

STRING discover_file(CSTRREF filename);

rapidjson::Document make_json_document_from_file(CSTRREF filename);

void create_dag();

DEPENDENCY_GRAPH load_dependency_graph();

// String utilities.
void ltrim(STRINGREF str_to_ltrim);

STRING ltrimed(CSTRREF s);

void rtrim(STRINGREF s);

STRING rtrimed(CSTRREF s);

void trim(STRINGREF s);

STRING trimed(CSTRREF s);

// Graph utilities
void walk_dependencies(CSTRREF node, const DEPENDENCY_GRAPH& dependecies);