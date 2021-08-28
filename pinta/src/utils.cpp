////////////////////////////////////////////////////////
//
// Created by john on 15/8/21.
//

#include "utils.h"
#include <unistd.h>
#include <sys/stat.h>
#include <dirent.h>
#include <iostream>
#include <regex>
#include <pwd.h>

#define BUFFER_SIZE 32000
#define DELIMETER ","

static char BUFFER[BUFFER_SIZE];

std::string get_current_dir() {
    char cwd[1028];
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        return cwd;
    } else {
        return "error..";
    }
}

void remove_dir(CSTRREF dir){

}

bool is_directory(const std::string &parent_dir, const std::string &filename) {
    if (filename == "." || filename == ".." || filename[0] == '.' || filename[0] == '_')
        return false;

    auto path = parent_dir + "/" + filename;
    struct stat statbuf;
    if (stat(path.c_str(), &statbuf) != 0)
        return false;
    return S_ISDIR(statbuf.st_mode);
}

bool ends_with(const std::string &mainStr, const std::string &toMatch) {
    if (mainStr.size() >= toMatch.size() &&
        mainStr.compare(mainStr.size() - toMatch.size(), toMatch.size(), toMatch) == 0)
        return true;
    else
        return false;
}

bool starts_with(const std::string &mainStr, const std::string &toMatch) {
    if (mainStr.size() >= toMatch.size() && mainStr.compare(0, toMatch.size(), toMatch) == 0)
        return true;
    else
        return false;
}

bool is_regular_file(const std::string &parent_dir, const std::string &filename) {
    auto path = parent_dir + "/" + filename;
    struct stat path_stat;
    stat(path.c_str(), &path_stat);
    return S_ISREG(path_stat.st_mode);
}

std::vector<std::string> get_directories(const std::string &parent_dir) {
    std::vector<std::string> directories;
    DIR *d;
    dirent *dir;
    d = opendir(parent_dir.c_str());
    if (d) {
        while ((dir = readdir(d)) != NULL) {
            if (is_directory(parent_dir, dir->d_name)) {
                directories.push_back(parent_dir + "/" + dir->d_name);
            }
        }
        closedir(d);
    }
    return directories;
}

std::vector<std::string> get_python_files(const std::string &parent_dir) {
    std::vector<std::string> python_files;
    DIR *d;
    dirent *dir;
    d = opendir(parent_dir.c_str());
    if (d) {
        while ((dir = readdir(d)) != NULL) {
            if (ends_with(dir->d_name, ".py")) {
                auto filename = parent_dir + "/" + dir->d_name;
                python_files.push_back(parent_dir + "/" + dir->d_name);
            }
        }
        closedir(d);
    }
    return python_files;
}

bool file_exists(CSTRREF dir, CSTRREF filename) {
    struct stat buffer;
    auto full_path = dir + "/" + filename;
    return stat(full_path.c_str(), &buffer) == 0;
}

bool directory_exists(STRING dir_path) {
    struct stat buffer;
    return (stat(dir_path.c_str(), &buffer) == 0);
}

STRING get_parent_dir(CSTRREF dir) {
    const std::regex e1("^\\/[^\\/]*($|\\/$)");
    const std::regex e2("\\/[^\\/]*($|\\/$)");
    if (dir.empty() || dir == "/" || dir[0] != '/')
        return "";
    else if (std::regex_match(dir, e1))
        return "/";
    else
        return std::regex_replace(dir, e2, "");
}

rapidjson::Document make_json_document_from_file(CSTRREF filename) {
    rapidjson::Document document;
    FILE *fp = fopen(filename.c_str(), "r");
    if (fp == NULL)
        throw "File: " + filename + " not found";
    std::stringstream ss;
    while (fgets(BUFFER, BUFFER_SIZE, fp))
        ss << BUFFER;
    fclose(fp);
    document.Parse(ss.str().c_str());
    return document;
}

STRVEC discover_all_python_files(CSTRREF root) {
    STRVEC filenames;
    for (const auto &dir: get_directories(root)) {
        auto files = discover_all_python_files(dir);
        filenames.insert(filenames.end(), files.begin(), files.end());
    }
    auto files = get_python_files(root);
    filenames.insert(filenames.end(), files.begin(), files.end());
    return filenames;
}

void ltrim(STRINGREF str_to_ltrim) {
    auto from_iter = str_to_ltrim.begin();
    auto to_iter = std::find_if(
            str_to_ltrim.begin(),
            str_to_ltrim.end(),
            [](unsigned char ch) {
                return !std::isspace(ch);
            }
    );
    str_to_ltrim.erase(from_iter, to_iter);
}

STRING ltrimed(CSTRREF s) {
    auto s1{s};
    ltrim(s1);
    return move(s1);
}

void rtrim(STRINGREF s) {
    auto from_iter = std::find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
        return !std::isspace(ch);
    }).base();
    auto to_iter = s.end();
    s.erase(from_iter, to_iter);
}

STRING rtrimed(CSTRREF s) {
    auto s1{s};
    rtrim(s1);
    return move(s1);
}

void trim(STRINGREF s) {
    ltrim(s);
    rtrim(s);
}

STRING trimed(CSTRREF s) {
    auto s1{s};
    trim(s1);
    return move(s1);
}

STRING get_home_dir() {
    const char *psz_homedir;
    if ((psz_homedir = getenv("HOME")) == NULL) {
        psz_homedir = getpwuid(getuid())->pw_dir;
    }
    return STRING(psz_homedir);
}
