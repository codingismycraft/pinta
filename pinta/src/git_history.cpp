/**
 * Exports the whole git history.
 *
 * For each module that can be discovered in the working directory, we
 * report all of its changes and store them in a text file in a comma
 * delimited format.
 *
 * Uses the Settings class to discover the project root and the file
 * to use for the output.
 *
 */

#include "utils.h"
#include "settings.h"
#include <iostream>
#include <ctime>
#include <regex>
#include <map>
#include <iostream>


static char BUFFER[10000];

static char DATE_BUFFER[128];

static std::map<STRING, int> MONTH_MAP = {
        {"Jan", 1},
        {"Feb", 2},
        {"Mar", 3},
        {"Apr", 4},
        {"May", 5},
        {"Jun", 6},
        {"Jul", 7},
        {"Aug", 8},
        {"Sep", 9},
        {"Oct", 10},
        {"Nov", 11},
        {"Dec", 12},
};


static STRING parse_date(CSTRREF date) {
    // date passed as Thu Oct 22 15:37:02 2020
    // construct a stream from the string
    std::stringstream ss(date);
    std::string s;
    const char delimiter = ' ';
    std::vector<STRING> tokens;
    while (std::getline(ss, s, delimiter)) {
        tokens.push_back(s);
    }
    auto month = MONTH_MAP[tokens[1]];
    auto day = atoi(tokens[2].c_str());
    auto year = atoi(tokens[4].c_str());
    sprintf(DATE_BUFFER, "%d%02d%02d", year, month, day);
    return DATE_BUFFER;
}

static inline std::pair<STRING, STRING> split_full_path(CSTRREF full_path) {
    CSIZE index = full_path.find_last_of("/\\");
    return {full_path.substr(0, index), full_path.substr(index + 1)};
}

const std::regex rgx1("Author: (.+?) ");
const std::regex rgx2("Date:\\s+(.+) .+");


static void parse_git_log(CSTRREF full_path, FILE *fp_output) {

    const auto split = split_full_path(full_path);
    const auto dir = split.first;
    const auto filename = split.second;
    const auto command = "cd " + dir + "; git log " + filename;

    FILE *fp = popen(command.c_str(), "r");
    if (fp == NULL) {
        printf("Failed to execute: %s\n,", command.c_str());
        exit(-1);
    }

    std::smatch match;

    while (fgets(BUFFER, sizeof(BUFFER), fp) != NULL) {
        CSTRING line = {BUFFER};

        if (std::regex_search(line.begin(), line.end(), match, rgx1)) {
            fprintf(fp_output, "%s,%s,", full_path.c_str(), STRING(match[1]).c_str());
        } else if (std::regex_search(line.begin(), line.end(), match, rgx2)) {
            fprintf(fp_output, "%s\n", parse_date(match[1]).c_str());
        }
    }
    pclose(fp);
}

void create_sqlite_db() {
    // sqlite3 junk.db ".import module_changes.csv history"
    auto settings = Settings::obj();
    auto cmd = "rm " + settings.get_history_db();
    system(cmd.c_str());
    cmd = "sqlite3 " + settings.get_history_db() + " \"create table history (name text, author text, date text);\"";
    system(cmd.c_str());
    cmd = "sqlite3 " + settings.get_history_db() + " -separator ',' " +
            " \'.import " + settings.get_module_changes_filename() + " history\'";
    std::cout << cmd << std::endl;
    system(cmd.c_str());
}

void export_git_history() {
    auto settings = Settings::obj();
    auto files = discover_all_python_files(settings.get_project_root());
    FILE *fp = fopen(settings.get_module_changes_filename().c_str(), "w");
    if (fp == NULL) {
        std::cerr << "Error creating the output file: " << settings.get_module_changes_filename() << std::endl;
        exit(-1);
    }
    int i = 0;
    for (CSTRREF full_path: files) {
        std::cout << ++i << std::endl;
        parse_git_log(full_path, fp);
    }
    fclose(fp);
    fp = NULL;
    create_sqlite_db();
}
