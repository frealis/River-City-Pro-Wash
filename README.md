
# River-City-Pro-Wash

*Website for a power washing company*

- This website was built using Django and uses a Postgres database. It has also been tested using Docker with Windows 10 (Home) and Docker Toolbox (https://docs.docker.com/toolbox/toolbox_install_windows/) which uses Oracle VM Virtualbox, and -not- Microsoft's Hyper-V.


# Run the Web Application Locally

- To start the web application locally, navigate to the root directory (which contains manage.py) and run:

  $ python manage.py runserver

  ... and the website should be accessible at 127.0.0.1:8000. 

- To start the web application locally using the Heroku Local CLI plugin:

  $ heroku local web -f Procfile.windows

  ... and the website should be accessible at localhost:5000.
  
- Alternatively, to run the web application using a Dockerfile, navigate to the root directory (which contains docker-compose.yml) and run:

  $ docker-machine start default          // start up a virtualbox named 'default'
  $ docker-machine env                    // make sure environment variables exist
  $ docker-machine regenerate certs default // do this if prompted for new certs
  $ docker-compose up

  ... and the website should be accessible at 192.168.99.100:8000 (on Windows machines). However, there are a lot of caveats with running the web application from a Docker image which are explained below.

- Local environment variables are managed using dotenv https://github.com/theskumar/python-dotenv.


# Docker

- (4/3/2019) Docker's _Getting Started_ guide states: "Pull and run the image from the remote repository. From now on, you can use docker run and run your app on any machine with this command:

  $ docker run -p 4000:80 username/repository:tag

  ... If the image isn’t available locally on the machine, Docker pulls it from the repository." 
  
  ... Trying this with a Django application will pull a copy of the image from an online repository (if the image is not already available on the local drive) from https://hub.docker.com, but it will -not- automatically launch the application. This is regardless of whether or not a Postgres database is set up, or the port is mapped correctly on the command line (ie. 8000:8000 is my guess), or if it's something else. However, docker compose does work:

  $ docker-compose build    // create a docker image
  $ docker-compose up

  ... when trying to launch the web app from a docker image. However, you maybe have to run it twice: run it, then Ctrl+C (kill) it, and then run it again. I'm not sure if this has to do with setting up a container and creating a Postgres database with the necessary tables for migration first, or if it's something else. 

  ... also, if you make any changes (ex. added new dependencies in requirements.txt), you have to create a new docker image in order to reflect those changes via:

  $ docker-compose build

- This web app has been tested through Docker by launching an image and using a single container on a single virtual machine (a default machine that can be set up using the Docker Quickstart Terminal for Docker Toolbox), but swarms/services/stacks/nodes have not been tested. To view any existing virtual machines:

  $ docker-machine ls

- When deciding whether to launch the application via manage.py or docker-compose, you have to make appropriate database settings adjustments in order to use Postgres; Docker, when set to create a Postgres database through docker-compose.yml, will initially create a database named 'postgres' by default (which is why you probably have to set the 'NAME': attribute of the DATABASE settings in settings.py to 'postgres', at least initially). To test this out, make sure that all images and containers are deleted from your local machine (run these following commands from any directory, it doesn't matter):

  $ docker rm $(docker ps -a -q)    // Remove all containers
  $ docker rmi $(docker images -q)  // Remove all images

  ... and then navigate to the root directory of your Django web application and run:

  $ docker-compose up

  ... after awhile you'll see something like "2019-04-03 04:50:35.270 UTC [50] LOG:  database system was shut down at 2019-04-03 04:50:34 UTC". Next, get the 'postgres' image's CONTAINER ID, sneak into the container, access the postgres database, and see all of the containerized databases by running:

  $ docker container ls
  $ docker exec -it <CONTAINER ID> bash -l  // CONTAINER ID for postgres IMAGE
  root@<CONTAINER ID>:/# psql -U postgres
  postgres=# \l

  ... once you're done with looking at this, Ctrl+Z out of there and then Ctrl+C (kill) whichever terminal is currently running the dockerized instance of the web application. Wait for the application to stop (or alternatively, you can go into another terminal and run $ docker-compose down) and then run $ docker-compose up again. Hopefully at this point you get yellow text that reads "... exited with code 0."
  
  ... however, you might get an error code in yellow text that reads "... exited with code 1." which may have something to do with recently being inside of the database's container. If so, just Ctrl+C and run $ docker-compose up again.

- To login to the www.rivercityprowash.com/admin console while the application is running in a dockerized container, you'll have to create a user with both a username and a password -- when the database is set up in the docker container, it doesn't have a password by default because no password is specified in settings.py. 


# Deploy to Heroku

- Heroku has a free service that can host 1 website at a time on what they refer to as a "dyno". It doesn't offer much processing power (something like 512 MB of RAM) and will basically turn the dyno off after 30 minutes or so of inactivity, but will turn back on with a subsequent HTTP request, although there is a lag time of 10 to 20 seconds for the dyno to start up again.

- The nice thing about Heroku is that you can deploy it from the command line, and each deployment gets assigned a version number. Since each version is basically a git file, you can easily rollback to older versions or use other commands like 'git diff' to compare different versions:

  $ heroku releases         // view the past 15 or so web app versions
  $ heroku rollback v#      // rollback to a specific version, ex. v1, v3, etc.
  $ git diff # #            // # # represent two different deploys

- https://devcenter.heroku.com/articles/django-app-configuration
- https://medium.com/agatha-codes/9-straightforward-steps-for-deploying-your-django-app-with-heroku-82b952652fb4

- To run locally via heroku:

  $ heroku local web -f Procfile.windows

  ... which runs at localhost:5000

- To upload to git/deploy and view online:

  $ git push heroku master
  $ heroku ps:scale web=1 (to make sure at least 1 web dyno is running)
  $ heroku open

  ... note: when you push a web app to heroku, only the 'master' branch takes effect. Pushing code from any other branch is ignored by Heroku.

- When you set DEBUG = False and push this app to production, it will give a 500 error unless the ALLOWED_HOSTS =[] in settings.py includes the URL where this site is hosted. Some people also think that not having collected static files or not migrating the database may also produce this error. To do both:

  $ python manage.py collectstatic
  $ git push heroku master (to push static files to Heroku server)
  $ heroku run python manage.py migrate (to apply migration files)

  ... to troubleshoot:

  $ heroku logs --tail

  ... also note: if you have static files in the templates, ie. {% static 'whatever' %}, and they are commented out via HTML comment tags, they are still visible to the program and can cause issues, especially when Debug = False.

- When altering models.py locally and updating your local database via:

  $ python manage.py makemigrations
  $ python manage.py migrate

  ... you are basically a) creating a migration file with SQL instructions, and b) applying those instructions to alter the database. Heroku has analogous commands:

  $ heroku run python manage.py makemigrations
  $ heroku run python manage.py migrate

  ... however, as long as you push your migration files from the /migration folder to Heroku, you can omit running the first command (makemigrations).

- Heroku environment variables can be viewed and set via:

  $ heroku config                 // view environment variables on heroku server
  $ heroku config:set key=value   // set environment variables on heroku server


# Deploy to AWS

- Web apps deployed on AWS exist in an environment that you can specify when creating a new web application. New applications can be created either from the AWS console or from the command line. AWS has two types of command lines -- awscli (the general all-purpose AWS command line) and awsebcli (the Elastic Beanstalk web development command line). 

- AWS has a free tier that is available for 12 months, and this basically allows for 1 website to be deployed at all times. This website will exist in an environment that can be shut off if needed -- terminating the environment will -not- terminate the application, but it will save on the allotted free tier hours that are granted each month for the first 12 months, so it's a good idea to turn it off when it's not needed. To view, get the status, and terminate an environment:

  $ eb list         // list environments, -a or -all to view all, * marks active
  $ eb use <env>    // switch between environments
  $ eb status       // get detailed information on current environment
  $ eb terminate    // terminate current environment

  ... in contrast to Heroku, where changes are pushed via git and have to be from the 'master' branch, changes in AWS are deployed by packaging all of the files in an application (into a *.zip file or other archive), sending those files to some Amazon S3 server, and then finally sending the files to an AWS environment. However, if you have git installed in the same directory that you're using to deploy to AWS, then your latest commit will get deployed https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-cli-git.html. The command to do this is:

  $ eb deploy

- To create a web app from the AWS console, click "Build a web app" and scroll to the bottom. You can choose a platform and upload a source bundle as a *.zip file. To put the project in a zip file using git from the command line, enter:

  $ git archive -v -o myapp.zip --format=zip HEAD

  ... https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/applications-sourcebundle.html#using-features.deployment.source.commandline

- To deploy from the command line, follow this guide: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html. Basically you have to create a new folder called .ebextensions and add a configuration file to it called django.config. The main commands involved with deploying an application using AWS Elastic Beanstalk are:

  $ eb init         // initializes the EB CLI in the current directory
  $ eb deploy       // packages web app as *.zip and sends to online AWS env
  $ eb open         // opens the web app in a browser

- AWS looks for static files generated by python manage.py collectstatic specifically in a folder called static/ located in the root directory of the project. It has to be static/, not staticfiles/. This could be a configuration setting in nginx, Apache, or whatever runs a Python AWS server.

- To set and view environment variables:

  $ eb setenv key=value     // set a key=value environment variable
  $ eb printenv             // view environment variables


# Generate a new random SECRET_KEY

- https://foxrow.com/generating-django-secret-keys


# Social Media Icon Credits

- Instagram
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

- Yelp
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

- Twitter
<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>