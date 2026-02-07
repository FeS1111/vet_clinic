-- Пациенты
CREATE TABLE IF NOT EXISTS patients (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name      TEXT NOT NULL,
  last_name       TEXT NOT NULL,
  phone           TEXT UNIQUE,
  email           TEXT,
  birth_date      DATE,
  species         TEXT,
  breed           TEXT,
  owner_name      TEXT NOT NULL,
  created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Врачи
CREATE TABLE IF NOT EXISTS doctors (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  full_name   TEXT NOT NULL,
  specialty   TEXT NOT NULL,
  phone       TEXT,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Записи к врачу
CREATE TABLE IF NOT EXISTS appointments (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  patient_id    INTEGER NOT NULL,
  doctor_id     INTEGER NOT NULL,
  starts_at     DATETIME NOT NULL,
  ends_at       DATETIME,
  status        TEXT NOT NULL DEFAULT 'scheduled',
  reason        TEXT,
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE,
  FOREIGN KEY(doctor_id)  REFERENCES doctors(id)  ON DELETE RESTRICT
);

-- Медкарта (записи)
CREATE TABLE IF NOT EXISTS medical_records (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  patient_id      INTEGER NOT NULL,
  appointment_id  INTEGER,
  diagnosis       TEXT,
  treatment       TEXT,
  notes           TEXT,
  created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE,
  FOREIGN KEY(appointment_id) REFERENCES appointments(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_appt_doctor_starts_at ON appointments(doctor_id, starts_at);
CREATE INDEX IF NOT EXISTS idx_records_patient ON medical_records(patient_id);