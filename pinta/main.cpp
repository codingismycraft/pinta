

#include "utils.h"
#include <iostream>


int main() {
    create_dag();
    return 1;
    auto dg = load_dependency_graph();

    for (auto const&[key, val] : dg) {
        if (key == "\\") {
            std::cout << key << " ";
            for (auto x: val) {
                std::cout << key << " ";
            }
            std::cout << std::endl;
        }
    }


    return 0;
}
