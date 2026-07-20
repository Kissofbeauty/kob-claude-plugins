# FastAPI SQL Database Reference (SQLModel)

## Installation

```bash
pip install sqlmodel
```

## Multiple Models Pattern

```python
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query

# 1. Base — shared fields (no table, no secrets)
class PipelineJobBase(SQLModel):
    name: str = Field(index=True)
    source: str
    destination: str
    schedule: str | None = None
    is_active: bool = True

# 2. Table model — actual DB table (add secret fields here)
class PipelineJob(PipelineJobBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    api_key: str           # never exposed to clients

# 3. Public — response (no secrets)
class PipelineJobPublic(PipelineJobBase):
    id: int

# 4. Create — what clients send
class PipelineJobCreate(PipelineJobBase):
    api_key: str           # client sends this

# 5. Update — all optional for PATCH
class PipelineJobUpdate(SQLModel):
    name: str | None = None
    source: str | None = None
    destination: str | None = None
    schedule: str | None = None
    is_active: bool | None = None
    api_key: str | None = None
```

## Engine & Session Dependency

```python
# SQLite (dev)
sqlite_url = "sqlite:///pipeline.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

# PostgreSQL (production)
# engine = create_engine("postgresql://user:password@localhost/dbname")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
```

## Lifespan Integration

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()   # Create tables at startup
    yield

app = FastAPI(lifespan=lifespan)
```

## Full CRUD Endpoints

```python
# CREATE
@app.post("/jobs/", response_model=PipelineJobPublic, status_code=201)
def create_job(job: PipelineJobCreate, session: SessionDep):
    db_job = PipelineJob.model_validate(job)
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job

# READ ALL (paginated)
@app.get("/jobs/", response_model=list[PipelineJobPublic])
def read_jobs(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return session.exec(select(PipelineJob).offset(offset).limit(limit)).all()

# READ ONE
@app.get("/jobs/{job_id}", response_model=PipelineJobPublic)
def read_job(job_id: int, session: SessionDep):
    job = session.get(PipelineJob, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# UPDATE (partial PATCH)
@app.patch("/jobs/{job_id}", response_model=PipelineJobPublic)
def update_job(job_id: int, job: PipelineJobUpdate, session: SessionDep):
    db_job = session.get(PipelineJob, job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    update_data = job.model_dump(exclude_unset=True)  # only changed fields
    db_job.sqlmodel_update(update_data)
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job

# DELETE
@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, session: SessionDep):
    job = session.get(PipelineJob, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    session.delete(job)
    session.commit()
    return {"ok": True}
```

## Filter & Query

```python
from sqlmodel import select

# Filter
statement = select(PipelineJob).where(PipelineJob.is_active == True)
jobs = session.exec(statement).all()

# Multiple conditions
statement = select(PipelineJob).where(
    PipelineJob.source == "s3",
    PipelineJob.is_active == True,
)

# Order
statement = select(PipelineJob).order_by(PipelineJob.name)

# Join (with relationships)
statement = select(PipelineJob, RunLog).join(RunLog, PipelineJob.id == RunLog.job_id)
```

## Relationships

```python
from sqlmodel import Relationship

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    pipelines: list["PipelineJob"] = Relationship(back_populates="team")

class PipelineJob(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="pipelines")
```

## Production Tips

```python
# PostgreSQL engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,   # detect stale connections
)
```

**Checklist:**
- Use PostgreSQL for production (not SQLite)
- Use hand-written SQL migrations for schema changes (team standard — see `skill-data-modeling` / `skill-sql` · do NOT use Alembic)
- Always paginate list endpoints (`offset` + `limit`)
- Always check existence before update/delete
- Use `exclude_unset=True` for all PATCH operations
- Separate `Create`, `Public`, `Update` models — never expose secrets
