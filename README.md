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
The library provides dynaconf object to load all config properties
required by tests. see  [Dynaconf library](https://dynaconf.com) for
more details.

There are a few cases the library can be used at
1) upstream environment
2) CI environment
3) stage environment
4) production environment

For more details see [Configuration](CONFIGURATION.md)

## License

Distributed under the terms of the `MIT`_ license.
