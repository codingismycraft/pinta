#include "pinta.h"
#include "utils.h"
#include "settings.h"
#include <iostream>
#include <ctime>
#include <regex>


int main(int argc, char *argv[]) {
    if (argc == 1) {
        clock_t begin = clock();
        export_graph();
        clock_t end = clock();
        double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
        std::cout << elapsed_secs << std::endl;
    } else if (argc >= 2 && STRING(argv[1]) == "-d") {
        export_git_history();
    } else {
        printf("Unknown argument: %s\n", argv[1]);
        exit(-1);
    }
    return 0;


//    clock_t begin = clock();
//    auto dg = load_dependency_graph(Settings::obj().get_dependencies_filename());
//    auto edges1 = walk_dependencies("pants.libs.rapidlib.orion.decorators", dg);
//    clock_t end = clock();
//    double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
//    std::cout << elapsed_secs << std::endl;
    return 0;
}
