# A Star implementation for 8-puzzle
## Make
Makefile provides a way to compile the binaries. simply type `make` at the
prompt and it will generate four targets q1,q2,q3,q4 for each heuristic type.

## Usage
Now execute a particular question by `./q1<input` where `input` is the input
file with start state.

## Data structures
The program uses cpp set for openList and closeList and cpp map for parent
generation.
Each of the heuristic is defined in its own subclass which inherits from a super
AStar module which has default heuristic h(n) = 0

## Test Run
Sample run "./q2<input"
