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

### Managing dependencies
The `requirements.txt` file defines exactly which packages - and which versions
of those packages - must be installed to the Python virtual environment, for both
local development and server deployments.

`requirements.txt` is compiled from `requirements.in` using the `pip-compile` command.

To add a Python package - e.g. pandas - that is referenced by any module in this
repository, first add it to `requirements.in` file. Then, run:

    pip-compile

To upgrade existing referenced packages or their dependencies, run:

    pip-compile --upgrade

Then, your virtual environment can be updated with any new or updated packages
using the following command:

    pip install -r requirements.txt

Note that, after upgrading any packages or their dependencies, it's a good idea
to test that everything works as expected, before committing the updated
`requirements.txt` to source control.

## Deployment
Log on to the server and switch to the root user by typing `sudo -s`.
Then, `cd` to the `/srv/Dash_applications` directory and run the following
commands to update the deployed Dash apps:

    git pull
    docker-compose build
    docker-compose up -d
