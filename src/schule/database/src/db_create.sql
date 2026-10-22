-- Create table and index for guardians

CREATE TABLE IF NOT EXISTS guardians (
    id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    ward_ids TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS guardians_index ON guardians(id);

-- Create table and index for primary students
CREATE TABLE IF NOT EXISTS primary_students (
    id TEXT PRIMARY KEY,
    guardian_id TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    grade INTEGER NOT NULL,
    FOREIGN KEY(id) REFERENCES `guardians.id` ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK(grade > 0 AND grade < 6)
);

CREATE INDEX IF NOT EXISTS primary_students_index ON primary_students(id);

-- Create table and index for secondary students

CREATE TABLE IF NOT EXISTS secondary_students (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    guardian_id TEXT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    grade INTEGER NOT NULL,
    FOREIGN KEY(id) REFERENCES `guardians.id` ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK(grade > 0 AND grade < 7)
);

CREATE INDEX IF NOT EXISTS secondary_students_index ON secondary_students(id);

-- Create table for primary subjects

CREATE TABLE IF NOT EXISTS primary_subjects (
    id INT AUTO INCREMENT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    description TEXT
);

-- Create table for secondary subjects

CREATE TABLE IF NOT EXISTS secondary_subjects (
    id INT AUTO INCREMENT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    min_class_grade INT NOT NULL,
    max_class_grade INT NOT NULL
);

-- Create table for primary teachers

CREATE TABLE IF NOT EXISTS primary_teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    grade INT NOT NULL,
    CHECK(grade > 0 AND grade < 7)
);

-- Create table for secondary teachers

CREATE TABLE IF NOT EXISTS secondary_teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    subject_id INT NOT NULL,
    FOREIGN KEY(subject_id) REFERENCES `secondary_subjects.id`
);
