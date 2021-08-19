

#include "utils.h"
#include <iostream>


int main() {
    create_dag();
    auto dg = load_dependency_graph();
//    for (auto const&[key, val] : dg) {
//        std::cout << key << " ";
//        for (auto x: val) {
//            std::cout << x << ":";
//        }
//        std::cout << std::endl;
//    }

    return 0;
}
