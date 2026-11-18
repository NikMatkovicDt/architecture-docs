# RFC-0004: .NET good practices

- **Status:** Collecting Feedback
- **Authors:** Nikola Matkovic
- **Feedback Deadline:** 2026-12-02
- **Last Update:** 2026-11-18

## Summary

This RFC proposes a baseline set of good practices for .NET services, covering
dependency injection, async usage, configuration, API layering, EF Core data
access, error handling, nullability, and testing — so services built on .NET
are consistent and reviewable regardless of which team wrote them.

## Need

.NET offers several valid ways to solve the same problem (manual service
instantiation vs. DI, blocking vs. async calls, ad hoc config reads vs. the
options pattern), and the wrong choice in each case has a specific, well-known
failure mode in production (thread-pool starvation from blocked async calls,
N+1 queries from EF Core, inconsistent error shapes across endpoints).
Codifying the default approach prevents these recurring, avoidable problems.

## Approach

- **Use the built-in DI container (`IServiceCollection`) exclusively.** No
  static service-locator patterns or manually `new`-ed dependencies in
  application code — register and inject everything, which keeps components
  testable and swappable.
- **Async all the way through.** Once a call is `async`, every caller up the
  stack stays `async` to the entry point. Never call `.Result` or `.Wait()` on
  a task from synchronous code — this is a common source of thread-pool
  starvation and deadlocks, especially under load.
- **Configuration via the `IOptions<T>` pattern**, bound from
  `appsettings.json` / environment-specific overrides / environment variables.
  Secrets are never hardcoded or committed — use user-secrets locally and a
  secrets manager (e.g. Key Vault) or environment variables in deployed
  environments.
- **Keep controllers/minimal-API handlers thin.** Request/response mapping
  only; business logic lives in services, not in the HTTP layer.
- **EF Core: avoid N+1 queries explicitly.** Use `.Include()` or projections
  (`.Select()`) to shape exactly the data a query needs, and use
  `AsNoTracking()` for read-only queries to avoid unnecessary change-tracking
  overhead.
- **Centralize exception handling** via `UseExceptionHandler` middleware,
  returning a consistent `ProblemDetails` response shape across the whole
  service rather than per-endpoint try/catch blocks.
- **Enable nullable reference types project-wide** (`<Nullable>enable</Nullable>`)
  so the compiler surfaces potential null-reference issues at build time
  instead of at runtime.
- **Testing**: use xUnit, with `WebApplicationFactory` for integration tests
  against the full request pipeline. Mock only true external boundaries
  (e.g. a third-party HTTP client) — don't mock internal collaborators that
  could just as easily be exercised directly.

## Pros & Cons

Not recorded when this RFC was written.

## Alternatives

- **Blocking calls where "it's just one await" seems harmless.** Rejected:
  there's no reliably "safe" place to block on async code in a service
  handling concurrent requests; the rule is kept absolute rather than
  case-by-case to avoid relitigating it in every review.
- **Ad hoc `IConfiguration["Key:SubKey"]` reads instead of `IOptions<T>`.**
  Rejected: string-keyed config reads lose compile-time safety and scatter
  configuration shape knowledge across the codebase instead of centralizing
  it in typed option classes.

## Appendix / References

None.
