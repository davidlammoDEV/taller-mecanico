--
-- PostgreSQL database dump
--

\restrict I4vm8DH7lt8qQDDSD0WLCkav1U00dbxuoZ57TuOa6YKi7jzEKUXDUpIX8tHMBUR

-- Dumped from database version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)

-- Started on 2026-07-27 01:24:58 -04

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- TOC entry 216 (class 1259 OID 25552)
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
-- TOC entry 215 (class 1259 OID 25551)
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
-- TOC entry 3567 (class 0 OID 0)
-- Dependencies: 215
-- Name: cliente_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cliente_id_seq OWNED BY public.cliente.id;


--
-- TOC entry 228 (class 1259 OID 25639)
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
    CONSTRAINT ck_factura_metodo CHECK (((metodo)::text = ANY ((ARRAY['Efectivo'::character varying, 'Tarjeta de Crédito'::character varying, 'Tarjeta de Débito'::character varying, 'Transferencia'::character varying])::text[])))
);


ALTER TABLE public.factura OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 25638)
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
-- TOC entry 3568 (class 0 OID 0)
-- Dependencies: 227
-- Name: factura_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.factura_id_seq OWNED BY public.factura.id;


--
-- TOC entry 218 (class 1259 OID 25561)
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
-- TOC entry 217 (class 1259 OID 25560)
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
-- TOC entry 3569 (class 0 OID 0)
-- Dependencies: 217
-- Name: mecanico_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mecanico_id_seq OWNED BY public.mecanico.id;


--
-- TOC entry 230 (class 1259 OID 25655)
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
-- TOC entry 229 (class 1259 OID 25654)
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
-- TOC entry 3570 (class 0 OID 0)
-- Dependencies: 229
-- Name: orden_detalle_repuesto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orden_detalle_repuesto_id_seq OWNED BY public.orden_detalle_repuesto.id;


--
-- TOC entry 232 (class 1259 OID 25672)
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
-- TOC entry 231 (class 1259 OID 25671)
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
-- TOC entry 3571 (class 0 OID 0)
-- Dependencies: 231
-- Name: orden_detalle_servicio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orden_detalle_servicio_id_seq OWNED BY public.orden_detalle_servicio.id;


--
-- TOC entry 226 (class 1259 OID 25613)
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
    CONSTRAINT ck_orden_estado CHECK (((estado)::text = ANY ((ARRAY['Pendiente'::character varying, 'En Proceso'::character varying, 'Completado'::character varying, 'Cancelado'::character varying])::text[])))
);


ALTER TABLE public.orden_servicio OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 25612)
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
-- TOC entry 3572 (class 0 OID 0)
-- Dependencies: 225
-- Name: orden_servicio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orden_servicio_id_seq OWNED BY public.orden_servicio.id;


--
-- TOC entry 222 (class 1259 OID 25580)
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
-- TOC entry 221 (class 1259 OID 25579)
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
-- TOC entry 3573 (class 0 OID 0)
-- Dependencies: 221
-- Name: proveedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.proveedor_id_seq OWNED BY public.proveedor.id;


--
-- TOC entry 224 (class 1259 OID 25600)
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
-- TOC entry 220 (class 1259 OID 25571)
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
-- TOC entry 219 (class 1259 OID 25570)
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
-- TOC entry 3574 (class 0 OID 0)
-- Dependencies: 219
-- Name: servicio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.servicio_id_seq OWNED BY public.servicio.id;


--
-- TOC entry 223 (class 1259 OID 25588)
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
-- TOC entry 3368 (class 2604 OID 25555)
-- Name: cliente id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente ALTER COLUMN id SET DEFAULT nextval('public.cliente_id_seq'::regclass);


--
-- TOC entry 3375 (class 2604 OID 25642)
-- Name: factura id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.factura ALTER COLUMN id SET DEFAULT nextval('public.factura_id_seq'::regclass);


--
-- TOC entry 3369 (class 2604 OID 25564)
-- Name: mecanico id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mecanico ALTER COLUMN id SET DEFAULT nextval('public.mecanico_id_seq'::regclass);


--
-- TOC entry 3377 (class 2604 OID 25658)
-- Name: orden_detalle_repuesto id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_repuesto ALTER COLUMN id SET DEFAULT nextval('public.orden_detalle_repuesto_id_seq'::regclass);


--
-- TOC entry 3378 (class 2604 OID 25675)
-- Name: orden_detalle_servicio id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_servicio ALTER COLUMN id SET DEFAULT nextval('public.orden_detalle_servicio_id_seq'::regclass);


--
-- TOC entry 3373 (class 2604 OID 25616)
-- Name: orden_servicio id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_servicio ALTER COLUMN id SET DEFAULT nextval('public.orden_servicio_id_seq'::regclass);


--
-- TOC entry 3372 (class 2604 OID 25583)
-- Name: proveedor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedor ALTER COLUMN id SET DEFAULT nextval('public.proveedor_id_seq'::regclass);


--
-- TOC entry 3371 (class 2604 OID 25574)
-- Name: servicio id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicio ALTER COLUMN id SET DEFAULT nextval('public.servicio_id_seq'::regclass);


--
-- TOC entry 3382 (class 2606 OID 25559)
-- Name: cliente cliente_documento_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_documento_key UNIQUE (documento);


--
-- TOC entry 3384 (class 2606 OID 25557)
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id);


--
-- TOC entry 3402 (class 2606 OID 25648)
-- Name: factura factura_orden_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.factura
    ADD CONSTRAINT factura_orden_id_key UNIQUE (orden_id);


--
-- TOC entry 3404 (class 2606 OID 25646)
-- Name: factura factura_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.factura
    ADD CONSTRAINT factura_pkey PRIMARY KEY (id);


--
-- TOC entry 3386 (class 2606 OID 25569)
-- Name: mecanico mecanico_documento_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mecanico
    ADD CONSTRAINT mecanico_documento_key UNIQUE (documento);


--
-- TOC entry 3388 (class 2606 OID 25567)
-- Name: mecanico mecanico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mecanico
    ADD CONSTRAINT mecanico_pkey PRIMARY KEY (id);


--
-- TOC entry 3406 (class 2606 OID 25660)
-- Name: orden_detalle_repuesto orden_detalle_repuesto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_repuesto
    ADD CONSTRAINT orden_detalle_repuesto_pkey PRIMARY KEY (id);


--
-- TOC entry 3408 (class 2606 OID 25677)
-- Name: orden_detalle_servicio orden_detalle_servicio_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_servicio
    ADD CONSTRAINT orden_detalle_servicio_pkey PRIMARY KEY (id);


--
-- TOC entry 3400 (class 2606 OID 25622)
-- Name: orden_servicio orden_servicio_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_servicio
    ADD CONSTRAINT orden_servicio_pkey PRIMARY KEY (id);


--
-- TOC entry 3392 (class 2606 OID 25587)
-- Name: proveedor proveedor_documento_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedor
    ADD CONSTRAINT proveedor_documento_key UNIQUE (documento);


--
-- TOC entry 3394 (class 2606 OID 25585)
-- Name: proveedor proveedor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proveedor
    ADD CONSTRAINT proveedor_pkey PRIMARY KEY (id);


--
-- TOC entry 3398 (class 2606 OID 25606)
-- Name: repuesto repuesto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repuesto
    ADD CONSTRAINT repuesto_pkey PRIMARY KEY (codigo);


--
-- TOC entry 3390 (class 2606 OID 25578)
-- Name: servicio servicio_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicio
    ADD CONSTRAINT servicio_pkey PRIMARY KEY (id);


--
-- TOC entry 3396 (class 2606 OID 25594)
-- Name: vehiculo vehiculo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehiculo
    ADD CONSTRAINT vehiculo_pkey PRIMARY KEY (placa);


--
-- TOC entry 3414 (class 2606 OID 25649)
-- Name: factura factura_orden_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.factura
    ADD CONSTRAINT factura_orden_id_fkey FOREIGN KEY (orden_id) REFERENCES public.orden_servicio(id) ON DELETE RESTRICT;


--
-- TOC entry 3415 (class 2606 OID 25661)
-- Name: orden_detalle_repuesto orden_detalle_repuesto_orden_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_repuesto
    ADD CONSTRAINT orden_detalle_repuesto_orden_id_fkey FOREIGN KEY (orden_id) REFERENCES public.orden_servicio(id) ON DELETE CASCADE;


--
-- TOC entry 3416 (class 2606 OID 25666)
-- Name: orden_detalle_repuesto orden_detalle_repuesto_repuesto_codigo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_repuesto
    ADD CONSTRAINT orden_detalle_repuesto_repuesto_codigo_fkey FOREIGN KEY (repuesto_codigo) REFERENCES public.repuesto(codigo) ON DELETE RESTRICT;


--
-- TOC entry 3417 (class 2606 OID 25678)
-- Name: orden_detalle_servicio orden_detalle_servicio_orden_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_servicio
    ADD CONSTRAINT orden_detalle_servicio_orden_id_fkey FOREIGN KEY (orden_id) REFERENCES public.orden_servicio(id) ON DELETE CASCADE;


--
-- TOC entry 3418 (class 2606 OID 25683)
-- Name: orden_detalle_servicio orden_detalle_servicio_servicio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_detalle_servicio
    ADD CONSTRAINT orden_detalle_servicio_servicio_id_fkey FOREIGN KEY (servicio_id) REFERENCES public.servicio(id) ON DELETE RESTRICT;


--
-- TOC entry 3411 (class 2606 OID 25623)
-- Name: orden_servicio orden_servicio_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_servicio
    ADD CONSTRAINT orden_servicio_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.cliente(id) ON DELETE RESTRICT;


--
-- TOC entry 3412 (class 2606 OID 25633)
-- Name: orden_servicio orden_servicio_mecanico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_servicio
    ADD CONSTRAINT orden_servicio_mecanico_id_fkey FOREIGN KEY (mecanico_id) REFERENCES public.mecanico(id) ON DELETE RESTRICT;


--
-- TOC entry 3413 (class 2606 OID 25628)
-- Name: orden_servicio orden_servicio_placa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orden_servicio
    ADD CONSTRAINT orden_servicio_placa_fkey FOREIGN KEY (placa) REFERENCES public.vehiculo(placa) ON DELETE RESTRICT;


--
-- TOC entry 3410 (class 2606 OID 25607)
-- Name: repuesto repuesto_proveedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.repuesto
    ADD CONSTRAINT repuesto_proveedor_id_fkey FOREIGN KEY (proveedor_id) REFERENCES public.proveedor(id) ON DELETE SET NULL;


--
-- TOC entry 3409 (class 2606 OID 25595)
-- Name: vehiculo vehiculo_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehiculo
    ADD CONSTRAINT vehiculo_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.cliente(id) ON DELETE RESTRICT;


-- Completed on 2026-07-27 01:24:58 -04

--
-- PostgreSQL database dump complete
--

\unrestrict I4vm8DH7lt8qQDDSD0WLCkav1U00dbxuoZ57TuOa6YKi7jzEKUXDUpIX8tHMBUR

