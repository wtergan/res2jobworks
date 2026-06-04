# Automation Package

Safe browser/source automation adapters live here.

Automation code is a client over core command contracts. It may capture source
text, preserve evidence metadata, and prepare draft/fill/review instructions,
but default behavior must stop before submission and must not store credentials,
cookies, session tokens, or browser profiles.

Current capture contracts are browser-free:

- `CapturedJobSource` carries reviewed visible job text and whitelisted evidence.
- `FixtureCaptureAdapter` provides a local fake adapter for tests and fixtures.
- `import_captured_job` feeds captured text into the core `jobs.import` workflow.
