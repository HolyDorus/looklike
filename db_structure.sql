CREATE EXTENSION ltree;

CREATE TABLE all_clothes (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    image_path VARCHAR(250),
    parent_id BIGINT REFERENCES all_clothes ON DELETE CASCADE,
    parent_path LTREE,
    display_priority INTEGER
);

CREATE TABLE characters (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    author_id BIGINT,
    image_path VARCHAR(250),
    description TEXT,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clothes_on_characters (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    character_id BIGINT REFERENCES characters ON DELETE CASCADE NOT NULL,
    clothes_id BIGINT REFERENCES all_clothes ON DELETE CASCADE NOT NULL
);

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    username VARCHAR(40) UNIQUE NOT NULL,
    password_hash VARCHAR(70) NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE favorite_characters_of_users (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    user_id BIGINT REFERENCES users ON DELETE CASCADE NOT NULL,
    character_id BIGINT REFERENCES characters ON DELETE CASCADE NOT NULL
);

CREATE INDEX all_clothes_parent_path_idx ON all_clothes USING GIST (parent_path);
CREATE INDEX all_clothes_parent_id_idx ON all_clothes (parent_id);

CREATE OR REPLACE FUNCTION update_all_clothes_parent_path() RETURNS TRIGGER AS $$
    DECLARE
        path ltree;
    BEGIN
        IF NEW.parent_id IS NULL THEN
            NEW.parent_path = NEW.id::text::ltree;
        ELSE
            SELECT parent_path FROM all_clothes WHERE id = NEW.parent_id INTO path;
            IF path IS NULL THEN
                RAISE EXCEPTION 'Invalid parent_id %', NEW.parent_id;
            END IF;
            NEW.parent_path = (path::text || '.' || NEW.id)::ltree;
        END IF;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER all_clothes_parent_path_tgr BEFORE INSERT OR UPDATE ON all_clothes
    FOR EACH ROW EXECUTE PROCEDURE update_all_clothes_parent_path();
