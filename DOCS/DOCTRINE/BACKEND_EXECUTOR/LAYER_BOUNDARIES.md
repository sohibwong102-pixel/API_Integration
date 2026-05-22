==================

# LAYER_BOUNDARIES

==================

## handlers/

responsibility:

- interaction adapter
- request parsing
- response formatting
- FSM trigger
- execution trigger

forbidden:

- reusable business logic
- orchestration complexity
- provider routing logic
- database workflow
- heavy AI processing

---

## workflows/

responsibility:

- orchestration coordination
- sequence management
- continuation flow
- execution lifecycle

forbidden:

- transport protocol handling
- UI logic
- provider implementation logic
- heavy reusable business logic
- hidden state mutation

---

## services/

responsibility:

- reusable business logic
- AI integration
- provider execution
- reusable processing layer

forbidden:

- HTTP layer handling
- workflow coordination
- Telegram interaction
- response presentation logic

---

## prompts/

responsibility:

- centralized prompt storage
- reusable prompt templates
- prompt consistency

forbidden:

- business logic
- orchestration logic
- workflow state handling

---

## storage/

responsibility:

- persistence layer
- history storage
- storage abstraction

forbidden:

- orchestration logic
- workflow coordination
- direct API behavior
- provider execution

---

## utils/

responsibility:

- helper utilities
- isolated reusable helpers

forbidden:

- orchestration ownership
- business workflow ownership
- hidden shared state
- dumping ground behavior
