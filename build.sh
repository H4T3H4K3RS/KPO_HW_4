echo ====CREATING DB [START]====
python create_db.py
echo ====CREATING DB [END]==== 

echo ====CREATING MIGRATIONS [START]==== 
python manage.py makemigrations 
echo ====CREATING MIGRATIONS [END]==== 


echo ====MIGRATING [START]==== 
python manage.py migrate 
echo ====MIGRATING [END]==== 

echo ====RUNNING [START]==== 
python manage.py runserver 0.0.0.0:8080 