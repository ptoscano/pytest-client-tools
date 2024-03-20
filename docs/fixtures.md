# Fixtures

pytest-client-tools provides a number of fixtures for pytest.

### `candlepin`

This fixture signals that the test requires the Candlepin server, and in
particular an upstream Candlepin.

The type of the fixture is the [`Candlepin`][pytest_client_tools.candlepin.Candlepin]
class.

This fixture has a "session" scope.

This fixture cannot be used together with the `external_candlepin` &
`any_candlepin` fixtures.

The usage of this fixture to a test automatically adds a `candlepin` marker
to that test.

### `external_candlepin`

This fixture signals that the test requires the Candlepin server, and in
particular an external Candlepin server whose details are in the configuration.

This fixture requires details of a Candlepin server set up in the configuration,
and if a server is not fully configured then this fixture will skip the test
automatically. The configuration keys that are needed for this are:

- `candlepin.host`,
- `candlepin.port`
- `candlepin.prefix`
- either of:
    - `candlepin.username` and `candlepin.password`
    - `candlepin.activation_keys` and `candlepin.org`

The type of the fixture is the [`Candlepin`][pytest_client_tools.candlepin.Candlepin]
class.

This fixture has a "session" scope.

This fixture cannot be used together with the `candlepin` & `any_candlepin`
fixtures.

The usage of this fixture to a test automatically adds a `external_candlepin`
marker to that test.

### `any_candlepin`

This fixture signals that the test requires a Candlepin server, and it does not
matter which (upstream with test data, or external).

If an external Candlepin is available, then it will be used as object of this
fixture (i.e. it will be the same as `external_candlepin`); otherwise, the
upstream Candlepin will be used (i.e. it will be the same as `candlepin`).

The type of the fixture is the [`Candlepin`][pytest_client_tools.candlepin.Candlepin]
class.

This fixture has a "session" scope.

This fixture cannot be used together with the `candlepin` & `external_candlepin`
fixtures.

The usage of this fixture to a test automatically adds a `any_candlepin` marker
to that test.

### `subman`

This fixture signals that the test uses `subscription-manager`.

When a Candlepin fixture (`candlepin`, `external_candlepin`, `any_candlepin`)
is used together with the `subman` fixture in a test, then the `subman` fixture
will automatically configure its `SubscriptionManager` object to register to the
`Candlepin` object of the Candlepin fixture.

The system is unregistered when the fixture gets out of scope, i.e. when a test
finishes its execution.

The type of the fixture is the
[`SubscriptionManager`][pytest_client_tools.subscription_manager.SubscriptionManager]
class.

This fixture has a "function" scope.

In case the `subman_session` fixture is used when this fixture is used, then
its behaviour changes:

- there is no more automatic configuration of the `SubscriptionManager` object,
  as the object provided by `subman_session` will have already done its own
  configuration
- the system is no more unregistered at the end of the scope of this fixture

which means that thix fixture is still usable to interact with
`subscription-manager`; in this case, there should be care about not
unregistering during a test, otherwise it breaks the assumptions that tests
have when using the `subman_session` fixture.

The usage of this fixture to a test automatically adds a `subman` marker
to that test.

### `subman_session`

This fixture is equivalent to the `subman` fixture, and the only difference is
the "session" scope; because of this, the unregistration of the system happens
at the end of the test session.

When used, this modifies how the `subman` fixture behaves; please check the
documentation of that fixture for more details.

### `insights_client`

This fixture signals that the test uses `insights-client`.

The type of the fixture is the
[`InsightsClient`][pytest_client_tools.insights_client.InsightsClient]
class.

The usage of this fixture to a test automatically adds a `insights_client`
marker to that test.

### `rhc`

This fixture signals that the test uses `rhc`.

The type of the fixture is the [`Rhc`][pytest_client_tools.rhc.Rhc] class.

The usage of this fixture to a test automatically adds a `rhc` marker to that
test.

### `test_config`

This fixture provides the configuration used for the tests.

The type of the fixture is the
[`TestConfig`][pytest_client_tools.test_config.TestConfig] class.

