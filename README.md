![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![ML Client Build/Test](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/ml-client.yml/badge.svg)
![Web App Build/Test](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/web-app.yml/badge.svg)

# Rock Paper Scissors

## Table of Contents
1. [Description](#description)
2. [Set up a virtual environment](#set-up-a-virtual-environment)
3. [Run the app](#run-the-app)
4. [Team members](#team-members)

## Description
This app allows users to play standard rock paper scissors against the computer. It uses machine learning to recognize hand gestures from the web camera and compares that against the randomized computer choice to determine the winner. The app leverages Docker and MongoDB, operating in a containerized environment with three sub-systems: a machine-learning client, a web-app interface, and a database.
See [instructions](./instructions.md) for details.

## Set up a virtual environment
Install pipenv using pip:
```
pip3 install pipenv
```

Activate it:
```
pipenv shell
```

Create a new virtual environment with the name .venv
```
python3 -m venv .venv
```

Activate the virtual environment:
```
source .venv/bin/activate # For Mac
.venv\Scripts\activate.bat # For Windows
```

Install dependencies using pip
```
pip3 install -r requirements.txt
```

## Run the app
Start by building
```
docker-compose up --build
```

Or if you have previously built and haven't made any changes, simply compose the containers
```
docker-compose up
```

Play the game!
Open the web app following this link [HERE](http://127.0.0.1:5001)

## Team members

[Haley Hobbs](https://github.com/haleyhobbs) \
[Emma Zhu](https://github.com/ez106) \
[Jason Tran](https://github.com/huyy422) \
[Jenna Han](https://github.com/jnahan)