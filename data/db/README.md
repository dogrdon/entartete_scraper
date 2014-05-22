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



###movements - data enriched from dbpedia
*id - artist id, primary key in `artworks`
*nation - nationality or country associated with artist

###nationalities - data enriched from dbpedia
*id - artist id, primary key in `artworks`
*mvmnt - name of artistic movement associated with artist