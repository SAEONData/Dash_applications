# SAEON Dash Applications

A repository of [Dash](https://plotly.com/dash/) applications developed
by the SAEON uLwazi Node's Data Science Team.

## Development

### Initial setup
Clone this repository to your local computer:

    git clone https://github.com/SAEONData/Dash_applications.git

Switch to the `Dash_applications` directory:

    cd Dash_applications/

Create a Python virtual environment:

    python -m venv .venv

Activate the virtual Environment:

#### On Windows
    .venv\Scripts\activate
    
#### On Linux
    source .venv/bin/activate

Install Dash and other packages to the Virtual Environment  
    
    pip install -U pip setuptools pip-tools
    pip install -r requirements.txt

Now you can open the `Dash_applications` folder as a project in the PyCharm IDE.

## Deployment
Log on to the server and switch to the root user by typing `sudo -s`.
Then, `cd` to the `/srv/Dash_applications` directory and run the following
commands to update the deployed Dash apps:

    git pull
    docker-compose build
    docker-compose up -d
