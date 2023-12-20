# ColouringPagesPrinter
An interface to enable rapid printing of kids colouring pages. 

## Setup
The setup requires a number of steps (typically) on a clean system. 

### Install SQLite3 database
```bash
sudo apt-get install sqlite3
```

### Create database tables
```bash
cd app
sqlite3 colouring_pages.db < database_setup.sql
cd ..
```


```bash
pip install -r requirements.txt
sqlite3 colouring_pages.db < database_setup.sql
python -m run
```

### CUPS library install issues
If you're installing the various packages on a Linux/Raspberry Pi system and you 
get some error relating to the ```pycups``` library, try installing the following dev 
package. 

```bash
sudo apt-get install libcups2-dev
```


## SQlite Database setup
There are two main tables created as part of this project, ```images``` which holds the file references to 
all the stored image files, and ```keywords``` which manages the relationship between various keywords and 
the images. 

The tables used in the SQLite database are below, and this can be re-created locally by running the script in the ```app``` 
folder as follows, 

```bash
sqlite3 colouring_pages.db < database_setup.sql
```

```sql 
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
```


```sql
SELECT thumbnail_path FROM images ORDER BY total_selections DESC LIMIT 12;
```
