# Run with docker

```shell
docker build -f "Dockerfile" -t stayinyourkot:latest "."
```

```shell
docker run -p 8080:8080 stayinyourkot:latest
```

# Run with pyenv and virtualenv
https://realpython.com/intro-to-pyenv/
https://github.com/pyenv/pyenv

Ìnstall dependencies
```shell
brew install openssl readline sqlite3 xz zlib
```

Install pyenv
```shell
brew install pyenv
```

Add python 3.8.2
```shell
pyenv install 3.8.2
```

Set python version for this project(execute in the projects directory)
```shell
pyenv local 3.8.2
```

Create a new virtualenv for this project using python 3.8.2
```shell
pyenv virtualenv 3.8.2 siyk
```

Activate your environment
```shell
pyenv local siyk
```

Install all the requirements
```shell
pip install -r requirements.txt
```

Run the app, which will be available on localhost:8050
```shell
python viz/app.py
```

# Deploy on Google App Engine

An app.yaml file is included with the correct gunicorn command to deploy and run on GAE.


# Run the jupyter notebooks

Follow the instructions to run the app locally.

Install jupyter
```shell
pip install jupyter
```

Run jupyter (notebooks are located in notebooks directory)
```shell
jupyter notebook notebooks
```