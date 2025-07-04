# caremo-be

## Cotrolerr-Routes

```
        CLIENT REQUEST
              │
              ▼
          [ROUTE Layer]
🛣️ Defines endpoint paths & HTTP verbs
🧠 Calls appropriate controller function
              │
              ▼
      [CONTROLLER Layer]
🎯 Handles input validation, request orchestration
🧠 Calls service layer for business logic
              │
              ▼
         [SERVICE Layer]
⚙️ Contains business logic
🧠 Calls repository for data access
              │
              ▼
     [REPOSITORY Layer]
🗃️ Abstracts DB access (SQLAlchemy, ORM, raw SQL)
🧠 Returns models/data
              │
              ▼
         [DATABASE Layer]
🔗 SQLAlchemy engine/session handles DB calls
```

## Repository Pattern

