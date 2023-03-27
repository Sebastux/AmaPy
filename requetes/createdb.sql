CREATE TABLE "amatable" (
	"keyzon"	INTEGER NOT NULL UNIQUE,
	"nom_produit"	TEXT,
	"note"	INTEGER,
	"description"	BLOB,
	"evaluation"	INTEGER,
	"status_produit"	TEXT,
	"date_creation"	TEXT,
	PRIMARY KEY("keyzon" AUTOINCREMENT)
);

CREATE TABLE "tblprix" (
	"keyzon"	INTEGER NOT NULL,
	"prix"	REAL,
	"monnaie"	TEXT,
	"date_maj"	TEXT,
	FOREIGN KEY("keyzon") REFERENCES "amatable"("keyzon")
);

CREATE TABLE "tbllink" (
	"keyzon"	INTEGER NOT NULL,
	"url"	TEXT,
	"chemin_image1"	TEXT,
	FOREIGN KEY("keyzon") REFERENCES "amatable"("keyzon")
);

PRAGMA foreign_keys = ON;