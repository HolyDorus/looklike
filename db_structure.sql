CREATE EXTENSION ltree;

CREATE TABLE all_clothes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    image_path VARCHAR(250),
    parent_id INTEGER REFERENCES all_clothes ON DELETE CASCADE,
    parent_path LTREE
);

CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    author_id INTEGER,
    image_path VARCHAR(250),
    description TEXT,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clothes_on_characters (
    id SERIAL PRIMARY KEY,
    character_id INTEGER REFERENCES characters ON DELETE CASCADE,
    clothes_id INTEGER REFERENCES all_clothes ON DELETE CASCADE
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
