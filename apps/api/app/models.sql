create table if not exists users (
  id uuid primary key,
  email text not null unique,
  name text not null,
  created_at timestamptz not null default now()
);

create table if not exists organizations (
  id uuid primary key,
  name text not null,
  created_at timestamptz not null default now()
);

create table if not exists incidents (
  id text primary key,
  organization_id uuid references organizations(id),
  title text not null,
  severity text not null,
  status text not null,
  root_cause text,
  confidence int,
  started_at timestamptz not null,
  resolved_at timestamptz
);

create table if not exists telemetry_events (
  id uuid primary key,
  incident_id text references incidents(id),
  service_name text not null,
  metric_name text not null,
  metric_value numeric not null,
  severity text not null,
  observed_at timestamptz not null default now()
);

create table if not exists deployments (
  id uuid primary key,
  organization_id uuid references organizations(id),
  service_name text not null,
  version text not null,
  commit_sha text,
  deployed_at timestamptz not null
);

create table if not exists ai_analysis (
  id uuid primary key,
  incident_id text references incidents(id),
  agent_name text not null,
  finding text not null,
  confidence int not null,
  created_at timestamptz not null default now()
);

create table if not exists recovery_actions (
  id uuid primary key,
  incident_id text references incidents(id),
  action text not null,
  risk text not null,
  status text not null,
  approved_by uuid references users(id),
  created_at timestamptz not null default now()
);

create table if not exists service_topology (
  id uuid primary key,
  organization_id uuid references organizations(id),
  source_service text not null,
  target_service text not null,
  relation text not null default 'depends_on'
);

create table if not exists memory_embeddings (
  id uuid primary key,
  organization_id uuid references organizations(id),
  source_type text not null,
  source_id text not null,
  summary text not null,
  embedding_ref text not null,
  created_at timestamptz not null default now()
);
