# pytest-client-tools

Plugin for `pytest` to test RHSM client tools: `subscription-manager`,
`insights-client`, and `rhc`.

## Requirements

- requests

## Installation

You can install it using `pip` from this git repository, i.e.

```bash
$ pip install git+https://github.com/ptoscano/pytest-client-tools@main
```

## Usage

It provides a set of fixtures for `pytest`, representing the various client tools
and some helper bits:
- `candlepin` -- a locally deployed Candlepin from sources with test data
- `external_candlepin` -- a remote Candlepin (requires a configuration pointing
  to it passed as `--test-config`)
- `any_candlepin` -- `external_candlepin` if available, otherwise `candlepin`
- `subman` -- `subscription-manager`
- `insights_client` -- `insights-client`
- `rhc` -- `rhc`

## Configuration

There is a fixture =test_config= in the defined fixtures.
It uses [Dynaconf library](https://dynaconf.com) to load configuration
properties.

It is necesary to set a few env variables to tell dynaconf what
properties source to use:

```bash
export SETTINGS_FILES_FOR_DYNACONF="['settings.toml','.secrets.yaml']"
export ENV_FOR_DYNACONF=stage
```

The default source of the properties to load is a shell environment.

The example above specifies that dynaconf 
- will load configuration from files `settings.toml` and `.secrets.yaml`
- will use a section `stage` to load all properties.

### Environments in settings properties

Dynaconf can provide you a different values of the properties
depending on a specified environment (is it `ENV_FOR_DYNACONF`
env variable).

an example of settings.yaml file:

```yaml
development:
  account:
    username: MY_NAME
	password: MY_PASSWORD
production:
  account:
    username: MY_PROD_NAME
	password: MY_PROD_PASSWORD
stage:
  account:
    username: MY_STAGE_NAME
	password: MY_STAGE_PASSWORD
```

Specifying an env var `ENV_FOR_DYNACONF` you tell dynaconf to use the
proper section to load properties.

## License

Distributed under the terms of the `MIT`_ license.
