# Pinta

Analyzes a python code base creating the dependency graph.

Parses all the python files under a specific directory, discovers
the dependencies among them and saves them for further processing.

# Configuration

The program settings are specified in a json file which holds the
root directory of the project to scan and also the default prefix
of the import files.

The location of the configuration file is :

```
~/.pinta/pinta_conf.json
```

While its content should be:

```
    {
        "project_root": "...",
        "include_root": "...",
        "dependencies_filename": "...",
        "module_changes_filename": "...",
        "history_db": "..."
    }
```


# Dependencies

You need to have flask installed and also you need to clone the
following repo:

```
git clone git@github.com:Tencent/rapidjson.git
```

# Build
You can build the executable from CLion (prefer the Release version)

To prepare the database with the Git changes you should call the pinta
executable passing the -d argument.



