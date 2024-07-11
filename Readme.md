# Online Marketplace Platform


## Requirements
* python 3.11

#### Running on docker
* comment out `MONGO_DATABASE_URI` env variable as docker has it's own configured and this variable will override it

* run `docker compose build web`
* run `docker compose up web`


#### Running Locally
using a virtual enviroment like `venv` or `pyenv` would be a good idea 

* run `pip install -r requirements.txt`
* run `./backend/start.sh`


you can now head to fastapi interactive docs to try the apis at http://localhost:8000/docs


#### Upon startup
the ``start.sh`` script will run to check for admin user if not found it will assume that it's the first time running the project and it will populate the database with one admin user and one product

```
email: admin@admin.com
password: 12345678
```

to test stripe webhook events you'd need to run the stripe cli tool andd replace the `STRIPE_WEBHOOK_SECRET` with the generated one
```dotnetcli
stripe listen --forward-to localhost:8000/api/webhooks/stripe
```



#### running tests
```./backend/test.sh```
##### Extra endpiont

implemented and extra endpoint to recieve a notification whenever a new product is listed 
all connected clients will get this notification except admins
you can test it by opening a new tab and navigate http://localhost/api/
this route will render a simple html page that will request a socket connection and display the received messages
try to post a new product
``` ~ note: only admins can post products ~```

admins get notifiyed whenever a paymenent succeed in order to try that you'll need to use postman or something similar to request a connection as admin by seting the `authorization`  header with the admin jwt
