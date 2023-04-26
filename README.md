#  Graph-based Decision Making (GDM)
[![Coverage Status](https://coveralls.io/repos/github/bi3mer/GDM/badge.svg)](https://coveralls.io/github/bi3mer/GDM)

The goal of this library is to provide and out of the box passive reinforcement learning algorithms that are easy to use. The work on your part is to define your problem as a [Graph](./GDM/Graph/Graph.py) and the library takes care of the rest. The use of a graph, rather than the classic [MDP](https://en.wikipedia.org/wiki/Markov_decision_process) formulation (`S,A,R,P`), is to provide an easy/efficient way to define MDPs where actions vary across states.

## Install

With pip:
```bash
python -m pip install git+https://github.com/bi3mer/GDM.git@main
```

With pipenv
```bash
pipenv install -e git+https://github.com/bi3mer/GDM.git@main#egg=GDM
```

## Examples

In addition to basic unit testing, [tests/](tests/) provides and tests three different grid world environments, the gambler's ruin environment, and tic-tac-toe. 
