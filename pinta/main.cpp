#include "utils.h"
#include "settings.h"
#include <iostream>
#include <ctime>


int main() {
    {
        clock_t begin = clock();
        create_dag();
        clock_t end = clock();
        double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
        std::cout << elapsed_secs << std::endl;
    }
    clock_t begin = clock();
    auto dg = load_dependency_graph(Settings::obj().get_dependencies_filename());
    auto edges1 = walk_dependencies("pants.libs.rapidlib.orion.decorators", dg);
    clock_t end = clock();
    double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
    std::cout << elapsed_secs << std::endl;
    return 0;
}
