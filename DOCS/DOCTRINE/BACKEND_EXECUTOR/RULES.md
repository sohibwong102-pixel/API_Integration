=============================

# RULES FOR BACKEND_EXECUTOR

=============================

- reusable > hardcoded
- modular > monolithic
- workflow-first architecture
- orchestration-friendly implementation
- business logic stays in services
- handlers are interaction adapters only
- workflows coordinate execution only
- prompts must remain centralized
- provider integration must stay abstracted
- maintain predictable dependency direction
- preserve loose coupling across layers
- prefer simple-first evolution
- avoid premature abstraction
- optimize for maintainability over cleverness
- implementation must remain interface-independent
- backend logic should survive platform migration
- scaling must remain incremental and low-risk
- every module should have clear responsibility
- every workflow should have predictable flow
- continuation flow must remain explicit
- hidden orchestration behavior is forbidden
