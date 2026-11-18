# RFC-0003: Spring Boot good practices

- **Status:** Proposed
- **Date:** 2026-11-18
- **Author:** Nikola Matkovic

## Summary

This RFC proposes a baseline set of good practices for Spring Boot services,
covering dependency injection style, configuration, layering, transactions,
validation, error handling, observability, and testing — so services built on
Spring Boot are consistent and reviewable regardless of which team wrote them.

## Motivation

Spring Boot's flexibility means the same problem (e.g. "inject a dependency",
"handle a validation error") can be solved several different ways in the same
codebase, which makes cross-team review and onboarding harder than it needs to
be. Codifying a default approach for the common cases reduces that variance
without blocking genuine exceptions.

## Proposed rules

- **Constructor injection only.** No field-level `@Autowired`. Constructor
  injection makes required dependencies explicit, supports immutability
  (`final` fields), and is trivially testable without a Spring context.
- **Externalize all configuration** via `application.yml` plus Spring
  profiles (`application-{profile}.yml`). Secrets are never hardcoded or
  committed — they come from environment variables or a secrets manager
  (e.g. Vault), injected at runtime.
- **Layer strictly: controller → service → repository.** Controllers are thin
  (request/response mapping only); business logic lives in services; data
  access lives in repositories. Use DTOs at the API boundary — never return
  JPA entities directly from a controller.
- **Scope `@Transactional` at the service layer**, with explicit, short
  boundaries. Avoid long-running transactions that hold DB connections/locks
  across calls to external systems.
- **Validate at the controller boundary** using `jakarta.validation`
  annotations (`@Valid`, `@NotNull`, etc.) on request DTOs — don't defer basic
  shape validation to the service layer.
- **Centralize exception handling** via `@ControllerAdvice` /
  `@ExceptionHandler`, returning a consistent error response shape across the
  whole service rather than ad hoc per-controller handling.
- **Enable Actuator endpoints for health/metrics, but restrict access** — they
  must not be publicly exposed without authentication; treat them like any
  other internal operational endpoint.
- **Prefer slice tests over broad `@SpringBootTest` usage.** Use
  `@WebMvcTest` for controller-layer tests, `@DataJpaTest` for repository-layer
  tests, and plain unit tests (no Spring context) for business logic in
  services. Reserve full `@SpringBootTest` for genuine integration tests,
  since it's the slowest option and a convenient default is to overuse it.

## Alternatives considered

- **Field injection for brevity.** Rejected: it hides required dependencies,
  makes classes harder to unit test without reflection tricks, and prevents
  `final` fields.
- **`@SpringBootTest` everywhere for simplicity.** Rejected: it's correct but
  slow at scale; a test suite that defaults to full-context tests becomes a
  CI bottleneck as the codebase grows.

## Related

None.
