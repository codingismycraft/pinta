//
// Created by john on 28/8/21.
//

#ifndef PINTA_PINTA_H
#define PINTA_PINTA_H

#include "std_include.h"

// Creates a file with all the adjacent python modules.
void export_graph();

// Exports the whole git history for all the tracked python files.
void export_git_history();

// Loads the dependency graph from a file holding adjacent nodes.
DEPENDENCY_GRAPH load_dependency_graph(CSTRREF dependency_filename);

std::vector<std::pair<STRING, STRING>> walk_dependencies(CSTRREF node, DEPENDENCY_GRAPH &dg);

#endif //PINTA_PINTA_H
