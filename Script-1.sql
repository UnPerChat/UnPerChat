-- public.clients_info definition

-- Drop table

-- DROP TABLE public.clients_info;

CREATE TABLE public.clients_info (
	client_id serial4 NOT NULL,
	username varchar(50) NULL,
	email varchar(50) NULL,
	"password" varchar(100) NULL,
	CONSTRAINT clients_info_pkey PRIMARY KEY (client_id)
);