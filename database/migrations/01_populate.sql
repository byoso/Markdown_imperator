BEGIN TRANSACTION;
INSERT INTO "document" ("title", "content") VALUES('First example','# Big title\nSome text here\n##Smaller title');
INSERT INTO "category" ("name") VALUES('Favorites');
INSERT INTO "category" ("name") VALUES('python');
COMMIT;