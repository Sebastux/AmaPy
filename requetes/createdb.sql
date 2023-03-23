CREATE TABLE IF NOT EXISTS "amatable" (
	"keyzon"	INTEGER NOT NULL UNIQUE,
	"nom_produit"	TEXT,
	"note"	INTEGER,
	"description"	BLOB,
	"evaluation"	INTEGER,
	"status_produit"	TEXT,
	"date_creation"	TEXT,
	"url"	TEXT,
	PRIMARY KEY("keyzon" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "tblprix" (
	"prixzon"	INTEGER NOT NULL UNIQUE,
	"keyzon"	INTEGER,
	"prix"	REAL,
	"monnaie"	TEXT,
	"date_maj"	TEXT,
	PRIMARY KEY("prixzon" AUTOINCREMENT),
	FOREIGN KEY("keyzon") REFERENCES "amatable"("keyzon")
);