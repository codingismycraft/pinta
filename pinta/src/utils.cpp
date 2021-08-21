////////////////////////////////////////////////////////
//
// Created by john on 15/8/21.
//

#include "utils.h"
#include "settings.h"
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <iostream>
#include <regex>
#include <iterator>
#include <cstdio>
#include <cstdlib>
#include <assert.h>
#include <sys/stat.h>
#include <stdbool.h>
#include <set>
#include <queue>
#include <pwd.h>

#define BUFFER_SIZE 32000
#define DELIMETER ","

static char BUFFER[BUFFER_SIZE];

std::string current_dir() {
    char cwd[1028];
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        return cwd;
    } else {
        return "error..";
    }
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


STRING full_path_to_vertex(CSTRREF fullpath) {
    const std::regex e(Settings::obj().get_include_root());
    auto vertex = std::regex_replace(fullpath, e, "");
    const std::regex separator("/");
    vertex = std::regex_replace(vertex, separator, ".");
    const std::regex starting_separator("^.");
    vertex = std::regex_replace(vertex, starting_separator, "");
    const std::regex python_extension(".py");
    vertex = std::regex_replace(vertex, python_extension, "");
    return vertex;
}


std::regex rgx1("^import (.+?) as");
std::regex rgx2("^import ([^ ]+)\\s*\\n");


void parse_file(CSTRREF fullpath, FILE *output) {
    FILE *fp;
    fp = fopen(fullpath.c_str(), "r");
    assert(fp != NULL);
    STRING carryover_line = "";
    std::regex ends_with_continuation(R"(.*\\\n)");

    while (fgets(BUFFER, BUFFER_SIZE, fp)) {
        std::string s(BUFFER);
        ltrim(s);
        if(s.empty() || s[0] == '#')
            continue;
        if(s[0] != 'i' && carryover_line.empty())
            continue;

        if (std::regex_match(s, ends_with_continuation)) {
            s.erase(s.end() - 2, s.end());
            carryover_line += s;
            continue;
        }

        CSTRING full_line = carryover_line + s;
        carryover_line= "";
        std::smatch match;
        if (std::regex_search(full_line.begin(), full_line.end(), match, rgx1) ||
            std::regex_search(full_line.begin(), full_line.end(), match, rgx2)) {
            auto node1 = STRING (match[1]);
            if (node1[node1.size()-1] == '\r'){
                node1 = node1.substr(0, node1.size()-1);
            }
            fprintf(output, "%s, %s\n", node1.c_str(), full_path_to_vertex(fullpath).c_str());
        }
    }
    fclose(fp);
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

/**
    Returns the parent directory of the passed-in directory.

    Currently only works for linux file paths.

    @param dir The directory to get its parent.
    @param parent_dir It will receive the parent directory.

    @return Not zero on success.
*/
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

STRING _discover_file(CSTRREF dir, CSTRREF filename) {
    if (!directory_exists(dir.c_str()) || dir.empty()) {
        return "";
    } else if (file_exists(dir, filename)) {
        return dir + "/" + filename;
    } else {
        auto parent_dir = get_parent_dir(dir);
        if (!parent_dir.empty())
            return _discover_file(parent_dir, filename);
        else
            return "";

    }
}

STRING discover_file(CSTRREF filename) {
    return _discover_file(current_dir(), filename);
}

/// Creates a Document object holding the json data in the passed in file

/// @param filename The file name containing the json document.
/// @return A rapidjson Document object.
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


void create_dag() {
    auto settings = Settings::obj();
    CSTRING output_filename = settings.get_dependencies_filename();
    FILE *f = fopen(output_filename.c_str(), "w");
    if (f == NULL) {
        std::cerr << "Error creating the output file: " << output_filename << std::endl;
        exit(1);
    }
    fprintf(f, "node1, node2\n");
    auto files = discover_all_python_files(settings.get_project_root());
    int i = 0;
    for (auto fn: files) {
        ++i;
        parse_file(fn, f);
    }
    fclose(f);
}

STRVEC _get_tokens(char *buffer) {
    STRVEC v;
    auto token = strtok(BUFFER, DELIMETER);
    while (token) {
        STRING strg(token);
        if (!strg.empty() && strg[strg.length() - 1] == '\n') {
            strg.erase(strg.length() - 1);
        }
        v.push_back(strg);
        token = strtok(NULL, DELIMETER);
    }
    return move(v);
}

DEPENDENCY_GRAPH load_dependency_graph(CSTRREF dependency_filename) {
    DEPENDENCY_GRAPH graph;
    FILE *fp = fopen(dependency_filename.c_str(), "r");
    while (fgets(BUFFER, BUFFER_SIZE, fp)) {
        auto tokens = _get_tokens(BUFFER);
        if (tokens.size() >= 2) {
            auto node_1 = trimed(tokens[0]);
            auto node_2 = trimed(tokens[1]);

            if (graph.find(node_1) == graph.end()) {
                graph[node_1] = STRVEC();
            }
            if (graph.find(node_2) == graph.end()) {
                graph[node_2] = STRVEC();
            }

            graph[node_1].push_back(node_2);
        }
    }
    return move(graph);
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

void trim(STRINGREF s){
    ltrim(s);
    rtrim(s);
}

STRING trimed(CSTRREF s) {
    auto s1{s};
    trim(s1);
    return move(s1);
}


std::vector<std::pair<STRING, STRING>> walk_dependencies(CSTRREF node, DEPENDENCY_GRAPH& dg){
    std::set<STRING> visited;
    std::queue<STRING> node_queue;
    std::vector<std::pair<STRING, STRING>> edges;

    if(!dg.count(node)){
        return edges;
    }

    node_queue.emplace(node);
    visited.emplace(node);

    while (!node_queue.empty()){
        auto current_node = node_queue.front();
        node_queue.pop();
        for(auto child: dg[current_node]){
            if (visited.find(child) == visited.end()){
                auto edge = std::make_pair(current_node, child);
                edges.push_back(edge);
                node_queue.emplace(child);
            }
        }
        visited.emplace(current_node);
    }

    return edges;
}

STRING get_home_dir(){
    const char *psz_homedir;
    if ((psz_homedir = getenv("HOME")) == NULL) {
        psz_homedir = getpwuid(getuid())->pw_dir;
    }
    return STRING (psz_homedir);
}
