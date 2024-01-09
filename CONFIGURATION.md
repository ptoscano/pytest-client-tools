# Configuration and common usecases
## Tests are run in upstream environment

Pytest will run local candlepin service in a container.

Dynaconf will load all configuration from a file `settings.toml`

```bash
$ export ENVIRONMENTS_FOR_DYNACONF=True
$ export ENV_FOR_DYNACONF=upstream
$
$ pytest -v
```
Pytest will run all tests that are available for `upstream`
environment.

There is a section `[upstream]` in the settings file that contains of
all properties that tests require.

## Tests are run in CI environment
Jenkins does not require dynaconf to use environments.
Jenkins provides all config properties directly - using environment
variables.

```bash
$ export ENVIRONMENTS_FOR_DYNACONF=False
$
$ pytest -v
```

## Tests are run in stage environment
Properties that describe a development environment must be stored in a
secret file that is not part of the repo. Default name of the file is
`.secrets.toml`

```bash
$ export ENVIRONMENTS_FOR_DYNACONF=True
$ export ENV_FOR_DYNACONF=stage
$
$ pytest -v
```

`stage` environment is used for most of the tests. It requires all
services to be available.

All properties are defined in a custom file `.secrets.toml` This file
is not part of this repo.

# Example of `.secrets.toml`

```toml
[stage.candlepin]
hostname=TO_BE_CONFIGURED

[stage.account]
username=TO_BE_REDACTED
password=TO_BE_REDACTED
```
