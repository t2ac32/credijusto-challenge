# Origination Group Technical Challenge



## The high level problem


## Proposition

At this point i don't count with much information about how the service work. 
I would like to start by proposing a generla development Pipeline with two main blocks:
- Continous Integration Pipeline 
- Continous Development Pipeline

### The continous Integration Pipeline
Is the main set of tools that will helps with the work flow and implementation constant 
and with enough capabilities to keep growing and adding new features and developers.
Some commons tools to use will be:
- Git: github, gitlab 
- Pytest: Create unitary tests for every new module integrated to the project
- Virtual environments

### Continous Deployment Pipeline:
Asuming the tools mentioned in the last section where used/integrated a continous Deployment pipeline can be 
set up in order to control the quality of code being sent to production before and during deployment.

By using pyTest a separated set of tests can be written that are connected to production services.
Different code repository services offer Continous integration pipelines where pytest tests can be checked 
for 100% completition in order to accept any kind of deployment and merge requests.

At the same time continous integration services usually offer container services such as docker 
for standarization of the testing services. This services allow to create multiple images of the desired service
where an instance of that service can be used to replicate what production services look like. 

# Production test plan:
Based on what was explained above the next test pipeline diagram demonstrates the general idea of the ***production deployment pipeline***.   

![Test Plan to production](/images/high_levelproposition.png)

### Tests proposition
- server connection check
- database response check
- client data check
- client parameters check
- model response time
- model output validation


### The Low level problem

**How to run**
Docker:
- Go to project folder
- from terminal run:
    ```
      docker-compose up 
    ```
- Enter http://localhost:5000/ in a browser to see the application running. 
- If this doesn’t resolve, you can also try http://127.0.0.1:5000
 - It will ask for user and password to get a token:
   ```
   user: appsecret
   pass: appsecret
   ```
Python:
- App uses flask simply running exchange_service.py will run a local host on port 5000
cd to project folder
python exchange_service.py
On browser: go to 127.0.0.1:5000/

## GET RATES (from providers)
http://localhost:49155/rates
- notes: fixer (provider0) free account doesnt allow to choose base as USD, defaul base EUR
## GET RATES (from fixer)
http://localhost:49155/fixer
- notes: fixer (provider0) free account doesnt allow to choose base as USD, defaul base EUR
## GET RATES (from BANXICO )
http://localhost:49155/bmx
- notes: fixer (provider0) free account doesnt allow to choose base as USD, defaul base EUR
## GET RATES (from Diario oficial de la federacion )
http://localhost:49155/dof
- notes: fixer (provider0) free account doesnt allow to choose base as USD, defaul base EUR


### The Scenario problem