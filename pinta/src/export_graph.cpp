/**
 * Exports the dependency graph for all the tracked python modules.
 *
 *
 * Uses the Settings class to discover the project root and the file
 * to use for the output.
 *
 */

#include "utils.h"
#include "settings.h"
#include <iostream>
#include <regex>

#define BUFFER_SIZE 32000
#define DELIMETER ","

static char BUFFER[BUFFER_SIZE];

static const std::regex rgx1("^import (.+?) as");
static const std::regex rgx2("^import ([^ ]+)\\s*\\n");

static STRING full_path_to_vertex(CSTRREF fullpath) {
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

static void parse_file(CSTRREF fullpath, FILE *output) {

    FILE *fp;
    fp = fopen(fullpath.c_str(), "r");
    assert(fp != NULL);
    STRING carryover_line;
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

void export_graph() {
    auto settings = Settings::obj();
    CSTRING output_filename = settings.get_dependencies_filename();
    FILE *f = fopen(output_filename.c_str(), "w");
    if (f == NULL) {
        std::cerr << "Error creating the output file: " << output_filename << std::endl;
        exit(1);
    }
    auto files = discover_all_python_files(settings.get_project_root());
    for (auto fn: files) {
        parse_file(fn, f);
    }
    fclose(f);
}