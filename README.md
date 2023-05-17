# Read data from registry_stamp.csv and upload to a PostgreSQL database.

## .env

Make a copy of .env.sample and add the database credentials.


## The structure of the database should be:

```
-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS your_database.registry_stamp_id_seq;
CREATE SEQUENCE IF NOT EXISTS your_database.registry_stamp_passport_id_seq;

-- Table Definition
CREATE TABLE "your_database"."registry_stamp" (
    "id" int8 NOT NULL DEFAULT nextval('passport.registry_stamp_id_seq'::regclass),
    "hash" varchar(100),
    "provider" varchar(256),
    "credential" jsonb,
    "passport_id" int8 NOT NULL DEFAULT nextval('passport.registry_stamp_passport_id_seq'::regclass),
    PRIMARY KEY ("id")
);
```

## To spin up the docker instance:

```
make build
make run
```

## To execute inside of the container

```
make ssh
python check.py
```
