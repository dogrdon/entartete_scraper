##Sqlite db data descriptions

list of tables and their column headers and descriptions

###subject terms - data enriched from dbpedia
*id - artist id, primary key in `artworks`

*subject - individual subject term as used in dbpedia (to be used as `http://dbpedia.org/page/Category:$subject_term`) 

###artists - data scraped from the enartete datenbank and enriched form dbpedia
*id - artist id, primary key in `artworks`

*artist - string, artist name

*uri - resource location in dbpedia (not 100% accurate due to lazy NER)

*born - date of birth

*born_yr - year of birth only

*died - date of death

*died_yr - year of death only


###artworks - data scraped from the entartete datenbank

*catalog_id - 

*db_id - id as used by the creators of the database for this project

*loss_thru - how artwork obtained by Nazis originally (?) (e.g. Seizure, Exchange etc.)

*artwork_title - title of artwork or piece

*location - current location of artwork (if not lost or destroyed)

*date_lost - 

*material - material used in composing the artwork

*ek_inven_id - original id number given to the artwork by the Nazis

*uri - permamenent url for the record in the enatartete datenbank

*art_form - method of creating the artwork by the artist (e.g. watercolor, printmaking, sculpture, etc.)

*envelope - 

*work_status - current status of artwork (e.g. destroyed, lost, recovered)

*db_title - 

*work_date -

*artist_id - primary key for identifying artist

*copyright - copyright terms, if applicable

*inv_orig - 

*env_part - 

*museum_orig - original museum where artwork was housed before seizure (if applicable) (?)


###movements - data enriched from dbpedia
*id - artist id, primary key in `artworks`

*nation - nationality or country associated with artist

###nationalities - data enriched from dbpedia
*id - artist id, primary key in `artworks`

*mvmnt - name of artistic movement associated with artist