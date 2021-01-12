# Corewars
Python implementation of CoreWars. It supports ICWS'94 standard and up to five warriors in core.
It uses Pygame for a graphical representation of the core but it can be run without gui too.
![Alt text](docs/corewars.png?raw=true "Corewars")

## Running project
1. Clone repository
1. Go to project's directory:
    ```shell script
   $ cd corewars/
   ```
1. Create and activate virtual environment:
   ```shell script
    $ python3 -m venv pve3
    $ source pve3/bin/activate    
   ```
1. Install required dependencies:
    ```shell script
   $ pip3 install -r requirements.txt
    ```
1. Run project:
    ```shell script
   $ ./corewars.py
   ```
   
## Usage
```./corewars.py [-h] [--rounds [ROUNDS]] [--core-size [CORE_SIZE]] [--max-cycles [MAX_CYCLES]] [--no-gui] [warriors [warriors ...]] ```     
**Options:**  
**warriors** : Paths to redcode files  
**-h --help** : Print help  
**--rounds** :  Number of rounds to play (Default 10)  
**--core-size** :  Size of the core (Default 8000)  
**--max-cycles** :  Cycles (executed instructions) until round will be finished as a tie (Default 80000)  
**--no-gui** : Run game without gui (print only game summary after all rounds)  

#### Examples
When no warrior files specified randomly selected 3 warriors will be loaded from `warriors/` directory:
```shell script 
$ ./corewars.py
```

Run game with two rounds between **imp** and **mice**:
```shell script 
$ ./corewars.py warriors/imp.red warriors/mice.red --rounds 2
```
Run game between **imp** and **chang1** without gui:
```shell script 
$ ./corewars.py warriors/imp.red warriors/chang1.red --no-gui
```   

## Core visualization
Initially, the entire core is initialized to grey colour (you can adjust this in colors.py).
Next warriors are loaded into core and blocks are set to solid warrior colour.
* Each time warrior executes an instruction the block will change colour to solid warrior colour.
* Each time warrior reads the block will have a circle with warrior colour.
* Each time warrior writes the block will have an "X" with warrior colour.


## Game results
If you use a GUI, you can watch warrior results during the simulation.  
Each warrior have W-L-T (Won-Lost-Tied).  
After all rounds completed a short report will be printed to console:
```
****Won-Lost-Tied after 3 round/s****
Warrior: 2-1-0
IMP: 1-2-0
```

## Creating your own warrior
To create your own warrior just write instructions to a file.  
To give warrior a name in your warrior file add the line:
```
;name <Your warrior's name>
```
Sample warrior file content (instructions are case insensitive):
```
;name IMP
mov.i #1, }0
```

## Running tests
To run test in project's root directory execute: 
   ```shell script
   $ pytest 
   ```
## License
Code released under the [MIT](https://github.com/StartBootstrap/startbootstrap-creative/blob/gh-pages/LICENSE) license.