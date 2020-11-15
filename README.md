# serverlessCqrsPython

<h2>Welcome to the exercises for CQRS in Python.  </h2>

<h4> An important caveat for Python.</h4>
JSON in Python is case sensitive.  By convention, I have named all class variables in python in camel case starting with
an upper case letter.  For example, the hotel identifier is HotelId, the reservation identifier is ReservationId. The
JSON text you send to the API **must** match the case of the class variables or serialization will fail.


Once you have checked out the code, you will need the following set up on your workstation:
1. A local installation of EventStoreDB from  https://www.eventstore.com/ is required to run this project.  Make sure 
that the event store database is installed and running.  This can be verified by
loading http://localhost:2113/web/index.html#/ The default username/password is admin/changeit.  Commands cannot be issued 
to the hotel reservation system without an active event store.  There are 2 methods of installing event store.
    1. A docker-compose.yml file has also been provided in the repositories root directory. Execute the command
    `docker-compose up` in the root directory if you have docker installed.
    1. You can find installation instructions for Event Store Db at https://www.eventstore.com/. 


1. **Python 3**, I suggest python 3.7, available from https://realpython.com/installing-python/#how-to-install-python-on-linux 
for Linux or the windows store https://www.microsoft.com/en-ca/p/python-37/9nj46sx7x90p for Windows. 
1. pip, the python package installer. Type `pip help` at a command line to see if it's already installed after installing python.
pip can be installed using the instructions at https://phoenixnap.com/kb/install-pip-windows for Windows or https://pip.pypa.io/en/stable/installing/
for Linux
1. An IDE, I've used both pycharm and Visual Studio Code to develop this repository.
	1. Azure Functions - you can run the examples as an Azure Function, but you must install the Azure functions core tools.
	 If you choose Azure functions, you will have to run and debug using Visual Studio Code. Instructions for debugging
	 and running Azure Functions can be found at https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-04
	1. pycharm from jet brains can also be used, as the code can be run as a flask app
1. Install dependencies, if you use pycharm or Visual Studio Code, the IDE will install all required python libraries. 
The IDE will not install Azure functions core tools, you must do this step yourself.
1. You can install the dependencies from the command line.  In the repostiories root directory, using the provided 
`requirements.txt` file and pip by entering the command `pip install -r requirements.txt`

Running the code through the IDE is the easiest way to get started.  pycharm should modify all path's so that the libraries 
developed for this module are found.  The Azure functions module appends to the system path to ensure that all python 
classes can be found.  If you're a purist and want to run everything from the command line, you will have 
to modify your PYTHONPATH environment variable to include the root directory of the repository.

<h2> Running the Flask project in pycharm</h2>
There is a directory called `FlaskProject` in the repository root directory that contains a python file called `app.py`. 
This is the entry point for the Hotel Management API described in the exercises.  Here you will find the entry point for 
the MakeReservation command which is in a function called make_reservation.  Debug or run app.py within the IDE to start
the hotel reservation system under as a Flask web app.  The web app will run at http://localhost:5000
 
 <h2>Running the Azure Function project in Visual Studio Code</h2>
 If you prefer to run the hotel reservation system as an Azure function you must do so using Visual Studio Code unless you
 are very familiar with the Azure functions command line interface. Your entry point for Azure functions is a file called
 `__init__.py` in a directory called MakeReservation.  Azure functions written in python are named after the directory
 that contains them. The azure functions will be hosted locally at http://localhost:7071/api .
 