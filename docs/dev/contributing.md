# Contributing to the App

The project is packaged with a light [development environment](dev_environment.md) based on `docker-compose` to help with the local development of the project and to run tests.

The project is following Network to Code software development guidelines and is leveraging the following:

- Python linting and formatting: `black`, `pylint`, `bandit`, `flake8`, and `ruff`.
- YAML linting is done with `yamllint`.
- Django unit test to ensure the app is working properly.

Documentation is built using [mkdocs](https://www.mkdocs.org/). The [Docker based development environment](dev_environment.md#docker-development-environment) automatically starts a container hosting a live version of the documentation website on [http://localhost:8001](http://localhost:8001) that auto-refreshes when you make any changes to your local files.

## Creating Changelog Fragments

All pull requests to `next` or `develop` must include a changelog fragment file in the `./changes` directory. To create a fragment, use your GitHub issue number and fragment type as the filename. For example, `2362.added`. Valid fragment types are `added`, `changed`, `deprecated`, `fixed`, `removed`, and `security`. The change summary is added to the file in plain text. Change summaries should be complete sentences, starting with a capital letter and ending with a period, and be in past tense. Each line of the change fragment will generate a single change entry in the release notes. Use multiple lines in the same file if your change needs to generate multiple release notes in the same category. If the change needs to create multiple entries in separate categories, create multiple files.

!!! example

    **Wrong**
    ```plaintext title="changes/1234.fixed"
    fix critical bug in documentation
    ```

    **Right**
    ```plaintext title="changes/1234.fixed"
    Fixed critical bug in documentation.
    ```

!!! example "Multiple Entry Example"

    This will generate 2 entries in the `fixed` category and one entry in the `changed` category.

    ```plaintext title="changes/1234.fixed"
    Fixed critical bug in documentation.
    Fixed release notes generation.
    ```

    ```plaintext title="changes/1234.changed"
    Changed release notes generation.
    ```

## Branching Policy

Device Lifecycle App leverages a feature and develop branching strategy.  The default branch has been changed to the `develop` branch, and all feature branches should source from it.  Once a feature has been merged back into develop, it will be considered to merge into main along with other feature branches - which will ultimately lead to the next release.

## Release Policy

New versions of the Device Lifecycle App are based on the most recent PR's that have been merged into the develop branch.  A release can contain major or minor changes, as well as bug patches.  The product owner, and tech lead are responsible for determining when a group of PR's will be tagged and released.  In general, the maintainers follow the semantic release philosophy of Major, Minor, Patch release determination.
