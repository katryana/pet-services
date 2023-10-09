# pet_services

Django project for training centers to provide their services for users

## Check it out

https://pet-services.onrender.com

## Installation

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

A step by step series of examples that tell you how to get a development env running

Python3 must be already installed

```shell
git clone https://github.com/katryana/pet-services
cd pet_services
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
python manage.py runserver  # starts Django Server
```

## Filling out the data

Use ``` python manage.py loaddata training_centers_db_data.json``` to add data

Create your own superuser to test admin features or use these credentials:

username: ``` admin ``` 
password: ```n5d5ved&84```
public
You can sign up to the site to see the difference between staff and ordinary users

## Running the tests

To run tests use this command ```python manage.py test ```

## Features

* Authentication functionality for User
* Customising profile, adding dog with specific breed, making appointments for users 
* The ability to create, update, delete breeds only for staff workers directly from website
* Powerful admin panel for advanced managing

## Demo

Here you can find images of some pages

![image](https://github.com/katryana/pet-services/assets/136272476/f2efdd71-f358-429c-9da4-1a49583e2b00)

![image](https://github.com/katryana/pet-services/assets/136272476/39a5192a-ba59-49e9-bcdf-5ff4c545634b)

![image](https://github.com/katryana/pet-services/assets/136272476/81a500b4-8fe5-47cd-81ad-41db7626251b)
