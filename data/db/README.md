## Sqlite db data descriptions

list of tables and their column headers and descriptions

### subject terms 
#### data enriched from dbpedia
* id - artist id, primary key in `artworks`

* subject - individual subject term as used in dbpedia (to be used as `http://dbpedia.org/page/Category:$subject_term`) 

### artists 
#### data scraped from the enartete datenbank and enriched form dbpedia
* id - artist id, primary key in `artworks`

* artist - string, artist name

* uri - resource location in dbpedia (not 100% accurate due to lazy NER)

* born - date of birth

* born_yr - year of birth only

* died - date of death

* died_yr - year of death only


### artworks
#### data scraped from the entartete datenbank

* catalog_id - not used

* db_id - id as used by the creators of the database for this project

* loss_thru - how artwork obtained by Nazis originally (?) (e.g. Seizure, Exchange etc.)

* artwork_title - title of artwork or piece

* location - current location of artwork (if not lost or destroyed)

* date_lost - not used

* material - material used in composing the artwork

* ek_inven_id - original id number given to the artwork by the Nazis

* uri - permamenent url for the record in the enatartete datenbank

* art_form - material and or technique in creating the artwork by the artist (e.g. watercolor, printmaking, sculpture, etc.)

* envelope - container location, if applicable 

* work_status - current status of artwork (e.g. destroyed, lost, recovered)

* db_title - title of artwork or piece as recorded in the Entartete Kunst records

* work_date - year work was created

* artist_id - primary key for identifying artist

* copyright - copyright terms, if applicable

* inv_orig - musuem of origin inventory number (?)

* env_part - container location, if applicable

* museum_orig - original museum where artwork was housed before seizure (if applicable) (?)


### movements  
#### data enriched from dbpedia
* id - artist id, primary key in `artworks`

* nation - nationality or country associated with artist

### nationalities - data enriched from dbpedia
* id - artist id, primary key in `artworks`

* mvmnt - name of artistic movement associated with artist
