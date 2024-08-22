
# KHATAMAT 
a platform for muslims to do various islamic activities such doing a khatma together, reading articles, discussing different topics and more.
# Contributing          
## how to run it 
### install virtual enviroment
Set up a virtual enviroment
```
python3 -m venv env
```
for Windows:
```
py -m venv env
```
Activate the virtual environment and verify it
```
source env/bin/activate
```
for Windows:
```
.\env\Scripts\activate
```
### clone and download requirements
now clone the repo and install requirement for the backend
```
git clone https://github.com/L4z3x/khatamat_b 
pip install -r requirements.txt
``` 
now install the requirement for the frontend
``` 
cd khatamat_front/
npm i 
npm run build
```
### start the server
go back to the main dir
```
cd ..
```
start the local server
```
python3 manage.py runserver
```