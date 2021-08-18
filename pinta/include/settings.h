#pragma once

#include "std_include.h"

class Settings {
    STRING _project_root;
    STRING _include_root;
    STRING _dependencies_filename;

    Settings();
public:
    static const Settings& obj();

    STRING get_project_root() const;
    STRING get_include_root() const;
    STRING get_dependencies_filename() const;
};
