CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT NOT NULL,
  university TEXT,
  timezone TEXT NOT NULL DEFAULT 'Asia/Kolkata',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE oauth_accounts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider TEXT NOT NULL,
  provider_subject TEXT NOT NULL,
  encrypted_access_token BYTEA,
  encrypted_refresh_token BYTEA,
  scopes TEXT[] NOT NULL DEFAULT '{}',
  expires_at TIMESTAMPTZ,
  UNIQUE(provider, provider_subject)
);

CREATE TABLE courses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  code TEXT NOT NULL,
  name TEXT NOT NULL,
  faculty TEXT,
  credits NUMERIC(3,1),
  UNIQUE(user_id, code)
);

CREATE TABLE attendance_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  attended INT NOT NULL DEFAULT 0,
  total INT NOT NULL DEFAULT 0,
  minimum_percent NUMERIC(5,2) NOT NULL DEFAULT 75,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  course_id UUID REFERENCES courses(id),
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'todo',
  priority INT NOT NULL CHECK(priority BETWEEN 1 AND 100),
  deadline TIMESTAMPTZ,
  estimated_minutes INT NOT NULL DEFAULT 60,
  difficulty INT NOT NULL DEFAULT 3 CHECK(difficulty BETWEEN 1 AND 5),
  energy_required INT NOT NULL DEFAULT 3 CHECK(energy_required BETWEEN 1 AND 5),
  risk_level TEXT NOT NULL DEFAULT 'medium',
  source TEXT NOT NULL DEFAULT 'manual',
  confidence NUMERIC(4,3) NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE TABLE deadlines (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  course_id UUID REFERENCES courses(id),
  title TEXT NOT NULL,
  due_at TIMESTAMPTZ NOT NULL,
  source TEXT NOT NULL,
  confidence NUMERIC(4,3) NOT NULL DEFAULT 0.5,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE assignments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  deadline_id UUID REFERENCES deadlines(id) ON DELETE SET NULL,
  task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
  course_id UUID REFERENCES courses(id),
  title TEXT NOT NULL,
  instructions TEXT,
  submission_url TEXT,
  estimated_minutes INT NOT NULL DEFAULT 120,
  difficulty INT NOT NULL DEFAULT 3 CHECK(difficulty BETWEEN 1 AND 5),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE task_dependencies (
  task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  depends_on_task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  PRIMARY KEY(task_id, depends_on_task_id)
);

CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  starts_at TIMESTAMPTZ NOT NULL,
  ends_at TIMESTAMPTZ NOT NULL,
  location TEXT,
  networking_score INT DEFAULT 0,
  placement_score INT DEFAULT 0,
  skill_score INT DEFAULT 0,
  attendance_impact INT DEFAULT 0,
  recommendation TEXT,
  confidence NUMERIC(4,3) DEFAULT 0.5
);

CREATE TABLE emails (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider_message_id TEXT NOT NULL,
  subject TEXT NOT NULL,
  sender TEXT,
  received_at TIMESTAMPTZ NOT NULL,
  category TEXT,
  urgency INT CHECK(urgency BETWEEN 1 AND 100),
  confidence NUMERIC(4,3),
  raw_payload_encrypted BYTEA,
  UNIQUE(user_id, provider_message_id)
);

CREATE TABLE calendar_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  external_id TEXT,
  title TEXT NOT NULL,
  starts_at TIMESTAMPTZ NOT NULL,
  ends_at TIMESTAMPTZ NOT NULL,
  source TEXT NOT NULL,
  is_fixed BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  kind TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  scheduled_at TIMESTAMPTZ NOT NULL,
  sent_at TIMESTAMPTZ,
  status TEXT NOT NULL DEFAULT 'pending'
);

CREATE TABLE preferences (
  user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  focus_hours INT[] NOT NULL DEFAULT '{9,10,15,16}',
  sleep_start TIME NOT NULL DEFAULT '23:30',
  sleep_end TIME NOT NULL DEFAULT '07:00',
  notification_channels TEXT[] NOT NULL DEFAULT '{email,pwa}'
);

CREATE TABLE analytics_daily (
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  day DATE NOT NULL,
  productivity_score NUMERIC(5,2),
  attendance_score NUMERIC(5,2),
  consistency_score NUMERIC(5,2),
  burnout_score NUMERIC(5,2),
  focus_minutes INT NOT NULL DEFAULT 0,
  study_minutes INT NOT NULL DEFAULT 0,
  PRIMARY KEY(user_id, day)
);

CREATE TABLE ai_memory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  memory_type TEXT NOT NULL,
  content TEXT NOT NULL,
  embedding VECTOR(1536),
  confidence NUMERIC(4,3) NOT NULL DEFAULT 0.5,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  action TEXT NOT NULL,
  resource_type TEXT NOT NULL,
  resource_id TEXT,
  ip_hash TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE INDEX idx_oauth_accounts_user_provider ON oauth_accounts(user_id, provider);
CREATE INDEX idx_courses_user_code ON courses(user_id, code);
CREATE INDEX idx_attendance_records_course_recorded ON attendance_records(course_id, recorded_at DESC);
CREATE INDEX idx_tasks_user_deadline ON tasks(user_id, deadline) WHERE status <> 'done';
CREATE INDEX idx_tasks_user_status_priority ON tasks(user_id, status, priority DESC);
CREATE INDEX idx_deadlines_user_due_at ON deadlines(user_id, due_at);
CREATE INDEX idx_assignments_course_created ON assignments(course_id, created_at DESC);
CREATE INDEX idx_events_user_starts_at ON events(user_id, starts_at);
CREATE INDEX idx_emails_user_received_at ON emails(user_id, received_at DESC);
CREATE INDEX idx_calendar_items_user_starts_at ON calendar_items(user_id, starts_at);
CREATE INDEX idx_notifications_user_scheduled ON notifications(user_id, scheduled_at) WHERE status = 'pending';
CREATE INDEX idx_analytics_daily_user_day ON analytics_daily(user_id, day DESC);
CREATE INDEX idx_ai_memory_user_type ON ai_memory(user_id, memory_type);
CREATE INDEX idx_audit_logs_user_created ON audit_logs(user_id, created_at DESC);
