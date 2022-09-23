BEGIN TRANSACTION;
INSERT INTO "document" ("title", "content") VALUES('First example','# Example');
INSERT INTO "category" ("name") VALUES('Favorites');
INSERT INTO "category" ("name") VALUES('Python');
INSERT INTO "category" ("name") VALUES('Snippets');
COMMIT;