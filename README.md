# Versioner

## Description

Versioner is a tool for tracking which version of various microservices are deployed to different environments by using api calls from whatever deployment pipeline to update a sql database.

Versioner will have a ui for viewing being able to view which applications are deployed by environment and application(done) and on what date they were last deployed(todo, but the data is there)

Versioner will have a django admin login functionality to lock down application and environment names so that deployment api users wont accidently make multiple versions of the same environment or application with different spellings(done)

Versioner will have an api for pulling all the latest deployed sw versions on a paticular environment for purpouses of allowing someone to audit what is deployed in a loggable fashion(done)

Versioner will have the ability to pull a list of the history of deployments for a paticular application for a paticular environment to allow someone to audit when versions of an application were deployed in a loggable fashion(done)

Versioner will have the ability to pull a list of all the latest deployed versions of an application for all environments to allow someone to audit which versions of an application are deployed to each environment in a loggable fashion(done)

## Design

Versioner is a python django web application with api and ui components. This repo is not self-packaged for deployment, but intended to be packaged seperately as a docker container. Versioner's resource requirements are trivial, but it will require the usage of some kind of sql database (even sqlite is probably fine). Versioner will use an admin page to maintain a list of environments and applications to track but is intended to be used as an internal tool and not exposed to the internet

## Manual instalation, setup, and execution for development purpouses

1. Install python3 virtual env
2. Activate python3 virtual env
3. Pull git repo
4. Install pre-requisites 'pip install -r requirements.txt'
5. Create Admin user 'python manage.py createsuperuser'
6. Launch site 'python manage.py runserver'
7. Log in as admin user and create records for application and env names
8. Update deployment processes to send api calls for deployment versions to correct endpoint
    * post call example to http://127.0.0.1:8000/api/AppVersion {"name": "fooapp", "environment": "development", "version": "0.1"}
9. Check UI to make sure deployments are being registered and displayed
10. play around with other apis
    * get request to http://127.0.0.1:8000/api/AppVersion will return json list of most recent deployment for each environment for each application
    * get request to http://127.0.0.1:8000/api/AppEnvironment returns a json list of all environments
    * get request to http://127.0.0.1:8000/api/AppName returns a json list of all application names
    * get request to http://127.0.0.1:8000/api/AppHistory with app name and environment {"name": "barapp", "environment": "production"} returns json list of the entire history of deployments for that environment
    * get request to http://127.0.0.1:8000/api/AppCurrentDeploys with app name {"name": "barapp"} returns json list of the latest deployments for all environments for that application
11. Take a Coffee(or other fine beverage) break. You've earned it.

## More todos:

Web UI needs a web2 makeover

Needs deployment packaging (seperate project)
