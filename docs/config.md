# Configuration

pytest-client-tools uses [Dynaconf][dynaconf] for reading the configuration
for the tests. Please check its website for more details on it, including its
internals.

The configuration uses the Dynaconf environments, and `default` is the default
environment.

The `PYTEST_CLIENT_TOOLS` prefix is set for tweaking the Dynaconf configuration
using environment variables.

The format for the configuration file is [TOML][toml]; allowed file names for it
are `settings.toml`, and `.secrets.toml`.

The configuration file is optional; if not specified, pytest-client-tools
disables certain features or falls back to default values.

## Reference

This is an example of the available configuration keys:

```toml
[default]
candlepin.host = "candlepin-hostname"
candlepin.port = 443
candlepin.prefix = "/candlepin-prefix"
candlepin.insecure = false
candlepin.username = "candlepin-username"
candlepin.password = "candlepin-password"
candlepin.activation_keys = ["activation-key-1", "activation-key-2"]
candlepin.org = "candlepin-organization"
candlepin.environments = ["environment-1", "environment-2"]
insights.legacy_upload = false
```

The various keys are grouped depending on their area; here follows the
explanation of each key, with the type of its value:

- `candlepin.host` (string)

    The hostname of the external Candlepin server.

- `candlepin.port` (number)

    The port of the external Candlepin server. Since it is a port number,
    it must be greater than 0 and less than 65536.

- `candlepin.prefix` (string)

    The prefix (starting with `/`) of the external Candlepin server.

- `candlepin.insecure` (boolean)

    This specifies whether to disable the validation of the SSL certificate
    of the external Candlepin server.

- `candlepin.username` (string)

    The username to use for registration to the external Candlepin server.

- `candlepin.password` (string)

    The password to use for registration to the external Candlepin server.

- `candlepin.activation_keys` (list of strings)

    The activation keys to use for registration to the external Candlepin
    server.

- `candlepin.org` (string)

    The organization to use for registration to the external Candlepin server.

- `candlepin.environments` (list of strings)

    The environments to use for registration to the external Candlepin server.

- `insights.legacy_upload` (boolean)

    Whether to set the `legacy_upload` configuration option for
    `insights-client` by default when a new instance of the `insights_client`
    fixture is returned. If not set, the value previous set in
    `insights-client.conf` is not changed.

[dynaconf]: https://www.dynaconf.com/ "Dynaconf"
[toml]: https://toml.io/ "TOML"
