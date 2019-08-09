Zillow project using Python Django by mruanova

cd git/python3env/bin
source activate

cd ..
cd zillow
cat runtime.txt
python manage.py runserver

127.0.0.1:8000

#update
sudo pip install --upgrade pip
sudo pip install -U Django
pip freeze > requirements.txt

git add .
git commit -m "updated requirements.txt"
git push -u origin master