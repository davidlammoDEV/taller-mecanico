--
-- PostgreSQL database dump
--

\restrict Ko4n81VgQdkpwV6NNPLApIZGZak0EGGtxVSFj5sp3gJ0a2UbOo4aDUF8NjvZaLg

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auditoria; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auditoria (
    id bigint NOT NULL,
    tabla character varying(50) NOT NULL,
    operacion character varying(20) NOT NULL,
    registro_id text NOT NULL,
    datos_antes jsonb,
    datos_despues jsonb,
    usuario_db text,
    fecha_evento timestamp without time zone,
    revisado boolean,
    nota_supervisor text,
    revisado_por integer,
    fecha_revision timestamp without time zone
);


ALTER TABLE public.auditoria OWNER TO postgres;

--
-- Name: auditoria_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auditoria_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.auditoria_id_seq OWNER TO postgres;

--
-- Name: auditoria_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auditoria_id_seq OWNED BY public.auditoria.id;


--
-- Name: cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cliente (
    id integer NOT NULL,
    documento character varying(20) NOT NULL,
    nombre character varying(100) NOT NULL,
    telefono character varying(20),
    correo character varying(100),
    direccion character varying(200) NOT NULL,
    activo boolean NOT NULL
);


ALTER TABLE public.cliente OWNER TO postgres;

--
-- Name: cliente_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cliente_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cliente_id_seq OWNER TO postgres;

--
-- Name: cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cliente_id_seq OWNED BY public.cliente.id;


--
-- Name: factura; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.factura (
    id integer NOT NULL,
    orden_id integer NOT NULL,
    fecha timestamp without time zone DEFAULT now() NOT NULL,
    subtotal numeric(12,2) NOT NULL,
    impuestos numeric(12,2) NOT NULL,
    total numeric(12,2) NOT NULL,
    cobro_final numeric(12,2) NOT NULL,
    metodo character varying(50) NOT NULL,
    activo boolean NOT NULL,
    CONSTRAINT ck_factura_metodo CHECK (((metodo)::text = ANY (ARRAY[('Efectivo'::character varying)::text, ('Tarjeta de Crédito'::character varying)::text, ('Tarjeta de Débito'::character varying)::text, ('Transferencia'::character varying)::text])))
);


ALTER TABLE public.factura OWNER TO postgres;

--
-- Name: factura_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.factura_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.factura_id_seq OWNER TO postgres;

--
-- Name: factura_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.factura_id_seq OWNED BY public.factura.id;


--
-- Name: mecanico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mecanico (
    id integer NOT NULL,
    documento character varying(20) NOT NULL,
    nombre character varying(100) NOT NULL,
    especialidad character varying(100),
    telefono character varying(20),
    fecha_ingreso date DEFAULT CURRENT_DATE NOT NULL,
    activo boolean NOT NULL
);


ALTER TABLE public.mecanico OWNER TO postgres;

--
-- Name: mecanico_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mecanico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.mecanico_id_seq OWNER TO postgres;

--
-- Name: mecanico_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mecanico_id_seq OWNED BY public.mecanico.id;


--
-- Name: orden_detalle_repuesto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orden_detalle_repuesto (
    id integer NOT NULL,
    orden_id integer NOT NULL,
    repuesto_codigo character varying(20) NOT NULL,
    cantidad integer NOT NULL,
    precio_aplicado numeric(12,2) NOT NULL
);


ALTER TABLE public.orden_detalle_repuesto OWNER TO postgres;

--
-- Name: orden_detalle_repuesto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orden_detalle_repuesto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orden_detalle_repuesto_id_seq OWNER TO postgres;

--
-- Name: orden_detalle_repuesto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orden_detalle_repuesto_id_seq OWNED BY public.orden_detalle_repuesto.id;


--
-- Name: orden_detalle_servicio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orden_detalle_servicio (
    id integer NOT NULL,
    orden_id integer NOT NULL,
    servicio_id integer NOT NULL,
    cantidad integer NOT NULL,
    precio_aplicado numeric(12,2) NOT NULL
);


ALTER TABLE public.orden_detalle_servicio OWNER TO postgres;

--
-- Name: orden_detalle_servicio_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orden_detalle_servicio_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orden_detalle_servicio_id_seq OWNER TO postgres;

--
-- Name: orden_detalle_servicio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orden_detalle_servicio_id_seq OWNED BY public.orden_detalle_servicio.id;


--
-- Name: orden_servicio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orden_servicio (
    id integer NOT NULL,
    fecha timestamp without time zone DEFAULT now() NOT NULL,
    diagnostico text,
    estado character varying(30) NOT NULL,
    observaciones text,
    costo_estimado numeric(12,2),
    cliente_id integer NOT NULL,
    placa character varying(10) NOT NULL,
    mecanico_id integer NOT NULL,
    activo boolean NOT NULL,
    CONSTRAINT ck_orden_estado CHECK (((estado)::text = ANY (ARRAY[('Pendiente'::character varying)::text, ('En Proceso'::character varying)::text, ('Completado'::character varying)::text, ('Cancelado'::character varying)::text])))
);


ALTER TABLE public.orden_servicio OWNER TO postgres;

--
-- Name: orden_servicio_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orden_servicio_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orden_servicio_id_seq OWNER TO postgres;

--
-- Name: orden_servicio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orden_servicio_id_seq OWNED BY public.orden_servicio.id;


--
-- Name: proveedor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.proveedor (
    id integer NOT NULL,
    documento character varying(20) NOT NULL,
    nombre character varying(100) NOT NULL,
    nom_empresa character varying(100),
    telefono character varying(20),
    correo character varying(100),
    activo boolean NOT NULL
);


ALTER TABLE public.proveedor OWNER TO postgres;

--
-- Name: proveedor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.proveedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.proveedor_id_seq OWNER TO postgres;

--
-- Name: proveedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.proveedor_id_seq OWNED BY public.proveedor.id;


--
-- Name: refresh_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.refresh_token (
    id bigint NOT NULL,
    token character varying(500),
    user_log bigint,
    expira date,
    activo boolean
);


ALTER TABLE public.refresh_token OWNER TO postgres;

--
-- Name: refresh_token_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.refresh_token ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.refresh_token_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: repuesto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.repuesto (
    codigo character varying(20) NOT NULL,
    nombre character varying(100) NOT NULL,
    marca character varying(50),
    stock integer NOT NULL,
    costo numeric(12,2) NOT NULL,
    precio numeric(12,2) NOT NULL,
    descripcion text,
    activo boolean NOT NULL,
    proveedor_id integer
);


ALTER TABLE public.repuesto OWNER TO postgres;

--
-- Name: rol; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rol (
    idrol bigint NOT NULL,
    nombre character varying(30),
    descripcion text,
    activo boolean
);


ALTER TABLE public.rol OWNER TO postgres;

--
-- Name: rol_idrol_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.rol ALTER COLUMN idrol ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.rol_idrol_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: servicio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.servicio (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    costo_base numeric(12,2) NOT NULL,
    descripcion text,
    activo boolean NOT NULL
);


ALTER TABLE public.servicio OWNER TO postgres;

--
-- Name: servicio_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.servicio_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.servicio_id_seq OWNER TO postgres;

--
-- Name: servicio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.servicio_id_seq OWNED BY public.servicio.id;


--
-- Name: supervisor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.supervisor (
    id integer NOT NULL,
    documento character varying(20) NOT NULL,
    nombre character varying(100) NOT NULL,
    telefono character varying(20),
    fecha_ingreso date DEFAULT CURRENT_DATE NOT NULL,
    activo boolean NOT NULL
);


ALTER TABLE public.supervisor OWNER TO postgres;

--
-- Name: supervisor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.supervisor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.supervisor_id_seq OWNER TO postgres;

--
-- Name: supervisor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.supervisor_id_seq OWNED BY public.supervisor.id;


--
-- Name: user_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_log (
    idsuer_log bigint NOT NULL,
    idrol bigint,
    iduser character varying(20),
    activo boolean
);


ALTER TABLE public.user_log OWNER TO postgres;

--
-- Name: user_log_idsuer_log_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.user_log ALTER COLUMN idsuer_log ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.user_log_idsuer_log_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    nombre character varying(30),
    apellido character varying(30),
    correo character varying(30),
    activo boolean,
    iduser character varying(20) NOT NULL,
    contrase character varying(100)
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: vehiculo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vehiculo (
    placa character varying(10) NOT NULL,
    marca character varying(50) NOT NULL,
    modelo character varying(50) NOT NULL,
    ano integer NOT NULL,
    color character varying(30),
    kilometraje integer NOT NULL,
    observaciones text,
    activo boolean NOT NULL,
    cliente_id integer NOT NULL
);


ALTER TABLE public.vehiculo OWNER TO postgres;

--
-- Name: auditoria id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria ALTER COLUMN id SET DEFAULT nextval('public.auditoria_id_seq'::regclass);


--
-- Name: cliente id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente ALTER COLUMN id SET DEFAULT nextval('public.cliente_id_seq'::regclass);


--
-- Name: factura id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.factura ALTER COLUMN id SET DEFAULT nextval('public.factura_id_seq'::regclass);


--
-- Name: mecanico id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mecanico ALTER COLUMN id SET DEFAULT nextval('public.mecanico_id_seq'::regclass);


--
-- Name: orden_detalle_repuesto id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_repuesto ALTER COLUMN id SET DEFAULT nextval('public.orden_detalle_repuesto_id_seq'::regclass);


--
-- Name: orden_detalle_servicio id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_servicio ALTER COLUMN id SET DEFAULT nextval('public.orden_detalle_servicio_id_seq'::regclass);


--
-- Name: orden_servicio id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_servicio ALTER COLUMN id SET DEFAULT nextval('public.orden_servicio_id_seq'::regclass);


--
-- Name: proveedor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedor ALTER COLUMN id SET DEFAULT nextval('public.proveedor_id_seq'::regclass);


--
-- Name: servicio id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicio ALTER COLUMN id SET DEFAULT nextval('public.servicio_id_seq'::regclass);


--
-- Name: supervisor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supervisor ALTER COLUMN id SET DEFAULT nextval('public.supervisor_id_seq'::regclass);


--
-- Data for Name: auditoria; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auditoria (id, tabla, operacion, registro_id, datos_antes, datos_despues, usuario_db, fecha_evento, revisado, nota_supervisor, revisado_por, fecha_revision) FROM stdin;
\.


--
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cliente (id, documento, nombre, telefono, correo, direccion, activo) FROM stdin;
1	V-12322134	Mike	Morales	brawlcito12@gmail.com	Av. Rotaria	t
2	V-12345677	Melvin	0422-4567122	melvinhomelander@gmail.com	Las Acasias, calle 3	t
3	cp3322	CpAndrea	0244-5654312	AndreaPernia@gmail.com	Baario Enchufao	f
\.


--
-- Data for Name: factura; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.factura (id, orden_id, fecha, subtotal, impuestos, total, cobro_final, metodo, activo) FROM stdin;
\.


--
-- Data for Name: mecanico; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mecanico (id, documento, nombre, especialidad, telefono, fecha_ingreso, activo) FROM stdin;
1	V-9234511	CpAndres	carros	0412-43212265	2025-08-19	t
\.


--
-- Data for Name: orden_detalle_repuesto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orden_detalle_repuesto (id, orden_id, repuesto_codigo, cantidad, precio_aplicado) FROM stdin;
\.


--
-- Data for Name: orden_detalle_servicio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orden_detalle_servicio (id, orden_id, servicio_id, cantidad, precio_aplicado) FROM stdin;
\.


--
-- Data for Name: orden_servicio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orden_servicio (id, fecha, diagnostico, estado, observaciones, costo_estimado, cliente_id, placa, mecanico_id, activo) FROM stdin;
1	2026-08-19 12:38:11.418555	Tiene toyobobo	Pendiente	tiene toyobobo	25000.00	2	MK8DX	1	t
\.


--
-- Data for Name: proveedor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.proveedor (id, documento, nombre, nom_empresa, telefono, correo, activo) FROM stdin;
1	V-1345632	Kingpin	KingpinOS	2077-345324	kingpinosCEO@yahoo.com	t
\.


--
-- Data for Name: refresh_token; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.refresh_token (id, token, user_log, expira, activo) FROM stdin;
1	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZXNzaXhjcjdAZ21haWwuY29tIiwiZXhwIjoxNzg3NDA2NjQ2LCJ0eXBlIjoicmVmcmVzaCJ9.OYLt663aXYAEyZgP7k1LnieaNezNYXAtpegxM6JjRlE	1	2026-08-22	t
2	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZXNzaXhjcjdAZ21haWwuY29tIiwiZXhwIjoxNzg3NzU3MDUwLCJ0eXBlIjoicmVmcmVzaCJ9.BDaLZMS53UFxkYLNDKhraF_t_3RORDQvpCbV1qaWlS0	1	2026-08-26	t
3	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZXNzaXhjcjdAZ21haWwuY29tIiwiZXhwIjoxNzg3NzU3OTUxLCJ0eXBlIjoicmVmcmVzaCJ9.4VGf0g5toPrBCcQI8knBiEn83we0Rs8k_f2Oovi4_HM	1	2026-08-26	t
4	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZXNzaXhjcjdAZ21haWwuY29tIiwiZXhwIjoxNzg3NzYyMjgzLCJ0eXBlIjoicmVmcmVzaCJ9.jLnMVy2Cw_gfUwX-mHi89dcTEKot2KevNYWzRdsJuVk	1	2026-08-26	t
5	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZXNzaXhjcjdAZ21haWwuY29tIiwiZXhwIjoxNzg3NzgyMDgyLCJ0eXBlIjoicmVmcmVzaCJ9.3O8vi_9CBEFM78zylVc07qUns8gSOrSAzFUZQDCJLuc	1	2026-08-26	t
6	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZXNzaXhjcjdAZ21haWwuY29tIiwiZXhwIjoxNzg3NzgyMjU3LCJ0eXBlIjoicmVmcmVzaCJ9.tt4AOhAYIjM8Qg9ojt8zowQy1JPnkmGPJJXqHPc-fyU	1	2026-08-26	t
\.


--
-- Data for Name: repuesto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.repuesto (codigo, nombre, marca, stock, costo, precio, descripcion, activo, proveedor_id) FROM stdin;
CP05	Rines de carro	Cpsin	30	20000.00	35000.00	Rines para carro para que nuestro carro carree	t	1
CP04	Rines de moto	Cpsin	20	10000.00	20000.00	Rines para carro para que nuestra moto motee	t	1
\.


--
-- Data for Name: rol; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rol (idrol, nombre, descripcion, activo) FROM stdin;
1	Mecanico	El mecanico se encarga de reparar motores, cambio de aceite, cambio de cauchos, etc.	t
2	Jefe de Taller	El jefe de taller es el encargado de tener seguimiento sobre los mecanicos, sobre las piezas que se encuentran dentro del taller, contratar o despedir empleados.	t
3	Supervisor	Aquel que supervisa al supervisando	t
\.


--
-- Data for Name: servicio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.servicio (id, nombre, costo_base, descripcion, activo) FROM stdin;
\.


--
-- Data for Name: supervisor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.supervisor (id, documento, nombre, telefono, fecha_ingreso, activo) FROM stdin;
\.


--
-- Data for Name: user_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_log (idsuer_log, idrol, iduser, activo) FROM stdin;
1	2	V-012345	t
3	3	V-1234567	t
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (nombre, apellido, correo, activo, iduser, contrase) FROM stdin;
Erick	Moncada	lordriczer1105@gmail.com	f	V-31122642	\N
Smick	Medina	messixcr7@gmail.com	t	V-012345	$2b$12$Iny0huxnBw8C/LcIPeqav.7my6W9DANrLkSQLqOnE5B9IeCqzg7w2
David	Labrador	CombatesAleatorios@gmail.com	t	V-1234567	$2b$12$ZCF13rinmtcRufb0vPhCIu5GlrLG1no3GhMTYcGQOZxdWnQWG887i
Erick	Ratatin	RatatinGaming@gmail.com	t	V-11223344	$2b$12$JFzL5Z1z9bZz6qd8p1RQI.qx1r6ii30ud15.TJEuJioQjvRczirpK
\.


--
-- Data for Name: vehiculo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vehiculo (placa, marca, modelo, ano, color, kilometraje, observaciones, activo, cliente_id) FROM stdin;
MK8DX	Toyota	Toyota	1700	Gris	5	Tiene un daño grave en el toyobobo	t	2
\.


--
-- Name: auditoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auditoria_id_seq', 1, false);


--
-- Name: cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cliente_id_seq', 3, true);


--
-- Name: factura_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.factura_id_seq', 1, false);


--
-- Name: mecanico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mecanico_id_seq', 1, true);


--
-- Name: orden_detalle_repuesto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orden_detalle_repuesto_id_seq', 1, false);


--
-- Name: orden_detalle_servicio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orden_detalle_servicio_id_seq', 1, false);


--
-- Name: orden_servicio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orden_servicio_id_seq', 1, true);


--
-- Name: proveedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.proveedor_id_seq', 1, true);


--
-- Name: refresh_token_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.refresh_token_id_seq', 6, true);


--
-- Name: rol_idrol_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rol_idrol_seq', 3, true);


--
-- Name: servicio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.servicio_id_seq', 1, false);


--
-- Name: supervisor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.supervisor_id_seq', 1, false);


--
-- Name: user_log_idsuer_log_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_log_idsuer_log_seq', 3, true);


--
-- Name: auditoria auditoria_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoria
    ADD CONSTRAINT auditoria_pkey PRIMARY KEY (id);


--
-- Name: cliente cliente_documento_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_documento_key UNIQUE (documento);


--
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id);


--
-- Name: factura factura_orden_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.factura
    ADD CONSTRAINT factura_orden_id_key UNIQUE (orden_id);


--
-- Name: factura factura_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.factura
    ADD CONSTRAINT factura_pkey PRIMARY KEY (id);


--
-- Name: mecanico mecanico_documento_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mecanico
    ADD CONSTRAINT mecanico_documento_key UNIQUE (documento);


--
-- Name: mecanico mecanico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mecanico
    ADD CONSTRAINT mecanico_pkey PRIMARY KEY (id);


--
-- Name: orden_detalle_repuesto orden_detalle_repuesto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_repuesto
    ADD CONSTRAINT orden_detalle_repuesto_pkey PRIMARY KEY (id);


--
-- Name: orden_detalle_servicio orden_detalle_servicio_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_servicio
    ADD CONSTRAINT orden_detalle_servicio_pkey PRIMARY KEY (id);


--
-- Name: orden_servicio orden_servicio_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_servicio
    ADD CONSTRAINT orden_servicio_pkey PRIMARY KEY (id);


--
-- Name: proveedor proveedor_documento_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedor
    ADD CONSTRAINT proveedor_documento_key UNIQUE (documento);


--
-- Name: proveedor proveedor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedor
    ADD CONSTRAINT proveedor_pkey PRIMARY KEY (id);


--
-- Name: refresh_token refresh_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_token
    ADD CONSTRAINT refresh_token_pkey PRIMARY KEY (id);


--
-- Name: repuesto repuesto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repuesto
    ADD CONSTRAINT repuesto_pkey PRIMARY KEY (codigo);


--
-- Name: rol rol_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (idrol);


--
-- Name: servicio servicio_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicio
    ADD CONSTRAINT servicio_pkey PRIMARY KEY (id);


--
-- Name: supervisor supervisor_documento_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supervisor
    ADD CONSTRAINT supervisor_documento_key UNIQUE (documento);


--
-- Name: supervisor supervisor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supervisor
    ADD CONSTRAINT supervisor_pkey PRIMARY KEY (id);


--
-- Name: user_log user_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_log
    ADD CONSTRAINT user_log_pkey PRIMARY KEY (idsuer_log);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (iduser);


--
-- Name: vehiculo vehiculo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehiculo
    ADD CONSTRAINT vehiculo_pkey PRIMARY KEY (placa);


--
-- Name: ix_auditoria_fecha_evento; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_auditoria_fecha_evento ON public.auditoria USING btree (fecha_evento);


--
-- Name: ix_auditoria_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_auditoria_id ON public.auditoria USING btree (id);


--
-- Name: ix_auditoria_registro_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_auditoria_registro_id ON public.auditoria USING btree (registro_id);


--
-- Name: ix_auditoria_tabla; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_auditoria_tabla ON public.auditoria USING btree (tabla);


--
-- Name: factura factura_orden_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.factura
    ADD CONSTRAINT factura_orden_id_fkey FOREIGN KEY (orden_id) REFERENCES public.orden_servicio(id) ON DELETE RESTRICT;


--
-- Name: refresh_token fk_idtoken_user_log; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_token
    ADD CONSTRAINT fk_idtoken_user_log FOREIGN KEY (user_log) REFERENCES public.user_log(idsuer_log);


--
-- Name: refresh_token fk_token_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_token
    ADD CONSTRAINT fk_token_user FOREIGN KEY (user_log) REFERENCES public.user_log(idsuer_log);


--
-- Name: user_log fk_userlog_rol; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_log
    ADD CONSTRAINT fk_userlog_rol FOREIGN KEY (idrol) REFERENCES public.rol(idrol);


--
-- Name: user_log fk_userlog_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_log
    ADD CONSTRAINT fk_userlog_user FOREIGN KEY (iduser) REFERENCES public.usuarios(iduser);


--
-- Name: orden_detalle_repuesto orden_detalle_repuesto_orden_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_repuesto
    ADD CONSTRAINT orden_detalle_repuesto_orden_id_fkey FOREIGN KEY (orden_id) REFERENCES public.orden_servicio(id) ON DELETE CASCADE;


--
-- Name: orden_detalle_repuesto orden_detalle_repuesto_repuesto_codigo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_repuesto
    ADD CONSTRAINT orden_detalle_repuesto_repuesto_codigo_fkey FOREIGN KEY (repuesto_codigo) REFERENCES public.repuesto(codigo) ON DELETE RESTRICT;


--
-- Name: orden_detalle_servicio orden_detalle_servicio_orden_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_servicio
    ADD CONSTRAINT orden_detalle_servicio_orden_id_fkey FOREIGN KEY (orden_id) REFERENCES public.orden_servicio(id) ON DELETE CASCADE;


--
-- Name: orden_detalle_servicio orden_detalle_servicio_servicio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_servicio
    ADD CONSTRAINT orden_detalle_servicio_servicio_id_fkey FOREIGN KEY (servicio_id) REFERENCES public.servicio(id) ON DELETE RESTRICT;


--
-- Name: orden_servicio orden_servicio_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_servicio
    ADD CONSTRAINT orden_servicio_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.cliente(id) ON DELETE RESTRICT;


--
-- Name: orden_servicio orden_servicio_mecanico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_servicio
    ADD CONSTRAINT orden_servicio_mecanico_id_fkey FOREIGN KEY (mecanico_id) REFERENCES public.mecanico(id) ON DELETE RESTRICT;


--
-- Name: orden_servicio orden_servicio_placa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_servicio
    ADD CONSTRAINT orden_servicio_placa_fkey FOREIGN KEY (placa) REFERENCES public.vehiculo(placa) ON DELETE RESTRICT;


--
-- Name: repuesto repuesto_proveedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repuesto
    ADD CONSTRAINT repuesto_proveedor_id_fkey FOREIGN KEY (proveedor_id) REFERENCES public.proveedor(id) ON DELETE SET NULL;


--
-- Name: vehiculo vehiculo_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehiculo
    ADD CONSTRAINT vehiculo_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.cliente(id) ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict Ko4n81VgQdkpwV6NNPLApIZGZak0EGGtxVSFj5sp3gJ0a2UbOo4aDUF8NjvZaLg

