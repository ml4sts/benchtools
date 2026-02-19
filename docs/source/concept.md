# Overview


`benchtool` is a python library with a CLI for creating, managing, and running AI benchmarks. 

## Key terms

- A benchmark is comprised of several tasks, structured data, and documentation. 
- A task consists of a prompt, optionally a template with variations, a means of scoring, and a reference value if necessary for scoring
- a scoring function must have an API that takes 2 inputs, response and refernce, though reference may be unused and passed as `None`

## Sample benchmarks

The easiest way to get familar is to run the demo benchmarks that are available in the repository


Clone the repository then explore the `benchtools/demos` folder