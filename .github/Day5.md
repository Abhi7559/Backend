# Exercise: Film Review Platform — Alembic Migrations + Data Seeding

## Goal

Implement production-style database migrations and repeatable seed data for the existing Film Review Platform.

The project already has SQLAlchemy ORM models, an async database engine/session, Pydantic schemas, and FastAPI routes.

Do not rebuild the project from scratch.

First inspect the existing project structure, configuration, database setup, ORM models, and naming conventions. Reuse the existing architecture and make only the changes required for this exercise.

---

# 1. Requirements

Implement all of the following:

1. Configure Alembic for the existing async SQLAlchemy database.
2. Configure Alembic autogeneration using the application's SQLAlchemy ORM metadata.
3. Generate an initial migration containing the existing:

   * User table
   * Film table
   * Review table
4. Manually verify the generated migration and correct it if necessary.
5. Apply the initial migration.
6. Add a new Watchlist ORM model representing a many-to-many relationship between users and films.
7. Generate a second migration for the Watchlist table.
8. Do not modify the first migration after the second migration is created.
9. Apply the second migration.
10. Create an idempotent async seed script.
11. Seed at least:

    * 10 films
    * 3 users with distinct roles
    * 5 reviews
12. Running the seed script multiple times must not create duplicate records.
13. Add a clear setup comment block at the top of the seed script explaining the complete setup flow from an empty database.
14. Verify the complete migration and seeding workflow.

---

# 2. Important Project Rules

Before making changes:

* Inspect the existing project.
* Identify the current SQLAlchemy `Base`.
* Identify all existing ORM models.
* Identify the async engine.
* Identify the async session factory.
* Identify the existing configuration/settings class.
* Identify the current database URL configuration.
* Identify the existing package/module structure.

Do not create duplicate database engines or session factories.

Do not create a second unrelated configuration system.

Reuse the existing database configuration and async session infrastructure wherever possible.

Do not replace the existing architecture.

Do not introduce unnecessary dependencies.

Follow the existing project's coding style.

---

# 3. Alembic Configuration

Configure Alembic to work with the existing async SQLAlchemy setup.

The Alembic environment must:

* Use the project's database URL.
* Support the async PostgreSQL driver already used by the application.
* Import the application's ORM models before reading metadata.
* Set:

```python
target_metadata = Base.metadata
```

or the equivalent metadata object used by the existing project.

Make sure all ORM models are imported so Alembic can detect their tables.

Do not use `Base.metadata.create_all()` for application database initialization.

The database schema must be managed through Alembic migrations.

---

# 4. Initial Migration

Create the first migration using Alembic autogeneration.

Use a meaningful migration message such as:

```text
create initial film review tables
```

The migration should contain the three existing tables:

```text
users
films
reviews
```

The generated migration must correctly reflect the existing ORM models.

Verify:

* Primary keys
* Foreign keys
* Column names
* Column types
* Nullable constraints
* Unique constraints
* Required indexes
* Default values
* Timestamp columns
* Relationships represented at the database level

Do not blindly trust autogeneration.

Open and review the generated migration before applying it.

If Alembic generates anything incorrect, fix the migration file manually.

Do not modify the ORM models just to make the generated migration look correct unless the ORM model itself is incorrect.

---

# 5. Apply Initial Migration

After reviewing the migration, apply it with:

```bash
alembic upgrade head
```

Verify that the database contains:

```text
users
films
reviews
alembic_version
```

The `alembic_version` table should contain the currently applied migration revision.

---

# 6. Watchlist Model

Add a new ORM model:

```text
Watchlist
```

It represents a many-to-many relationship between users and films.

Conceptually:

```text
User
  |
  | 1
  |
  | many
Watchlist
  |
  | many
  |
  | 1
Film
```

The Watchlist table should contain at least:

```text
user_id
film_id
```

Both columns must reference the appropriate parent tables using foreign keys.

Prevent duplicate user-film combinations.

Prefer an appropriate composite primary key or unique constraint such as:

```text
(user_id, film_id)
```

Follow the existing project's SQLAlchemy style.

Do not unnecessarily change the existing User or Film models.

---

# 7. Second Migration

After adding the Watchlist model, generate a second migration.

Use a meaningful migration message such as:

```text
add watchlist table
```

The migration history must look like:

```text
001_initial_tables
        ↓
002_add_watchlist
```

The second migration must only add the Watchlist-related schema.

IMPORTANT:

Do NOT edit or rewrite the first migration after creating the second migration.

Migration history must remain incremental and reviewable.

The second migration must contain both:

```python
def upgrade():
```

and:

```python
def downgrade():
```

The downgrade should remove the Watchlist table and its related constraints.

---

# 8. Apply Second Migration

Run:

```bash
alembic upgrade head
```

Verify that the database now contains:

```text
users
films
reviews
watchlist
alembic_version
```

Verify that the current Alembic revision is the second migration.

---

# 9. Seed Script

Create an async seed script in the existing application package.

Prefer the existing project structure. For example:

```text
app/
    seed.py
```

If the project already has a dedicated scripts/commands package, use that instead.

The seed script must use the existing async SQLAlchemy session infrastructure.

Do not create another database engine unless absolutely required by the existing architecture.

---

# 10. Seed Data

The seed script must insert at least:

## Users

Create at least 3 users.

Each user must have a distinct role.

Example:

```text
admin
reviewer
member
```

Use valid values according to the project's existing User model and role definitions.

Do not store plaintext passwords if the existing application architecture expects password hashes.

If password hashes are required, use the project's existing password hashing utility.

Do not invent a second password hashing implementation.

---

## Films

Create at least 10 films.

Use realistic data.

The films must cover at least 3 different genres.

For example:

```text
Sci-Fi
Drama
Action
```

Use values compatible with the existing Film model.

---

## Reviews

Create at least 5 reviews.

Each review must:

* Reference an existing film.
* Reference an existing user.
* Have a valid rating.
* Have a valid review body.
* Follow all existing database constraints.

If the existing Review model requires a minimum review length, satisfy it.

If the model has timestamp fields, populate them appropriately.

---

# 11. Idempotent Seeding

The seed script MUST be idempotent.

This means:

```text
First run:
10 films
3 users
5 reviews

Second run:
10 films
3 users
5 reviews
```

NOT:

```text
Second run:
20 films
6 users
10 reviews
```

Before inserting each seed record, check whether the corresponding record already exists.

Use stable identifying fields.

For example:

Users:

```text
email
```

Films:

```text
title + release year
```

or another appropriate unique identifier based on the existing schema.

Reviews:

Use an appropriate stable combination such as:

```text
user_id + film_id
```

if the application allows only one review per user per film.

Do not depend on randomly generated IDs to detect duplicates.

If records already exist, reuse them instead of creating duplicates.

---

# 12. Seed Transaction Handling

Use the existing async session.

The seed flow should be conceptually:

```text
Create async session
        ↓
Find/create users
        ↓
Find/create films
        ↓
Find/create reviews
        ↓
Commit transaction
        ↓
Close session
```

Use proper transaction handling.

If an error occurs, rollback the transaction and display a meaningful error.

Do not leave the session open.

---

# 13. Seed Script Comment Block

At the very top of the seed script, add a clear documentation comment block.

It must explain the complete setup process starting from an empty database.

Use the actual commands appropriate for this project.

Example format:

```python
"""
Film Review Platform - Database Seed

Setup from an empty database:

1. Start PostgreSQL.

2. Configure the database URL in the project's environment configuration.

3. Apply all database migrations:

   alembic upgrade head

4. Run the seed script:

   python -m app.seed

5. Run the seed script again to verify idempotency:

   python -m app.seed

Expected final state:

- At least 10 films
- At least 3 users with distinct roles
- At least 5 reviews
- Watchlist table exists
- Running the seed script multiple times does not create duplicates
"""
```

Adjust the commands if the project's actual module/package structure requires a different command.

---

# 14. Meaningful Console Output

The seed script should print useful, human-readable messages.

For example:

```text
Starting database seed...
Creating users...
Creating films...
Creating reviews...
Committing seed data...
Database seed completed successfully.
```

When a record already exists, the output should make that clear.

For example:

```text
User admin@example.com already exists. Skipping.
Film Inception already exists. Skipping.
```

At the end, print a useful summary such as:

```text
Seed completed successfully.

Users: 3
Films: 10
Reviews: 5
```

Do not use meaningless output such as:

```text
done
success
abc
test
```

---

# 15. Verification

After implementation, verify the following.

## Migration verification

From an empty database:

```bash
alembic upgrade head
```

Verify both migrations are applied in order.

Verify:

```text
users
films
reviews
watchlist
```

exist.

---

## Seed verification

Run:

```bash
python -m app.seed
```

Verify:

```text
Users >= 3
Films >= 10
Reviews >= 5
```

Verify films contain at least 3 genres.

Verify users have distinct roles.

---

## Idempotency verification

Run:

```bash
python -m app.seed
```

again.

Verify that the record counts do not increase.

The second execution must not create duplicate seed records.

---

## Migration history verification

Use:

```bash
alembic history
```

and:

```bash
alembic current
```

Confirm that the migration chain is:

```text
initial migration
        ↓
watchlist migration
```

Confirm that the first migration file was not modified after the second migration was created.

---

# 16. Downgrade Verification

Verify the second migration can be rolled back.

Run:

```bash
alembic downgrade -1
```

Confirm that:

```text
watchlist
```

is removed.

Then restore the latest schema:

```bash
alembic upgrade head
```

Confirm that:

```text
watchlist
```

exists again.

Do not destroy the initial migration.

---

# 17. Code Quality Requirements

Keep the implementation simple and beginner-friendly.

Use:

* Existing project architecture
* Existing async engine
* Existing async session
* Existing settings/configuration
* Existing ORM Base
* Existing models and enums
* Existing utilities

Avoid:

* Duplicate database configuration
* Duplicate session factories
* `Base.metadata.create_all()`
* Synchronous database code inside the async application
* Hardcoded database URLs
* Hardcoded secrets
* Random IDs for idempotency checks
* Unnecessary dependencies
* Unnecessary refactoring
* Modifying unrelated files

Use meaningful names.

Add type hints where they fit the existing project style.

---

# 18. Final Expected Structure

After implementation, the relevant structure should look approximately like:

```text
project/
│
├── alembic/
│   ├── versions/
│   │   ├── <revision>_create_initial_film_review_tables.py
│   │   └── <revision>_add_watchlist_table.py
│   │
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── models/
│   │   ├── user.py
│   │   ├── film.py
│   │   ├── review.py
│   │   └── watchlist.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── config.py
│   └── seed.py
│
├── alembic.ini
├── pyproject.toml
└── .env
```

Do not force this exact structure if the existing project already uses a different valid architecture. Follow the existing structure instead.

---

# 19. Final Acceptance Checklist

Before finishing, verify every item:

* [ ] Alembic is installed/configured.
* [ ] Alembic works with the async database engine.
* [ ] Alembic uses the application's ORM metadata.
* [ ] All ORM models are imported for autogeneration.
* [ ] Initial migration creates User, Film, and Review tables.
* [ ] Initial migration was manually reviewed.
* [ ] Initial migration was applied successfully.
* [ ] Watchlist ORM model was added.
* [ ] Watchlist represents User ↔ Film many-to-many relationship.
* [ ] Watchlist prevents duplicate user-film pairs.
* [ ] Second migration adds only Watchlist.
* [ ] First migration was not modified after the second migration was created.
* [ ] Second migration was applied successfully.
* [ ] Seed script uses the async database session.
* [ ] Seed script creates at least 10 films.
* [ ] Films cover at least 3 genres.
* [ ] Seed script creates at least 3 users.
* [ ] Users have distinct roles.
* [ ] Seed script creates at least 5 reviews.
* [ ] Seed script is idempotent.
* [ ] Running seed twice creates no duplicates.
* [ ] Seed script has setup instructions in its top comment block.
* [ ] Migration history is correct.
* [ ] `alembic current` shows the latest migration.
* [ ] Second migration can be downgraded.
* [ ] Latest migration can be applied again successfully.
* [ ] No unrelated project files were unnecessarily changed.

---

# 20. Important Instruction for Antigravity

Do not simply generate files based on assumptions.

First inspect the existing codebase and determine:

1. Where `Base` is defined.
2. Where the async engine is defined.
3. Where the async session factory is defined.
4. Where User, Film, and Review models are defined.
5. How configuration/settings are currently loaded.
6. What database URL format is currently used.
7. What existing enums and constraints are used by the models.

Then implement the migration and seed workflow using those existing components.

After implementation, run the relevant commands and fix errors instead of stopping after generating code.

At the end, provide a concise summary containing:

* Files created
* Files modified
* Migration revisions created
* Commands executed
* Database verification results
* Seed verification results
* Idempotency verification results
* Any assumptions or issues that could not be verified
