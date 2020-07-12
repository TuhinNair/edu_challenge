# manatal_edu

### Containerization
- In a production application consider a multi-stage build to minizmize image size.

- The script to check for service availability is from here https://github.com/Eficode/wait-for as recommended by the docker-compose docs. See https://docs.docker.com/compose/startup-order/

### Secrets
- *.env* should not be checked into version control but for this challenge I've left it out of *.gitignore*.
- Ideally injected during CI builds.

### Model

- The spec defines id's to be 20 char but also mentions that UUID is an option. The use of the UUIDField invalidates the 20 char limit and sacrifices readibility. TODO: A human readable/slug implementation (with sufficient entropy if desired) with integrity checks. 

## How to run it

### Build

`docker-compose up`

### Creating a superuser 

Enter the service container and run 

`pipenv run python manage.py createsuperuser --email <admin@example.com> --username <admin>`