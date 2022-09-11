-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 0.9.4
-- PostgreSQL version: 13.0
-- Project Site: pgmodeler.io
-- Model Author: ---
-- object: isaac | type: ROLE --
-- DROP ROLE IF EXISTS isaac;
CREATE ROLE isaac WITH 
	SUPERUSER
	INHERIT
	LOGIN
	ENCRYPTED PASSWORD '********';
-- ddl-end --


-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: new_database | type: DATABASE --
-- DROP DATABASE IF EXISTS new_database;
CREATE DATABASE new_database
	ENCODING = 'UTF8'
	LC_COLLATE = 'Portuguese_Brazil.1252'
	LC_CTYPE = 'Portuguese_Brazil.1252'
	TABLESPACE = pg_default
	OWNER = postgres;
-- ddl-end --


-- object: public.movie | type: TABLE --
-- DROP TABLE IF EXISTS public.movie CASCADE;
CREATE TABLE public.movie (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START WITH 1 CACHE 1 ),
	name text NOT NULL,
	synopsis text NOT NULL,
	rating numeric(3,1),
	image_url text,
	trailer_url text,
	CONSTRAINT movie_pk PRIMARY KEY (id)
);
-- ddl-end --

-- -- object: public.movie_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS public.movie_id_seq CASCADE;
-- CREATE SEQUENCE public.movie_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 9223372036854775807
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE public.movie_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
-- object: public.genre | type: TABLE --
-- DROP TABLE IF EXISTS public.genre CASCADE;
CREATE TABLE public.genre (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START WITH 1 CACHE 1 ),
	alias text NOT NULL,
	reference_image text,
	CONSTRAINT genre_pk PRIMARY KEY (id)
);
-- ddl-end --

INSERT INTO public.genre (id, alias, reference_image) VALUES (E'1', E'Ação', E'https://m.media-amazon.com/images/M/MV5BMTg4NDI4MTA2Ml5BMl5BanBnXkFtZTgwMjUyOTYzMjI@._V1_FMjpg_UX1280_.jpg');
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'2', E'Aventura', E'https://m.media-amazon.com/images/M/MV5BMDBiMjliZWYtNThiMi00NWZjLWI1MDYtMmMxMmY0MDJmNGU4XkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_.jpg');
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'3', E'Animação', E'https://m.media-amazon.com/images/M/MV5BZWY3NGMzMjgtNTJjNy00NzY0LWI5NTUtYmJlNmQ2NmJiYjRmXkEyXkFqcGdeQXVyMTQ0OTA3OTY4._V1_FMjpg_UX1280_.jpg');
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'4', E'Biografia', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'5', E'Comédia', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'6', E'Crime', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'7', E'Documentário', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'8', E'Drama', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'9', E'Família', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'10', E'Fantasia', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'11', E'Game-Show', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'12', E'História', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'13', E'Terror', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'14', E'Musical', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'15', E'Mistério', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'16', E'Jornal', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'17', E'Reality-Show', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'18', E'Romance', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'19', E'Sci-Fi', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'20', E'Curta-Metragem', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'21', E'Esporte', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'22', E'Talk-Show', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'23', E'Thriller', DEFAULT);
-- ddl-end --
INSERT INTO public.genre (id, alias, reference_image) VALUES (E'24', E'Guerra', DEFAULT);
-- ddl-end --

-- -- object: public.genre_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS public.genre_id_seq CASCADE;
-- CREATE SEQUENCE public.genre_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 32767
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE public.genre_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
-- object: public.platform | type: TABLE --
-- DROP TABLE IF EXISTS public.platform CASCADE;
CREATE TABLE public.platform (
	id smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 1 MAXVALUE 32767 START WITH 1 CACHE 1 ),
	name text NOT NULL,
	url text NOT NULL,
	CONSTRAINT platforms_pk PRIMARY KEY (id)
);
-- ddl-end --

INSERT INTO public.platform (id, name, url) VALUES (E'1', E'Netflix', E'https://www.netflix.com');
-- ddl-end --
INSERT INTO public.platform (id, name, url) VALUES (E'2', E'Disney Plus', E'https://www.disneyplus.com');
-- ddl-end --
INSERT INTO public.platform (id, name, url) VALUES (E'3', E'Star Plus', E'https://www.starplus.com');
-- ddl-end --
INSERT INTO public.platform (id, name, url) VALUES (E'4', E'Amazon Prime Vídeo', E'https://www.primevideo.com');
-- ddl-end --
INSERT INTO public.platform (id, name, url) VALUES (E'5', E'Paramount Plus', E'https://www.paramountplus.com');
-- ddl-end --
INSERT INTO public.platform (id, name, url) VALUES (E'6', E'Apple TV+', E'https://www.apple.com/apple-tv-plus');
-- ddl-end --
INSERT INTO public.platform (id, name, url) VALUES (E'7', E'Globoplay', E'https://globoplay.globo.com');
-- ddl-end --

-- -- object: public.platform_id_seq | type: SEQUENCE --
-- -- DROP SEQUENCE IF EXISTS public.platform_id_seq CASCADE;
-- CREATE SEQUENCE public.platform_id_seq
-- 	INCREMENT BY 1
-- 	MINVALUE 1
-- 	MAXVALUE 32767
-- 	START WITH 1
-- 	CACHE 1
-- 	NO CYCLE
-- 	OWNED BY NONE;
-- 
-- -- ddl-end --
-- ALTER SEQUENCE public.platform_id_seq OWNER TO postgres;
-- -- ddl-end --
-- 
-- object: public.movie_genres | type: TABLE --
-- DROP TABLE IF EXISTS public.movie_genres CASCADE;
CREATE TABLE public.movie_genres (
	id_movie bigint NOT NULL,
	id_genre smallint NOT NULL,
	CONSTRAINT movie_genre_pk PRIMARY KEY (id_movie,id_genre)
);
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
-- ALTER TABLE public.movie_genres DROP CONSTRAINT IF EXISTS movie_fk CASCADE;
ALTER TABLE public.movie_genres ADD CONSTRAINT movie_fk FOREIGN KEY (id_movie)
REFERENCES public.movie (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
-- ddl-end --

-- object: genre_fk | type: CONSTRAINT --
-- ALTER TABLE public.movie_genres DROP CONSTRAINT IF EXISTS genre_fk CASCADE;
ALTER TABLE public.movie_genres ADD CONSTRAINT genre_fk FOREIGN KEY (id_genre)
REFERENCES public.genre (id) MATCH FULL
ON DELETE RESTRICT ON UPDATE CASCADE;
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

-- object: "grant_CU_eb94f049ac" | type: PERMISSION --
GRANT CREATE,USAGE
   ON SCHEMA public
   TO postgres;
-- ddl-end --

-- object: "grant_CU_cd8e46e7b6" | type: PERMISSION --
GRANT CREATE,USAGE
   ON SCHEMA public
   TO PUBLIC;
-- ddl-end --


