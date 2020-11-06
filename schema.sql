--
-- PostgreSQL database dump
--
-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.2
-- Started on 2020-10-25 19:43:50
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
-- TOC entry 210 (class 1259 OID 16667)
-- Name: site_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.site_info (
    site_id integer NOT NULL,
    device character varying NOT NULL,
    date timestamp without time zone
);


ALTER TABLE public.site_info OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16665)
-- Name: site_info_site_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.site_info_site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 99999999
    CACHE 1
    CYCLE;

ALTER TABLE public.site_info_site_id_seq OWNER TO postgres;

--
-- TOC entry 2877 (class 0 OID 0)
-- Dependencies: 209
-- Name: site_info_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.site_info_site_id_seq OWNED BY public.site_info.site_id;

--
-- TOC entry 2739 (class 2604 OID 16670)
-- Name: site_info site_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_info ALTER COLUMN site_id SET DEFAULT nextval('public.site_info_site_id_seq'::regclass);

--
-- TOC entry 2878 (class 0 OID 0)
-- Dependencies: 209
-- Name: site_info_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.site_info_site_id_seq', 10000001, true);

--
-- TOC entry 2741 (class 2606 OID 16781)
-- Name: site_info device_id_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_info
    ADD CONSTRAINT device_id_unique UNIQUE (device);

--
-- TOC entry 2743 (class 2606 OID 16675)
-- Name: site_info site_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_info
    ADD CONSTRAINT site_info_pkey PRIMARY KEY (site_id);


--
-- TOC entry 211 (class 1259 OID 16676)
-- Name: raw_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.raw_history (
    site_id integer NOT NULL,
    date timestamp without time zone NOT NULL,
    value integer
);


ALTER TABLE public.raw_history OWNER TO postgres;

ALTER TABLE ONLY public.raw_history
    ADD CONSTRAINT raw_history_pkey PRIMARY KEY (site_id, date);


--
-- TOC entry 2741 (class 2606 OID 16686)
-- Name: raw_history fk_site_info; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw_history
    ADD CONSTRAINT fk_site_info FOREIGN KEY (site_id) REFERENCES public.site_info(site_id) ON DELETE CASCADE NOT VALID;


--
-- TOC entry 212 (class 1259 OID 16692)
-- Name: day_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.day_history (
    site_id integer NOT NULL,
    date timestamp without time zone NOT NULL,
    value integer
);


ALTER TABLE public.day_history OWNER TO postgres;

--
-- TOC entry 2740 (class 2606 OID 16696)
-- Name: day_history day_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.day_history
    ADD CONSTRAINT day_history_pkey PRIMARY KEY (site_id, date);


--
-- TOC entry 2741 (class 2606 OID 16697)
-- Name: day_history fk_site_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.day_history
    ADD CONSTRAINT fk_site_id FOREIGN KEY (site_id) REFERENCES public.site_info(site_id) ON DELETE CASCADE;


--
-- TOC entry 213 (class 1259 OID 16702)
-- Name: month_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.month_history (
    site_id integer NOT NULL,
    date timestamp without time zone NOT NULL,
    value integer
);

ALTER TABLE public.month_history OWNER TO postgres;

-- TOC entry 2740 (class 2606 OID 16706)
-- Name: month_history month_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.month_history
    ADD CONSTRAINT month_history_pkey PRIMARY KEY (site_id, date);


--
-- TOC entry 2741 (class 2606 OID 16707)
-- Name: month_history fk_site_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.month_history
    ADD CONSTRAINT fk_site_id FOREIGN KEY (site_id) REFERENCES public.site_info(site_id) ON DELETE CASCADE;


-- Completed on 2020-10-25 19:45:50

--
-- PostgreSQL database dump complete
--