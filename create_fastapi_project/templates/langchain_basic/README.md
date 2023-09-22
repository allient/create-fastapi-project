# FastAPI Project with `create-fastapi-project`

This is a FastAPI project initialized using [`create-fastapi-project`](https://github.com/allient/create-fastapi-project), designed to provide a quick start for building APIs with [FastAPI](https://fastapi.tiangolo.com/).

## Required API Keys

### OpenAI

1. Create an account on [OpenAI](https://platform.openai.com/).
2. Get your API key from [API Keys - OpenAI](https://platform.openai.com/account/api-keys).
3. Set your API key as an environment variable named `OPENAI_API_KEY`.

## Other API Keys (Optional if you want to use the template's custom tools)

### Unsplash (Image Search)

1. Create an account on [Unsplash](https://unsplash.com/developers).
2. Create an app on [Unsplash Developers](https://unsplash.com/oauth/applications).
3. Get your Access Key from [Your Applications - Unsplash Developers](https://unsplash.com/oauth/applications).
4. Set your Access Key as an environment variable named `UNSPLASH_API_KEY`.

### SerpApi (Search Engine Results Page API)

1. Create an account on [SerpApi](https://serpapi.com/).
2. Get your API key from [API Key - SerpApi](https://serpapi.com/manage-api-key).
3. Set your API key as an environment variable named `SERP_API_KEY`.

## Containers Architecture

As this project uses [Caddy](https://caddyserver.com/) as a reverse proxy, which uses namespaces routing, you can access the documentation with the following path [http://fastapi.localhost/docs](http://fastapi.localhost/docs)

## Getting Started

The commands in this documentation can be customized on the **Makefile**. It can be started with and without docker.

This project uses poetry, if you don't have it installed, you can the follow the instruction in [Poetry Documentation](https://python-poetry.org/docs/#installation).

- Run the server (Recommended using docker):

```bash
# Run locally with docker in dev mode and force build
make run-dev-build
# or
# Run locally with docker in dev mode
make run-dev
# or
# Run locally with docker in prod mode (Autoreload disabled)
make run-prod
```

Open [http://fastapi.localhost/docs](http://fastapi.localhost/docs) with your browser to see the result.

- Run the server without docker:

First, make sure you have all packages installed:

```bash
make install
```

```bash
make run-app
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) with your browser to see the result.

You can start editing the server by modifying `app/main.py`.

## Demo Langchain Tools

- Search weather by city name ![weather-tool](https://res.cloudinary.com/dnv0qwkrk/image/upload/v1692746086/Allient/create-fastapi-project/weather-tool-demo_lgqtwu.gif)
- Search images by keyword ![images-tool](https://res.cloudinary.com/dnv0qwkrk/image/upload/v1692746086/Allient/create-fastapi-project/search-images-demo_mkorzv.gif)
- Search videos by keyword ![videos-tool](https://res.cloudinary.com/dnv0qwkrk/image/upload/v1692746087/Allient/create-fastapi-project/search-videos-demo_wikzn1.gif)
- Search pokemon by name or id ![pokemon-tool](https://res.cloudinary.com/dnv0qwkrk/image/upload/v1692746086/Allient/create-fastapi-project/pokemon-tool-demo_ggsc63.gif)

And also includes a agent that uses the tools to answer your questions.
You can access the agent by opening [http://fastapi.localhost/chat](http://fastapi.localhost/chat) with your browser or you can use the frontend server.

## Frontend server

This project includes a frontend server that uses [Streamlit](https://streamlit.io/) to display a chatbot that uses the langchain tools to answer your questions.

- Run the frontend server (Recommended using docker):

```bash
make run-streamlit
```

Now you can access the frontend server by opening [frontend.localhost](http://frontend.localhost) with your browser.

if you want to run the frontend server without docker, you need to install the dependencies in the frontend folder.

```bash
cd frontend
cd app
poetry install
streamlit run streamlit_app.py
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

Running `pip install create-fastapi-project@latest` (with no arguments) launches an interactive experience that guides you through the process of setting up your project. This interactive approach simplifies the initial configuration and gets you started quickly.

### Zero Dependencies

`create-fastapi-project` has been designed to be lightweight and efficient. It requires zero external dependencies, ensuring that your project remains unburdened by unnecessary packages.

### Reliability and Maintenance

`create-fastapi-project` is officially maintained by the [Allient development team](https://www.allient.io/). It is well-tested and aligns with best practices, ensuring that it functions as expected and remains up to date with FastAPI's releases.

By choosing `create-fastapi-project`, you streamline your initial project setup, leverage reliable patterns, and enjoy the convenience of a tool tailored for FastAPI development.

We love ❤️ [FastAPI](https://fastapi.tiangolo.com/) and its ecosystem. You can check out the [create-fastapi-project GitHub repository](https://github.com/allient/create-fastapi-project) - your feedback and contributions are welcome!
