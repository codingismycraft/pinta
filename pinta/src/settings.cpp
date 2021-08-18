// Implements the settings class.

#include "settings.h"
#include "utils.h"
#include <iostream>

#define CONFIG_FILENAME "depender.json"

Settings::Settings()  {
    auto full_path = discover_file(CONFIG_FILENAME);
    auto settings = make_json_document_from_file(full_path);

    _project_root = settings["project_root"].GetString();
    _include_root = settings["include_root"].GetString();
    _dependencies_filename = settings["dependencies_filename"].GetString();
}

const Settings& Settings::obj() {
    static Settings the_obj;
    return the_obj;
}

STRING Settings::get_project_root() const {
    return _project_root;
}

STRING Settings::get_include_root() const {
    return _include_root;
}

STRING Settings::get_dependencies_filename() const{
    return _dependencies_filename;
}
