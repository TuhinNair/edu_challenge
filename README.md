# manatal_edu

### Containerization
- In a production application consider a multi-stage build to minizmize image size.

- The script to check for service availability is from here https://github.com/Eficode/wait-for as recommended by the docker-compose docs. See https://docs.docker.com/compose/startup-order/

### Secrets
- *.env* should not be checked into version control but for this challenge I've left it out of *.gitignore*.

### Model

- The spec defines id's to be 20 char but also mentions that UUID is an option. The use of the UUIDField invalidates the 20 char limit and sacrifices readibility. For a human readable implementation (with sufficient entropy if desired) I've decided to defer for later (i.e after I get the rest of the app running and have time to spare).

## How to run it

### Build

`docker-compose up`

### Creating a superuser 

Enter the service container and run 

`pipenv run python manage.py createsuperuser --email <admin@example.com> --username <admin>`