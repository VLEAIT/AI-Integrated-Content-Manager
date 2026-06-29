# AI-Integrated Content Manager
A high-performance, multi-tenant Content Management System (CMS) engineered to streamline organizational digital workflows and automate marketing pipelines using Generative AI.
## Features
* **Multi-Tenant Workspaces:** Complete isolation of team files, digital assets, and campaign data.
* **Granular RBAC:** Role-Based Access Control (`User`, `Workspace`, `Workspacealloc`) to secure enterprise data.
* **Hierarchical Content Engine:** Relational mapping (`PostMaster` to `PostChild`) for tracking campaigns and their platform-specific variants.
* **AI Content Generation:** Asynchronous LLM processing to turn raw data inputs into polished cross-platform copy.
## Tech Stack
* **Backend:** FastAPI (Python)
* **Database:** PostgreSQL (Hosted via Supabase)
* **Migrations:** Alembic
* **Authentication:** JWT (JSON Web Tokens) & Bcrypt Password Hashing

## Recent Updates
* Added authentication support with JWT token creation and validation.
* Added password hashing and verification using bcrypt.
* Added user/workspace/workspace allocation models with SQLAlchemy ORM.
* Added PostgreSQL database connection and session management.
* Added Alembic support for migrations and schema versioning.
* Added application initialization in `main.py` to create tables on startup.

