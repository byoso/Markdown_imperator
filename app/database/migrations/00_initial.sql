BEGIN TRANSACTION;
CREATE TABLE "category" (
	"id"	INTEGER NOT NULL,
	"name"	NVARCHAR(80) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "document" (
    "id" INTEGER NOT NULL,
    "title" NVARCHAR(80) NOT NULL,
    "content" VARCHAR NULL,
    "filename" VARCHAR NOT NULL DEFAULT "",
    "directory" VARCHAR NOT NULL DEFAULT "",
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "cat_doc" (
    "id" INTEGER NOT NULL,
    "cat_id" INTEGER,
    "doc_id" INTEGER,
    PRIMARY KEY ("id" AUTOINCREMENT),
    FOREIGN KEY("cat_id") REFERENCES "category"("id") ON DELETE CASCADE,
    FOREIGN KEY("doc_id") REFERENCES "document"("id") ON DELETE CASCADE
);
CREATE INDEX index_category
ON category ( id COLLATE NOCASE );
CREATE INDEX index_document
ON document ( id COLLATE NOCASE );
COMMIT;
