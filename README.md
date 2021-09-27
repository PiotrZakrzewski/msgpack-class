# Python 3.8.11 serialization benchmark
This repo is a companion to my [blog post](https://piotrzakrzewski.medium.com/)
Read it for more context.

Create a new venv with python 3.8.11 and install the deps with 
```shell
poetry install
```

Run the benchmark with
```shell
pytest --benchmark-save=results.txt --benchmark-save-data
``` 
it will generate the results in `.benchmarks` dir, as a JSON.

My results, generated with the above commands ( and transformed from json to a csv)
 are in [this csv file](results.txt). Mind that the columns mention 
following numbers of fields: single, 100, 1k ...
while the blog post mentions 4, 400, 4k ... the 4x is correct, 1, 100 1k .. where the
input to the generator returning the test data and pytest used it by default as the column names.
