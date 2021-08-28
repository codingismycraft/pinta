/**
 * Implements graph related algorithms.
 */
#include "std_include.h"
#include "utils.h"

#include <set>
#include <queue>

#define BUFFER_SIZE 32000
#define DELIMETER ","

static char BUFFER[BUFFER_SIZE];

static STRVEC _get_tokens(char *buffer) {
    STRVEC v;
    auto token = strtok(buffer, DELIMETER);
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