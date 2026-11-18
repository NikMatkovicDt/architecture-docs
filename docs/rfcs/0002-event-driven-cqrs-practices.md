# RFC-0002: Event-driven architecture & CQRS good practices

- **Status:** Proposed
- **Date:** 2026-11-18
- **Author:** Nikola Matkovic

## Summary

This RFC proposes a baseline set of practices for services that adopt an
event-driven architecture and/or CQRS (Command Query Responsibility
Segregation), so that teams reaching for these patterns converge on
consistent, debuggable designs instead of each reinventing the hard parts
(idempotency, schema evolution, failure handling) independently.

## Motivation

CQRS and event-driven designs solve real problems — read/write scaling
divergence, decoupling producers from consumers, auditability — but they also
introduce failure modes that don't exist in a simple CRUD service: duplicate
event delivery, consumers that fall behind, event schemas that need to change
without breaking existing consumers, and eventual consistency that's easy to
accidentally hide from users until it causes confusion. Without agreed
practices, each team re-derives these the hard way, usually after an incident.

## Proposed rules

- **Separate command and query models explicitly.** Commands mutate state and
  return only acknowledgement/identifiers, never query results. Queries never
  mutate state. Don't let a single model/endpoint do both.
- **Event handlers must be idempotent.** Consumers will see duplicate
  deliveries (at-least-once delivery is the norm) — dedupe by a stable event
  id before applying side effects, rather than assuming exactly-once delivery.
- **Event schemas evolve additively only.** New fields may be added with
  sensible defaults; existing fields are never removed or repurposed. Old
  events must still be readable by current consumers (upcast at the read
  boundary if the in-memory representation needs to change).
- **Failed event processing needs an explicit policy**, not a silent drop: a
  bounded retry with backoff, then a dead-letter queue/table that's actually
  monitored, not just a sink nothing ever looks at.
- **Eventual consistency must be surfaced, not hidden.** If a read model can
  lag behind the write that produced it, the API/UI must make that
  observable (e.g. a "processing" state, a version/sequence number the client
  can poll for) rather than presenting stale reads as if they were current.
- **Propagate a correlation/trace id** from the originating command through
  every event and projection it produces, so a single business operation can
  be followed end-to-end across asynchronous boundaries.

## Alternatives considered

- **Leave this to each team's judgment.** Rejected: the failure modes above
  (duplicate delivery, silent event-schema breaks, hidden staleness) are
  consistently the source of production incidents in event-driven systems,
  and are cheap to prevent up front but expensive to retrofit.
- **Mandate full event sourcing (event log as sole source of truth) for every
  case.** Rejected as too prescriptive: CQRS without event sourcing (normal
  write DB + projected read models) is a legitimate, simpler option; this RFC
  doesn't require event sourcing, only that *if* events are used as an
  integration/audit mechanism, they follow the rules above.

## Related

None.
