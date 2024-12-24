<!-- Copyright Vespa.ai. Licensed under the terms of the Apache 2.0 license. See LICENSE in the project root. -->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://assets.vespa.ai/logos/Vespa-logo-green-RGB.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://assets.vespa.ai/logos/Vespa-logo-dark-RGB.svg">
  <img alt="#Vespa" width="200" src="https://assets.vespa.ai/logos/Vespa-logo-dark-RGB.svg" style="margin-bottom: 25px;">
</picture>

# 🔍 Visual Retrieval ColPali 👀

This readme contains the code for a web app including a frontend that can be set up as a user facing interface.

## Why?

To enable _you_ to showcase the power of ColPali and Vespa to your users, and to provide a starting point for your own projects.

> "But I only know Python, how can I create a web app that's not Gradio or Streamlit?" 🤔

No worries! This project uses [FastHTML](https://fastht.ml/) to create a beautiful web app - and it's all Python! 🐍

Also, 👇

<a href="https://imgflip.com/i/98mhch"><img src="https://i.imgflip.com/98mhch.jpg" title="made at imgflip.com" alt="Funny meme about json output in demo"/></a>

## Running this application

This application is containerized with Docker Compose. To start it, run:

```bash
docker compose up
```

This will start the application and the Postgres database.

You can access the application at `http://localhost:7860`.

If you want to run this application locally, you can follow the instructions below.

## Setting up python environment

This application should work on Python 3.8 and above.

You can install the dependencies with `pip`, but we recommend using `uv`.
Skip to [Installing dependencies using `uv`](#installing-dependencies-using-uv) if you want to use `uv`.

## Document feeding

There's a dependency that is used to feed the documents to Vespa.
To install it, run:

```bash
brew install poppler
```

### Installing dependencies using `pip`

You can install the dependencies with `pip`:

```bash
pip install -r src/requirements.txt
```

### Installing dependencies using `uv`

We recommend installing the amazing `uv` to manage your python environment:
See also [installation - uv docs](https://docs.astral.sh/uv/getting-started/installation/) for other installation options.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then, create a virtual environment:

```bash
uv venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Sync your virtual environment with the dependencies:

```bash
uv sync --extra dev
```

## Setting up your local database

The application expects a Postgres database to be running locally.

The following configuration is used, you can either set up your database to comply with these settings, or change the settings using the following env variables:

```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=postgres
```

## Running the application locally

To run the application locally, you can change into the `src` directory and run:

```bash
python main.py
```

This will start a local server that will connect to the database, and you can access the application at `http://localhost:7860`.

## Deploy to huggingface 🤗 spaces

### Compiling dependencies

Before a deploy, make sure to run this to compile the `uv` lock file to `requirements.txt` if you have made changes to the dependencies:

```bash
uv pip compile pyproject.toml -o src/requirements.txt
```

This will make sure that the dependencies in your `pyproject.toml` are compiled to the `requirements.txt` file, which is used by the huggingface space.

### Deploying to huggingface

Note that you need to set `HF_TOKEN` environment variable first.
This is personal, and must be created at [huggingface](https://huggingface.co/settings/tokens).
Make sure the token has `write` access.
Be aware that this will not delete existing files, only modify or add,
see [huggingface-cli](https://huggingface.co/docs/huggingface_hub/en/guides/upload#upload-from-the-cli) for more
information.

#### Update your space configuration

The `src/README.md` file contains the configuration for the space.
Feel free to update this file to match your own configuration - name, description, etc.

Note that we can actually use the `gradio` SDK of spaces, to serve FastHTML apps as well, as long as we serve the app on port `7860`.
See [Custom python spaces](https://huggingface.co/docs/hub/en/spaces-sdks-python) for more information.

#### Upload the files

To deploy, run

(Replace `vespa-engine/colpali-vespa-visual-retrieval` with your own huggingface user/repo name, does not need to exist beforehand)

```bash
huggingface-cli upload vespa-engine/colpali-vespa-visual-retrieval src . --repo-type=space
```

Note that we upload only the `src` directory.

## Development

This section applies if you want to make changes to the web app.

### Adding dependencies

To add dependencies, you can add them to the `pyproject.toml` file and run:

```bash
uv compile
```

and then sync the dependencies:

```bash
uv sync --extra dev
```

### Making changes to CSS

To make changes to output.css apply, run

```bash
shad4fast watch # watches all files passed through the tailwind.config.js content section

shad4fast build # minifies the current output.css file to reduce bundle size in production.
```

### Instructions on creating and feeding the full dataset

This section is only relevant if you want to create and feed the full dataset to Vespa.
The notebook referenced in the beginning of this readme should be sufficient if you just want to spin up a scaled down version of the demo.

#### Prepare data and Vespa application

First, install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then, run:

```bash
uv sync --extra dev --extra feed
```

#### Converting to notebook

If you want to run the `prepare_feed_deploy.py` as a notebook, you can convert it using `jupytext`:

Convert the `prepare_feed_deploy.py` to notebook to:

```bash
jupytext --to notebook prepare_feed_deploy.py
```

And launch a Jupyter instance with:

```bash
uv run --with jupyter jupyter lab
```

## Credits

Huge thanks to the amazing projects that made it a joy to create this demo 🙏🙌

- Freeing us from python dependency hell - [uv](https://astral.sh/uv/)
- Allowing us to build **beautiful** full stack web apps in Python [FastHTML](https://fastht.ml/)
- Introducing the ColPali architecture - [ColPali](https://huggingface.co/vidore/colpali-v1.2)
- Adding `shadcn` components to FastHTML - [Shad4Fast](https://www.shad4fasthtml.com/)
