![Pinta](https://m.media-amazon.com/images/I/51-Mw9LCK-L._AC_SX466_.jpg)

La Pinta (Spanish for The Painted One, The Look, or The Spotted One) was the fastest of the three Spanish ships used by Christopher Columbus in his first transatlantic voyage in 1492.

The name parallelism lies in the nature of the software that is implemented here; in the same way that Pinta was used to discover the new land the application developed here attempts to discover hidden information and relationships within the territory of a large scale python project having a complicated dependency tree.

# Description
Discovers and displays python module dependencies.


# Requirements

You need to have the following installed on your system:

### git
```
john@john-desktop:~$ git --version
git version 2.34.1
```


### g++
```
john@john-desktop:~$ g++ --version
g++ (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

### cmake
```
john@john-desktop:~$ cmake --version
cmake version 3.22.1

CMake suite maintained and supported by Kitware (kitware.com/cmake).
```

### python
```
john@john-desktop:~$ python3 --version
Python 3.10.12
```

### pip
```
john@john-desktop:~$ pip3 --version
pip 22.0.2 from /usr/lib/python3/dist-packages/pip (python 3.10)
```


# Installation

### Clone the code from github

```
cd <your-repos-home>
git clone https://github.com/codingismycraft/pinta.git
git clone https://github.com/Tencent/rapidjson.git
```

### Create the configuration file

```
cd ~
mkdir .pinta
cd .pinta
touch pinta_conf.json
```

Add the following content in the `pinta_conf.json` file:

```
{
        "project_root": "<path-to-project-root>/<top-dir>",
        "include_root": "<path-to-project-root>",
        "dependencies_filename": "<your-home-directory>/.pinta/deps"
        "module_changes_filename": "<home-dir>/.pinta/module_changes.csv",
        "history_db": "<home-dir>/.pinta/history.db"
}
```

### Build pinta executable

Build the `pinta` executable (is parsing the python code base and creates the
dependency graph).

```
cd <your-repos-home>/pinta/pinta
mkdir temp
cd temp
cmake .. -DCMAKE_BUILD_TYPE=Release
make
cp pinta <home-dir>/.pinta
cd ..
rm -rf temp
```

### Starting the pinta server

To start the server "by hand" you can follow these:

```
cs <your-repos-home>/pinta/server
python3.10 app.py
```

which will start the pinta service on port 5555

```
john@john-desktop:~/.../pinta/server$ python3.10 app.py 
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://localhost:5555
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 152-597-082
```

At this point you have a working server that can receive the full path to the
python file you want to check and reply with an HTML page displaying the full
dependency graph.


