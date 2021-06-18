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

![Test Plan to production](/images/high_levelproposition.png)




### The Low level problem
### The Scenario problem