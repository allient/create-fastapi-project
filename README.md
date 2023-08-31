# Create FastAPI Project

We love ❤️ [FastAPI](https://fastapi.tiangolo.com/) and its ecosystem so we decided to make easier to get started with [FastAPI](https://fastapi.tiangolo.com/) projects. By using the `create-fastapi-project` CLI tool, you can quickly start building a new FastAPI application with a basic folder structure, with everything set up for you.

To get started, use the following command:

```bash
pip install create-fastapi-project
create-fastapi-project
```

After you that you are going to see an interactive screen like this:

![create-app-terminal](https://res.cloudinary.com/dnv0qwkrk/image/upload/v1692746180/Allient/create-fastapi-project/demo-create-fastapi-final_fyirob.gif)

## Templates

### Basic

<details>
  <summary>See More</summary>
  
  We're excited to introduce you to our FastAPI Basic Project Template, carefully designed to jumpstart your FastAPI development journey. This template offers you a pre-configured project with a fundamental FastAPI setup and an organized folder structure, allowing you to hit the ground running.

## Folder Structure

```bash
└───app
  ├───app
  │   ├───api
  │   │   └───v1
  │   │       └───endpoints
  │   ├───core
  │   ├───schemas
  │   └───utils
  │       └───exceptions
  └───test
```

</details>

### Langchain Basic

<details>
  <summary>See More</summary>
  
  We're thrilled to introduce you to the LangChain project template, designed to accelerate your development process. This template serves as a solid foundation for your project, complete with essential features and an organized folder structure, all thoughtfully configured and ready for use.

## Folder Structure

```bash
app
    ├───app
    │   ├───api
    │   │   └───v1
    │   │       └───endpoints
    │   ├───core
    │   ├───schemas
    │   ├───templates
    │   │   └───general_pages
    │   └───utils
    │       ├───adaptive_cards
    │       └───exceptions
    └───test
```

## Containers Architecture

![langchain-architecture](https://res.cloudinary.com/dnv0qwkrk/image/upload/v1693340056/Allient/create-fastapi-project/image_2_mraj02.png)
As this project uses [Caddy](https://caddyserver.com/) as a reverse proxy, which uses namespaces routing, you can access the documentation with the following path [http://fastapi.localhost/docs](http://fastapi.localhost/docs)

## ENV Variables

```bash
PROJECT_NAME=
OPENAI_API_KEY=
UNSPLASH_API_KEY= # Optional
SERP_API_KEY= # Optional

#############################################
# Caddy variables
#############################################
EXT_ENDPOINT1=127.0.0.1
LOCAL_1=localhost
LOCAL_2=127.0.0.1
```

## Tools

- Search weather tool ![weather-tool](https://res.cloudinary.com/dnv0qwkrk/image/upload/v1692746086/Allient/create-fastapi-project/weather-tool-demo_lgqtwu.gif)
- Search images tool ![images-tool](https://res.cloudinary.com/dnv0qwkrk/image/upload/v1692746086/Allient/create-fastapi-project/search-images-demo_mkorzv.gif)
- Search videos tool ![videos-tool](https://res.cloudinary.com/dnv0qwkrk/image/upload/v1692746087/Allient/create-fastapi-project/search-videos-demo_wikzn1.gif)
- Search pokemon tool ![pokemon-tool](https://res.cloudinary.com/dnv0qwkrk/image/upload/v1692746086/Allient/create-fastapi-project/pokemon-tool-demo_ggsc63.gif)
</details>

### Full

<details>
  <summary>See More</summary>
  
This is a project template which uses [FastAPI](https://fastapi.tiangolo.com/), [Alembic](https://alembic.sqlalchemy.org/en/latest/) and async [SQLModel](https://sqlmodel.tiangolo.com/) as ORM. It shows a complete async CRUD template using authentication. Our implementation utilizes the newest version of FastAPI and incorporates typing hints that are fully compatible with **Python 3.10** and later versions. If you're looking to build modern and efficient web applications with Python, this template will provide you with the necessary tools to get started quickly. You can read a short article with the motivations for starting this sample project [here](https://medium.com/allient/our-journey-using-async-fastapi-to-harnessing-the-power-of-modern-web-apis-90301827f14c?source=friends_link&sk=9006b3f2a4137a28a8576a69546c8c18).

## Why Use This Template?

Developing web applications can be a challenging process, especially when dealing with databases, authentication, asynchronous tasks, and other complex components. Our template is designed to simplify this process and offer you a solid starting point. Some of the highlights of this template include:

- FastAPI Integration: FastAPI is a modern and efficient web framework that allows you to quickly and easily create APIs. This template uses the latest features of FastAPI and offers type hints that are compatible with **Python 3.10** and later versions.
- Asynchronous Database Management: We use SQLModel, an asynchronous ORM library, to interact with the database efficiently and securely.
- Asynchronous Tasks with Celery: This template includes examples of how to execute asynchronous and scheduled tasks using Celery, which is ideal for operations that require significant time or resources.
- Authentication and Authorization: We implement JWT-based authentication and role-based access control to ensure that your APIs are secure and protected.
- Documentation and Automated Testing: The template is configured to automatically generate interactive documentation for your APIs. It also includes automated tests using pytest to ensure code quality.
- Development Best Practices: We apply code formatting, type checking, and static analysis tools to ensure that the code is readable, robust, and reliable.

## Folder Structure

```bash
.
├───.github
│   └───workflows
├───.vscode
├───backend
│   └───app
│       ├───alembic
│       │   └───versions
│       ├───app
│       │   ├───api
│       │   │   └───v1
│       │   │       └───endpoints
│       │   ├───core
│       │   ├───crud
│       │   ├───db
│       │   ├───deps
│       │   ├───models
│       │   ├───schemas
│       │   └───utils
│       │       └───exceptions
│       └───test
│           └───api
├───caddy
├───db_docker
├───docs
├───minio
├───pgadmin
├───sonarqube
├───static
└───terraform
```

## Stack

- [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- [Pydantic](https://docs.pydantic.dev/latest/) - A library for data validation and settings management based on Python type hints.
- [SQLModel](https://sqlmodel.tiangolo.com/) - A library for interacting with SQL databases from Python code, with Python objects.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - A lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.
- [Caddy](https://caddyserver.com/) - A powerful, enterprise-ready, open source web server with automatic HTTPS written in Go.
- [Docker](https://www.docker.com/) - A set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers.
- [PostgreSQL](https://www.postgresql.org/) - A powerful, open source object-relational database system.
- [PGAdmin](https://www.pgadmin.org/) - The most popular and feature rich Open Source administration and development platform for PostgreSQL.
- [Celery](https://docs.celeryq.dev/en/stable/) - A simple, flexible, and reliable distributed system to process vast amounts of messages, while providing operations with the tools required to maintain such a system.
- [Redis](https://redis.io/) - An open source (BSD licensed), in-memory data structure store, used as a database, cache, and message broker.
- [Minio](https://min.io/) - A high performance distributed object storage server, designed for large-scale private cloud infrastructure.
- [SonarQube](https://www.sonarqube.org/) - An open source platform for continuous inspection of code quality.
- [Pytest](https://docs.pytest.org/en/stable/) - A framework that makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.

</details>

## Getting Started

The commands in this documentation can be customized on the **Makefile**. It can be started with and without docker.

After your project is created. First, make sure you have all packages installed:

```bash
make install
```

Run the server:

```bash
# Run locally without docker
make run-app
# or
# Run locally with docker in dev mode and force build
make run-dev-build
# or
# Run locally with docker in dev mode
make run-dev-build
# or
# Run locally with docker in prod mode
make run-prod
```

## Learn More

To learn more about Fastapi, take a look at the following resources:

- [Fastapi Documentation](https://fastapi.tiangolo.com/).
- [fastapi-alembic-sqlmodel-async](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async).
- [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql).
- [sqlmodel-tutorial](https://sqlmodel.tiangolo.com/tutorial/fastapi/).
- [asyncer-tutorial](https://asyncer.tiangolo.com/tutorial/).
- [fastapi-pagination](https://github.com/uriyyo/fastapi-pagination).
- [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices).
- [awesome-fastapi](https://github.com/mjhea0/awesome-fastapi).

## Why use Create FastAPI Project?

`create-fastapi-project` provides a streamlined way to kickstart your FastAPI projects. Here are some compelling reasons to choose it for your project setup:

### Interactive Experience

Running `create-fastapi-project` (with no arguments) launches an interactive experience that guides you through the process of setting up your project. This interactive approach simplifies the initial configuration and gets you started quickly.

### Zero Dependencies

`create-fastapi-project` has been designed to be lightweight and efficient. It requires zero external dependencies, ensuring that your project remains unburdened by unnecessary packages.

### Reliability and Maintenance

`create-fastapi-project` is maintained by the [Allient development team](https://www.allient.io/). Our team is composed by a experienced professionals specializing in FastAPI projects and NLP. If you need assistance or support for your project, please don't hesitate to get in touch with us at [info@allient.io](mailto:info@allient.io) or schedule a meeting with us [here](https://calendly.com/jonathanvargas).

You can check out the [create-fastapi-project GitHub repository](https://github.com/allient/create-fastapi-project) - your feedback and contributions are welcome ❤️!

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- This project is licensed under the terms of the **[MIT license](LICENSE)**
