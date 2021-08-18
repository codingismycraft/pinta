// Basic utilities.
#pragma once

#include "std_include.h"

using DEPENDENCY_GRAPH=std::map<STRING, STRVEC>;

STRING current_dir();
STRVEC get_directories(CSTRREF parent_dir);
STRVEC get_python_files(CSTRREF parent_dir);
STRING full_path_to_vertex( CSTRREF fullpath);
void parse_file(CSTRREF fullpath, FILE *output);
STRING discover_file(CSTRREF  filename);
rapidjson::Document make_json_document_from_file(const std::string &filename);
void create_dag();
DEPENDENCY_GRAPH load_dependency_graph();
