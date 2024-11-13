
# KHATAMAT 
a platform for muslims to discuss various islamic topics and do khatmas together, read quran, discuss inside closed groups.

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
pip install -r requirement.txt
``` 
clone the front-end repo here https://github.com/KMalek101/gharib
```
cd khatamat_b
git clone https://github.com/KMalek101/gharib
```    
``` 
cd gharib/
npm i 
npm run build
```
### start the server
go back to the main dir
```
cd ..
python3 manage.py runserver
```
open a new branch and start working
