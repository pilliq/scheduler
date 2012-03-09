# Scheduler

An ILOC local forward list instruction scheduler. 

## Usage
```./scheduler [options] < [ILOC program]```

### Options
```-a``` Prioritize instructions with longest latency-weighted path heuristic

```-b``` Prioritize instructions with highest latency heuristic

```-c``` Prioritize instructions with random priorities

```-o OUTPUT_FILE``` Store scheduled program in OUTPUT_FILE

```-g GRAPH_FILE``` Generate and store a GraphViz dot file of the input program's dependency graph to GRAPH_FILE
