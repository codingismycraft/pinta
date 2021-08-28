// Implements the settings class.

#include "settings.h"
#include "utils.h"
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>
#include <iostream>

#define CONFIG_FILENAME ".pinta/pinta_conf.json"

Settings::Settings()  {
    const STRING home_dir = get_home_dir();

    if(not file_exists(home_dir, CONFIG_FILENAME)){
        std::cerr << "Configuration file: " << home_dir
                  << CONFIG_FILENAME << " does not exist." << std::endl;
        exit(-1);
    }
    auto full_path = home_dir + "/" + CONFIG_FILENAME;
    auto settings = make_json_document_from_file(full_path);

    _project_root = settings["project_root"].GetString();
    _include_root = settings["include_root"].GetString();
    _dependencies_filename = settings["dependencies_filename"].GetString();
    _module_changes_filename  = settings["module_changes_filename"].GetString();
    _history_db = settings["history_db"].GetString();
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

STRING Settings::get_module_changes_filename() const{
    return _module_changes_filename;
}

STRING Settings::get_history_db() const {
    return _history_db;
}