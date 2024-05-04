# TODO APP BACKEND
This is the backend of a todo app. It provides User IAM and todo CRUD along with APIs for frontend integration.

## Table of Contents
- [CAPABILITIES](#CAPABILITIES)
- [WHAT COMES WITH THE APP](#WHAT-COMES-WITH-THE-APP)
- [HOW TO RUN THE APPLICATION](#HOW-TO-RUN-THE-APPLICATION)

## CAPABILITIES
This application is able to serve a multi-user "todo" tasks creation and managing interface.
All the tasks are user specific and the app lets the user:
- List
- Create
- Delete
- Update (edit)
- Flag as important or done

A task is composed by:
- Text (description of the todo)
- Due date
- Importance flag
- Completion flag (done)

The multi-user scenario forces a user to create an account and then log into the application; otherwise, the server won't allow any interaction.

## WHAT COMES WITH THE APP
The application automatically creates all the needs for local testing but also for production deployment.
In fact, once you run the application for the first time, a database (SQLite) is automatically created by SQLAlchemy and populated with needed tables.

Alembic is already configured to perform database versioning but only the first revision is present. In any case, at startup it is not mandatory to run any Alembic operation since SQLAlchemy will provide the startup configuration.

A static file of a functional frontend app, fully integrated with the backend, is provided and mounted along with the backend by FastAPI at the root path.

Also the documentation is served as a static file at "/mkdocs/". **IT'S IMPORTANT TO PUT THE BACKSLASH (/) AT THE END OTHERWISE THE APPLICATION WILL NOT FIND THE PATH AND REDIRECT TO ROOT!!** 

## HOW TO RUN THE APPLICATION
This app can be run locally in different ways, here are two easy ones:

*after run the app, go to:*
- *127.0.0.1:5174 to render the frontend*
- *127.0.0.1:5174/mkdocs/ to render the docs*
- *127.0.0.1:5174/docs/ to render the API docs*

### Method 1, using interpreter
**Requirements**:
- Python (> 3.8)
- Pip
- **!!create .env file in root folder!!** --> see here ("./docs/environment file.md")

**Procedure**:
- Clone the repo locally (or download as a zip and then unzip).
- Create a venv or use the global environment and install the required modules:
    `pip install -r .\requirements.txt`
- Run the main.py file (with global environment or venv, accordingly). Here is how to run with a global interpreter:
    `python ./main.py `

### Method 2, using Docker
The app comes with a Dockerfile and a docker-compose file. You can create your image to run the app inside a container.

**Requirements**:
- Docker

**Procedure**:
- First create the image:
    `docker-compose build`
- After finishing, run the container:
    `docker-compose up`


### Additional consideration
The application uses mkdocs for the docs. It is included as requirement inside `requirements.txt` and installed automatically if the procedure above is followed.
In order to customize the documentation, you need to:
- create, edit or delete MD files inside the ./docs folder
- modify the `./mkdocs.yml` file accordingly

Along with mkdocs, a custom community theme is installed (material) to render a nices documentation.
