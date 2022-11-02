BEGIN TRANSACTION;
INSERT INTO "document" ("title", "content") VALUES('Welcome !','# ![logo](https://i.goopics.net/lhw9s2.png)
# Welcome to Markdown Imperator !
_The best Markdown editor of the empire_
');
INSERT INTO "category" ("name") VALUES('Favorites');
COMMIT;