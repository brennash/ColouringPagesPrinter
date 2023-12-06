DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS keywords;
DROP TABLE IF EXISTS searches;

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    md5_hash TEXT NOT NULL,
    file_path TEXT NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    thumbnail_path TEXT NOT NULL,
    thumbnail_width INTEGER NOT NULL,
    thumbnail_height INTEGER NOT NULL,
    last_selected_yyyymmdd INTEGER,
    total_selections INTEGER
);

CREATE TABLE keywords (
    id INTEGER PRIMARY KEY,
    keyword TEXT NOT NULL,
    image_id INTEGER,
    FOREIGN KEY (image_id) REFERENCES images(id)
);

CREATE TABLE searches (
  id INTEGER PRIMARY KEY,
  created_at TIMESTAMP NOT NULL,
  search_terms TEXT NOT NULL
);
