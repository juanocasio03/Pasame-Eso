-- PasameEso database schema (System Design, Section 5).
-- Running `flask --app app init-db` DROPS every table and recreates it.
-- Change the database ONLY by editing this file, so the whole team stays in sync.

DROP TABLE IF EXISTS moderation_actions;
DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

-- Registered accounts (REQ.1.x, REQ.2.x, FEAT-03).
CREATE TABLE users (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    name                  TEXT    NOT NULL,
    email                 TEXT    NOT NULL UNIQUE CHECK (length(email) <= 64),
    username              TEXT    NOT NULL UNIQUE CHECK (length(username) <= 20),
    password_hash         TEXT    NOT NULL,                -- bcrypt, never plain text (NFR-SEC-02)
    role                  TEXT    NOT NULL DEFAULT 'contributor'
                                  CHECK (role IN ('contributor', 'moderator')),
    is_active             INTEGER NOT NULL DEFAULT 1,      -- moderators can deactivate (FEAT-03)
    failed_login_attempts INTEGER NOT NULL DEFAULT 0,      -- lockout after 5 (NFR-SEC-03)
    locked_until          TIMESTAMP,
    created_at            TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Published resources (REQ.4.x). "Post" and "Resource" mean the same thing.
CREATE TABLE posts (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    title         TEXT    NOT NULL CHECK (length(title) <= 100),
    resource_type TEXT    NOT NULL
                          CHECK (resource_type IN ('class_notes', 'practice_exam', 'study_guide')),
    course_code   TEXT    NOT NULL                         -- e.g. CCOM4030: 4 letters + 4 digits
                          CHECK (course_code GLOB '[A-Z][A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9]'),
    course_name   TEXT    CHECK (length(course_name) <= 64),
    professor     TEXT    NOT NULL CHECK (length(professor) <= 25),
    description   TEXT,
    file_path     TEXT    NOT NULL,                        -- relative to UPLOAD_FOLDER
    file_hash     TEXT    NOT NULL,                        -- SHA-256 of the file contents
    file_mime     TEXT    NOT NULL,
    file_size     INTEGER NOT NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Duplicate detection: the same file can't be uploaded twice for one course (REQ.4.2).
    UNIQUE (course_code, file_hash)
);

CREATE INDEX idx_posts_course    ON posts (course_code);
CREATE INDEX idx_posts_professor ON posts (professor);
CREATE INDEX idx_posts_created   ON posts (created_at);

-- 1-5 star ratings, one per user per post (FEAT-06).
CREATE TABLE ratings (
    user_id    INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    post_id    INTEGER NOT NULL REFERENCES posts (id) ON DELETE CASCADE,
    stars      INTEGER NOT NULL CHECK (stars BETWEEN 1 AND 5),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, post_id)
);

-- Plain-text comments (FEAT-07).
CREATE TABLE comments (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id    INTEGER NOT NULL REFERENCES posts (id) ON DELETE CASCADE,
    user_id    INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    body       TEXT    NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Reports against a post (REQ.5.1). One report per user per post.
CREATE TABLE reports (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id     INTEGER NOT NULL REFERENCES posts (id) ON DELETE CASCADE,
    reporter_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    reason      TEXT    NOT NULL
                        CHECK (reason IN ('inappropriate', 'incorrect', 'plagiarism', 'duplicate', 'other')),
    description TEXT    CHECK (length(description) <= 300),
    status      TEXT    NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending', 'viewed', 'resolved')),
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (post_id, reporter_id)
);

CREATE INDEX idx_reports_status ON reports (status);

-- Log of moderator decisions (REQ.5.3 "Log action"). Keeps a title snapshot
-- because the post itself may have been deleted.
CREATE TABLE moderation_actions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id      INTEGER REFERENCES posts (id) ON DELETE SET NULL,
    post_title   TEXT    NOT NULL,
    moderator_id INTEGER NOT NULL REFERENCES users (id),
    action       TEXT    NOT NULL CHECK (action IN ('keep', 'edit', 'delete')),
    note         TEXT    CHECK (length(note) <= 300),
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
