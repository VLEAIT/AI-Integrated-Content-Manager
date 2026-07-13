# AI-Integrated Content Manager

A high-performance, multi-tenant Content Management System (CMS) engineered to streamline organizational digital workflows and automate marketing pipelines using Generative AI. Built on a strict multi-tenant architecture, this platform guarantees complete isolation across independent brand spaces while allowing frictionless, localized team collaboration.

## Features

* **Multi-Tenant Workspaces:** Complete logical isolation of team files, digital assets, and campaign data across distinct company profiles.
* **Granular Dual-Layer RBAC:** Fine-grained Role-Based Access Control that splits administrative capabilities between a user's global profile account tier (`User`) and their localized room-level clearances (`Workspacealloc`) to ensure zero scope creep.
* **Hierarchical Content Engine:** Relational mapping (`PostMaster` to `PostChild`) designed to track overarching master campaigns alongside their platform-specific variants.
* **AI Content Generation:** Asynchronous LLM processing pipelines built to transform raw structural data inputs into polished, cross-platform copy.

## Tech Stack

* **Backend:** FastAPI (Python 3.11+)
* **Database Object Mapping:** SQLAlchemy 2.0 (ORM)
* **Database:** PostgreSQL (Hosted via Supabase)
* **Validation & Schemas:** Pydantic v2
* **Migrations:** Alembic
* **Authentication:** OAuth2-compatible JWT (JSON Web Tokens) & Passlib Bcrypt Password Hashing

---

##  Architectural Core: Dual-Layer Security

To prevent data leakage when users collaborate across multiple organizations, the platform uses a junction bridge table (`Workspacealloc`). This decouples a user's account capabilities from their workspace contexts:

1. **Global Permissions (`User.role_type`):** Checked during top-level structural changes (e.g., Only users with a global status of `Role_type.owner` hold the account privileges required to register or spin up a new billing workspace container).
2. **Local Workspace Permissions (`Workspacealloc.allocated_role`):** Evaluated inside individual workspaces. If a global workspace `owner` is invited into a foreign workspace, their local allocation entry can downgrade them to a `sub_creator`, preventing administrative data tampering or settings modification inside that specific boundary.

---

## API Endpoint Layout

### 1. Authentication Router (`/auth`)
* Enforces strict cryptographic validation using modern `Annotated` dependency injection patterns.

| HTTP Method | API Route | Access Level | Operational Mechanics |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/register` | Public | Validates distinct email criteria, hashes plaintext credentials, and creates a new user record. |
| `POST` | `/auth/login` | Public | Validates user credentials against stored hashes and returns a bearer JWT token payload. |
| `PATCH` | `/auth/update` | Authenticated | Executes selective partial updates on fields like non-colliding custom usernames. |
| `PATCH` | `/auth/password_change` | Authenticated | Mandates an active identity password challenge prior to rewriting the secure hash. |

### 2. Workspace Router (`/workspace`)
* Manages workspace creation and workspace visibility for the authenticated user.

| HTTP Method | API Route | Access Level | Operational Mechanics |
| :--- | :--- | :--- | :--- |
| `POST` | `/workspace/create` | Global Owner | Assesses owner-tier privileges, creates the workspace row, and instantly links the creator as a workspace owner in the allocation table. |
| `GET` | `/workspace/my_workspace` | Authenticated | Returns the list of workspaces associated with the current user. |

### 3. Posts Router (`/workspace/{workspace_id}/post`)
* Supports workspace-scoped post submission, review, and content updates with AI-assisted caption generation.

| HTTP Method | API Route | Access Level | Operational Mechanics |
| :--- | :--- | :--- | :--- |
| `POST` | `/workspace/{workspace_id}/post/mega_submit` | Authenticated + Workspace Access | Creates a master post and child posts for each selected platform, sets an initial AI caption status, and queues a background task to generate the final AI caption from the raw description. |
| `GET` | `/workspace/{workspace_id}/post/post_list` | Authenticated + Workspace Access | Lists posts for a workspace with pagination using the query parameters `skip` and `limit` (defaults: `skip=0`, `limit=10`). |
| `PATCH` | `/workspace/{workspace_id}/post/child/{child_id}/approval` | Authenticated + Workspace Access | Updates the approval state of a child post. |
| `PUT` | `/workspace/{workspace_id}/post/child/{child_id}/content` | Authenticated + Workspace Access | Updates child-post content values such as boost budget and scheduled time. |
| `PUT` | `/workspace/{workspace_id}/post/master/{master_id}/content` | Authenticated + Workspace Access | Updates the master post content and triggers AI caption regeneration. |
| `DELETE` | `/workspace/{workspace_id}/post/{masterpost_id}` | Authenticated + Workspace Access | Deletes a master post from the workspace. |

> Background AI caption behavior: during `mega_submit`, the system stores an initial caption of `Processing via AI` and then runs a background task to replace it with generated text based on the post description.

---

##  Local Workspace Ignition

### Prerequisites

- Python 3.11 or newer
- PostgreSQL (or Supabase) connection for `DATABASE_URL`

### Environment Configuration
Create a `.env` file in the project root with the following values:

```env
DATABASE_URL=postgresql://your_user:your_password@your_supabase_host:5432/postgres
SECRET_KEY=your_super_secure_jwt_secret_signing_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Setup: Virtual Environment & Dependencies
Run the following commands to create and activate a virtual environment and install dependencies.

On macOS / Linux:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows (PowerShell):

```powershell
python -m venv venv
venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

### Run: Development Server
Start the app with Uvicorn for local development:

```bash
uvicorn main:app --reload
```

After the server starts, open the interactive API docs at http://127.0.0.1:8000/docs

-> Recent Implementation Updates
Core Authentication Architecture: Fully integrated secure user authentication workflows supported by state-backed JWT (JSON Web Tokens) token issuance, payload signing, and live signature validation.

Cryptographic Security Layers: Configured automated password mutation flows using Passlib with Bcrypt cryptographic hashing and secure reverse-verification checks.

Relational Database Mapping: Structured clean, decoupled object-relational models (User, Workspace, and Workspacealloc) using SQLAlchemy 2.0 ORM conventions.

Session Persistence Management: Provisioned thread-safe PostgreSQL relational database connection pools and scoped transactional session factories (get_db) targeting Supabase.

Database Version Control: Initialized Alembic migration environments to support automated schema tracking, versioning, and structural upgrading.

Lifecycle Initialization Locks: Configured unified startup application hooks inside main.py to handle automated table generation and metadata binds on initial server engine ignition.

Production-Grade Localized RBAC: Enhanced the Workspacealloc bridge table to include an explicit allocated_role structural column, laying the foundation for localized workspace security scopes and team collaboration pipelines.

Workspace and Post Management Flows: Expanded the API with workspace creation and listing endpoints, along with post submission, approval handling, and content update workflows that support AI caption generation in the background.