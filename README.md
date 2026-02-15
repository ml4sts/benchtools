# Benchtools

a python library designed to help people design and run LLM benchmarks

**warning** currently just an outline, has not yet run


## Usage 
```
benchtool init new_test -p ../ -t add ../datasets/add/ -t Gaps ../datasets/miscops/ -a "this is a demo for benchtools"
```
```
Creating new_test in ../
Setting up add...Success
Setting up Gaps...Success
Would you like to run the benchmark? y/n? n
```
```
benchtool add-task ../new_test/ FillIn ../datasets/miscops/
```
```
Setting up FillIn...Success
```

```
benchtool run testRuns/111
```
### CLI 

``` 
benchtool init <benchmark_name>
```
To generate a folder structure for the Benchmark

The system asks conceptual questions about the benchmark to align user's thoughts with the BetterBench checklist



## Orientation to the Repo

- the `benchtools` folder is the code for the library
- `demobench` is a very minimal example benchmark that will function somewhere in between tests and docs.  eventually probably needs to be actually moved into one of those cases, but for now a top level so it can do both during development
- `docs` will hold documentation files that can render to a website with sphinx
- `project.toml` should provide info to make `pip install .` work
  

## Contributor

<!-- here we will write things for how people contribute after it is more complete -->