# VERITAS - Backend
## Setting Up Local Environment
The first thing to do is to clone the repository:
```sh
$ git clone https://github.com/manthan2205man/vendor.git
$ cd vendor
```
Create a virtual environment to install dependencies in and activate it (if python command is not available, you may create an alias by `alias python="python3"`):
```sh
python -m venv venv
```
Verify whether you are in virtual environment or not (It should print the path containing venv folder):
```sh
pip -V
```
For windows to activate ENV:
```sh
venv\scripts\activate
```
For Mac/Ubuntu to activate ENV:
```sh
source venv/bin/activate
```
```sh
(venv)$ pip install -r requirements.txt
```
Once `pip` has finished downloading the dependencies:
```sh
(venv)$ python manage.py migrate
(venv)$ python manage.py runserver
```
Here is a postman collection to check APIs
```sh
https://api.postman.com/collections/12941465-b68d7cbe-57cf-4328-8a6e-43d0a68b5718
```