```mermaid
graph TD
    classDef client fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff;
    classDef backend fill:#2ecc71,stroke:#27ae60,stroke-width:2px,color:#fff;
    classDef database fill:#f1c40f,stroke:#f39c12,stroke-width:2px,color:#000;
    classDef external fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff;

    %% Elements
    Creator[ Sub-Creator / Creator]:::client
    Owner[ Agency Owner]:::client
    FastAPI[ FastAPI Backend Engine]:::backend
    Pydantic[ Pydantic Guard]:::backend
    DB[(PostgreSQL Database)]:::database
    BackgroundQueue[ FastAPI Background Tasks]:::backend
    SocialAPI[ TikTok / Instagram API]:::external

    %% Workflows
    Owner -->|1. Creates Client Box & Configures Approval Switch| FastAPI
    FastAPI -->|Saves Workspace Settings| DB
    
    Creator -->|2. HTTP POST /api/v1/posts<br>Uploads Holiday Template or Video| FastAPI
    FastAPI -->|Runs Validation Checks| Pydantic
    Pydantic -->|Valid Payload Shapes| DB
    
    FastAPI -->|3. Database Query: Check Authorization & RLS| DB
    DB -->|Returns: requires_approval Status & Scopes| FastAPI
    
    FastAPI -->|4. Conditional Logic Branch| Check{Is Approval Required?}
    Check -->|YES: Status = Pending| DB
    Check -->|NO: Status = Approved| BackgroundQueue
    
    BackgroundQueue -->|5. Streams Asset Async over Internet| SocialAPI
