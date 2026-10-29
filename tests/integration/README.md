# Live integration tests

No live integration tests or supported images exist in this release.
Default tests are offline and never connect to a device.

Before adding live tests, require an explicit opt-in, a separate lab inventory,
an exact device allowlist, credentials from a secret provider, and recorded image
versions. Verify read-only collection before adding any reversible write test.
Do not create a passing placeholder that implies live coverage.
