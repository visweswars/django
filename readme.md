Zillow project using Python Django by mruanova

cd "git/dojo/4-Python/environments/djangoEnv/Scripts"
or 
cd "git/dojo/4-Python/environments/python3env/bin"
source activate

cd ../../../
cd django
cat runtime.txt
cd zillow
python manage.py runserver

127.0.0.1:8000

git add .
git commit -m "updated runtime.txt"
git push -u origin master

#update
sudo pip install --upgrade pip
sudo pip install -U Django
pip freeze > requirements.txt

