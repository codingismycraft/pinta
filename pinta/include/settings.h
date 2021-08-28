#pragma once

#include "std_include.h"

class Settings {
    STRING _project_root;
    STRING _include_root;
    STRING _dependencies_filename;
    STRING _module_changes_filename;
    STRING _history_db;

    Settings();
public:
    static const Settings& obj();

    STRING get_project_root() const;
    STRING get_include_root() const;
    STRING get_dependencies_filename() const;
    STRING get_module_changes_filename() const;
    STRING get_history_db() const;
};
