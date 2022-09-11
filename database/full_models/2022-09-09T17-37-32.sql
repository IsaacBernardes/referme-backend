-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 0.9.4
-- PostgreSQL version: 13.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: new_database | type: DATABASE --
-- DROP DATABASE IF EXISTS new_database;
CREATE DATABASE new_database;
-- ddl-end --


-- object: public.movie | type: TABLE --
-- DROP TABLE IF EXISTS public.movie CASCADE;
CREATE TABLE public.movie (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	name text NOT NULL,
	synopsis text NOT NULL,
	rating numeric(3,1),
	image_url text,
	trailer_url text,
	CONSTRAINT movie_pk PRIMARY KEY (id)
);

-- object: public.genre | type: TABLE --
-- DROP TABLE IF EXISTS public.genre CASCADE;
CREATE TABLE public.genre (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	alias text NOT NULL,
	CONSTRAINT genre_pk PRIMARY KEY (id)
);

-- object: public.platform | type: TABLE --
-- DROP TABLE IF EXISTS public.platform CASCADE;
CREATE TABLE public.platform (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	name text NOT NULL,
	url text NOT NULL,
	CONSTRAINT platforms_pk PRIMARY KEY (id)
);

-- object: public.movie_genre | type: TABLE --
-- DROP TABLE IF EXISTS public.movie_genre CASCADE;
CREATE TABLE public.movie_genre (
	id_movie bigint NOT NULL,
	id_genre smallint NOT NULL,
	CONSTRAINT movie_genre_pk PRIMARY KEY (id_movie,id_genre)
);
-- ddl-end --

-- object: movie_fk | type: CONSTRAINT --
-- ALTER TABLE public.movie_genre DROP CONSTRAINT IF EXISTS movie_fk CASCADE;
ALTER TABLE public.movie_genre ADD CONSTRAINT movie_fk FOREIGN KEY (id_movie)
REFERENCES public.movie (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: genre_fk | type: CONSTRAINT --
-- ALTER TABLE public.movie_genre DROP CONSTRAINT IF EXISTS genre_fk CASCADE;
ALTER TABLE public.movie_genre ADD CONSTRAINT genre_fk FOREIGN KEY (id_genre)
REFERENCES public.genre (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: public.movie_platforms | type: TABLE --
-- DROP TABLE IF EXISTS public.movie_platforms CASCADE;
CREATE TABLE public.movie_platforms (
	id_movie bigint NOT NULL,
	id_platform smallint NOT NULL,
	CONSTRAINT movie_platforms_pk PRIMARY KEY (id_movie,id_platform)
);
-- ddl-end --

-- object: movie_fk | type: CONSTRAINT --
-- ALTER TABLE public.movie_platforms DROP CONSTRAINT IF EXISTS movie_fk CASCADE;
ALTER TABLE public.movie_platforms ADD CONSTRAINT movie_fk FOREIGN KEY (id_movie)
REFERENCES public.movie (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: platform_fk | type: CONSTRAINT --
-- ALTER TABLE public.movie_platforms DROP CONSTRAINT IF EXISTS platform_fk CASCADE;
ALTER TABLE public.movie_platforms ADD CONSTRAINT platform_fk FOREIGN KEY (id_platform)
REFERENCES public.platform (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --


