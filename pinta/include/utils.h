// Basic utilities.
#pragma once

#include "std_include.h"

STRING get_current_dir();

STRING get_home_dir();

STRVEC get_directories(CSTRREF parent_dir);

STRVEC get_python_files(CSTRREF parent_dir);

STRVEC discover_all_python_files(CSTRREF root);

bool file_exists(CSTRREF dir, CSTRREF filename);

rapidjson::Document make_json_document_from_file(CSTRREF filename);

// String utilities.
void ltrim(STRINGREF str_to_ltrim);

STRING ltrimed(CSTRREF s);

void rtrim(STRINGREF s);

STRING rtrimed(CSTRREF s);

void trim(STRINGREF s);

STRING trimed(CSTRREF s);

bool starts_with(const std::string &mainStr, const std::string &toMatch);

bool ends_with(const std::string &mainStr, const std::string &toMatch);
