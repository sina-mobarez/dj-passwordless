# Django passwordless
`django passwordless` is a good base for one time password projects that using django 


## Build With
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=802d2d&labelColor=2c2c2c)
![RabbitMQ](https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white)



## Table of Contents
- [Django passwordless](#django-passwordless)
  - [Build With](#build-with)
  - [Table of Contents](#table-of-contents)
  - [About the Project](#about-the-project)
    - [What does it do?](#what-does-it-do)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Setup and Deploy steps](#setup-and-deploy-steps)
  - [Licence](#licence)



## About the Project

This project is simple and sutable for base of django projects that want to use one time password, this base code use [pyotp](https://pypi.org/project/pyotp/) package for provide code and use DRF for send it to phone number of user, i use [ippanel service](https://ippanel.com/) for sending sms, you can use another service like [Kave negar](https://kavenegar.com/) or [Twilio](https://www.twilio.com/).

### What does it do?
This project is use phone number instead username and send a code by sms to that namber and authenticate user by that (Sqlite by default).

>  user don't have to register, just have to login and use your site
The otp code send asynchronously to user (Use Celery)

> use RabbitMq for broker, you can use redis also

DRF used for send otp code, use Fetch java script to call that api, 
logging also implemented,
of course the whole project is just a base for other projects and you must develop it by yourself.



## Setup

### Prerequisites
Before setting up the Django passwordless project, ensure that you have the following prerequisites installed on your machine:

- Python
- Docker (or install rabbit and celery)


### Setup and Deploy steps
Follow these steps to set up the project:


**1. Clone the repository using Git:**

```
git clone https://github.com/sina-mobarez/dj-passwordless.git
```

**2. register for sms pannel**

if you want to use sms for sending code, you must register and get pannel 


**3. install requirements**

```
pip install -r requirements.txt
```


**4. Setup `.env` file**

inside `lesspass` directory create a `.env` file with variable structure similar to `.env.dist` file.


**5. Run the rabbit and celery**
i suggest use docker file and don't install local rabbit
for this use following command:

```
docker pull rabbitmq
```
```
docker run -d -p 5672:5672 rabbitmq
```
```
celery -A core worker --loglevel=INFO
```

**6. Create db tables, Super-user and run server**
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py createsuperuser
```
```
python manage.py runserver
```


## Licence

`Django passwordless` is maintained under `GNU General Public License v3.0` license (read more [here](/LICENSE))
