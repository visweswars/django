Zillow project at Coding Dojo using Python Django by Mauricio Ruanova-Hurtado and Kamil Wowczuk

cd "git/dojo/4-Python/environments/djangoEnv/Scripts"
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
pip install -U Django
pip freeze > requirements.txt

