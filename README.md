# utils

## Introduction

This is a small collection of utilities authored by
[@joseph-zhong](https://github.com/joseph-zhong), for the purpose of making
Python modules and scripts more fun and simpler to write and work with.

In particular, `cmd_line.py` parses the arguments of a given function, and uses
`argparse` under the hood and converts the python arguments into cmdline
arguments, neatly and programatically determining whether the arguments should
be optional/required, their types, and default values. TODO would be to parse
the docstring for the following help message!

## Table of Contents

- [Philsophy](#philsophy): A primer on the design behind `utils`.
- [Getting Started](#getting-started): How to use `utils`
- [TODOs](#todos): Some future work
- [Organization](#organiztaion): Example directory organization on how to use
  `utils`.
- [Acknowledgements](#acknowledgements): Special thanks to...

## Philosophy

Python is a great language for rapidly proto-typing ideas and getting them off
the ground. When it comes to building apps, or running scientific experiments,
it's hard to find another language with a comparable fluid experimental workflow
thanks to the combination of the scientific-library stack (`numpy`, `scipy`,
`torch`, `tensorflow`, `jupyter`, ...), as well as the simplistic, dynamically
typed flexibility offered by python, allowing for rapid iteration for scripts
and app-development. 

As a result, what ends up happening is that developers will build a multitude of
tools to support their own needs, from custom `argparse`-boilerplate code for
spinning up new scripts, to creating their own directory organization systems
for interfacing with their experimental datasets, models, results,
visualizations, etc.

`utils` aims to unify this world of productivity

- We want it to be easy to **add** code, and create **new** results.
  - We only have two files, because we want to Keep It Simple and Stupid. 
  - `utils.py` only interfaces with what directories need to exist to organize
    which results a developer cares about. See more in
    [#organization](#organization).
- We want to simultaneously support a Python and cmd-line API.
  - We want to think as though `python` is the developer's world in which they
    develop new algorithms, models, applications, ...
  - But independent of code, one should be able to apply said algorithms,
    models, applications, ...
    - `cmd_line.py` takes an existing python API and automatically turns it into
      a `cmd_line` interfacing API.

## Getting Started

0. To generalize the useage of `utils`, we use an environment variable `WS_PATH`
   to specify the workspace path housing your project directory, as well as the
   relevant data.

   Add the following to your `~/.bashrc`

   ```bash
   export WS_PATH=/path/to/your/ws/dir
   ```
1. Use `parseArgsForClassOrScript(...)` to turn a python function into the head
   for a cmdline script

  ```python
  import src.utils.utility as _util
  import src.utils.cmd_line as _cmd

  def train(dataset: str, num_epochs: int, ...):
      ...
      for epoch in range(num_epochs):
          train_step(...)
      ...

  def main():
      global _logger
      args = _cmd.parseArgsForClassOrScript(train)
      varsArgs = vars(args)
      verbosity = varsArgs.pop('verbosity', _util.DEFAULT_VERBOSITY)
      _logger.info("Passed arguments: '{}'".format(varsArgs))
      train(**varsArgs)

  if __name__ == '__main__':
      main()
  ```

## TODOs

- [ ] Parse docstring to also produce a help-message
- [ ] Correctly pass the `verbosity` flag recursively through the pipeline

## Organization

Here is an example of how `utils` could be used in your python project

```
./src: ..... Root python project source code
  - scripts: Relevant scripts to run particular jobs
    - train.py: Training executable to run a training job
    - demo.py: Demo executable to run a demo 
  - utils: General Utilities
    - utility.py
    - cmd_line.py
  - model
    - object_detection
      - yolo
        - v1
        - v2
        - v3 
    - rnn
    - rnn+attn
    - transformer
      - bert
      - gpt2
    - cnn
      - alexnet
      - resnet50
./data: .... Root data directory to place all relevant datasets, model weights,
    logs, ...
  - datasets: pre-processed training datasets
    - imagenet:
      - 1000
      - 5000
      - 10000
      - 100000
      - all
    - ...
  - raw: pure, un-touched datasets in their raw form
    - imagenet:
      - 1000
      - ...
  - weights: model checkpoints
    - imagenet:
      - model=resnet50
        - 0000
          - weights.pth
  - tb: tensorboard logs
    - imagenet:
      - model=resnet50
        - 0000
          - ...
```

## Acknowledgements

- Shon Katezenberger for being such an immensely impactful and inspirational
  mentor over the years, and always driving for succinct, high-functioning,
  purposeful, and correct code.
- [Ryan Rowe (@rfrowe)](https://github.com/rfrowe) for helping me test and debug
  `cmd_line.py` over our projects

