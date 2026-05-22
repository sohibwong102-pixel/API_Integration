=================

# WARNING_SIGNALS

=================
warn if:

- service becomes dependency for too many modules
- workflow becomes deeply nested
- orchestration logic spreads across layers
- provider-specific logic leaks outside provider layer
- handlers start containing business logic
- prompt duplication appears
- workflow state becomes implicit
- utils become business-logic containers
- abstraction complexity grows faster than feature complexity
- service branching becomes excessive
- dependency direction becomes unclear
- continuation flow becomes difficult to trace
- workflow lifecycle becomes unpredictable
- provider routing becomes tightly coupled
- reusable logic becomes duplicated
- module responsibility becomes ambiguous
- orchestration behavior becomes hidden
- backend portability starts decreasing
- architecture readability starts degrading
