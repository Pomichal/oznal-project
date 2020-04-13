# OZNAL (Knowledge Discovery) project, FIIT STU

## Data

We are using the [Goodreads dataset](https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home?authuser=0).

We works with young adult genre subset:
- [books](https://drive.google.com/uc?id=1gH7dG4yQzZykTpbHYsrw2nFknjUm0Mol) - download size (.gz): 100 MB
- [interactions](https://drive.google.com/uc?id=1NNX7SWcKahezLFNyiW88QFPAqOAYP5qg) - download size (.gz): 1.7 GB
- [reviews](https://drive.google.com/uc?id=1M5iqCZ8a7rZRtsmY5KQ5rYnP9S0bQJVo) - download size (.gz): 857 MB


To convert json data to csv use the converter.py script:

```bash
$ python src/preprocessing/converter.py -i data/goodreads_books_young_adult.json -o data/books      # example usage from project's root folder
```

## Virtualenv and dependencies

You can create a python virtual enviroment and install all dependencies by running these commands in project folder:

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python -m ipykernel install --user --name=.venv   # add .venv to the jupyter notebook kernels (see: https://janakiev.com/blog/jupyter-virtual-envs/)
```
