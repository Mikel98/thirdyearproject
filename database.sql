--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2

-- Started on 2020-05-20 23:24:13

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
-- TOC entry 210 (class 1259 OID 16497)
-- Name: sessionattendance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessionattendance (
    lecture_id integer NOT NULL,
    student_id integer NOT NULL,
    student_forename text NOT NULL,
    student_surname text NOT NULL,
    attendance_mark text NOT NULL
);


ALTER TABLE public.sessionattendance OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16483)
-- Name: ueafeedback; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ueafeedback (
    feedback_id integer NOT NULL,
    lecture_code text NOT NULL,
    feedback text,
    rating integer,
    lecture_id integer
);


ALTER TABLE public.ueafeedback OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 16481)
-- Name: ueafeedback_feedback_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ueafeedback_feedback_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ueafeedback_feedback_id_seq OWNER TO postgres;

--
-- TOC entry 2870 (class 0 OID 0)
-- Dependencies: 208
-- Name: ueafeedback_feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ueafeedback_feedback_id_seq OWNED BY public.ueafeedback.feedback_id;


--
-- TOC entry 207 (class 1259 OID 16433)
-- Name: ueasession; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ueasession (
    lectureid integer NOT NULL,
    session_name text NOT NULL,
    sessiondate date NOT NULL,
    sessiontime time without time zone NOT NULL,
    staff_id integer NOT NULL,
    lecture_code text NOT NULL,
    session_type text NOT NULL
);


ALTER TABLE public.ueasession OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 16431)
-- Name: uealectures_lectureid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.uealectures_lectureid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.uealectures_lectureid_seq OWNER TO postgres;

--
-- TOC entry 2871 (class 0 OID 0)
-- Dependencies: 206
-- Name: uealectures_lectureid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.uealectures_lectureid_seq OWNED BY public.ueasession.lectureid;


--
-- TOC entry 205 (class 1259 OID 16418)
-- Name: ueastaff; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ueastaff (
    staff_id integer NOT NULL,
    staff_forename text NOT NULL,
    staff_surname text NOT NULL,
    staff_email text NOT NULL,
    staff_faculty text
);


ALTER TABLE public.ueastaff OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16405)
-- Name: ueastudent; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ueastudent (
    student_id integer NOT NULL,
    student_forename text NOT NULL,
    student_surname text NOT NULL,
    student_email text NOT NULL
);


ALTER TABLE public.ueastudent OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16396)
-- Name: ueausers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ueausers (
    id integer NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    account_type text
);


ALTER TABLE public.ueausers OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 16394)
-- Name: ueausers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ueausers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ueausers_id_seq OWNER TO postgres;

--
-- TOC entry 2872 (class 0 OID 0)
-- Dependencies: 202
-- Name: ueausers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ueausers_id_seq OWNED BY public.ueausers.id;


--
-- TOC entry 2719 (class 2604 OID 16486)
-- Name: ueafeedback feedback_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueafeedback ALTER COLUMN feedback_id SET DEFAULT nextval('public.ueafeedback_feedback_id_seq'::regclass);


--
-- TOC entry 2718 (class 2604 OID 16436)
-- Name: ueasession lectureid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueasession ALTER COLUMN lectureid SET DEFAULT nextval('public.uealectures_lectureid_seq'::regclass);


--
-- TOC entry 2717 (class 2604 OID 16399)
-- Name: ueausers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueausers ALTER COLUMN id SET DEFAULT nextval('public.ueausers_id_seq'::regclass);


--
-- TOC entry 2733 (class 2606 OID 16504)
-- Name: sessionattendance pk_attend; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessionattendance
    ADD CONSTRAINT pk_attend PRIMARY KEY (lecture_id, student_id);


--
-- TOC entry 2731 (class 2606 OID 16491)
-- Name: ueafeedback ueafeedback_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueafeedback
    ADD CONSTRAINT ueafeedback_pkey PRIMARY KEY (feedback_id);


--
-- TOC entry 2727 (class 2606 OID 16464)
-- Name: ueasession uealectures_lectureid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueasession
    ADD CONSTRAINT uealectures_lectureid_key UNIQUE (lectureid);


--
-- TOC entry 2729 (class 2606 OID 16441)
-- Name: ueasession uealectures_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueasession
    ADD CONSTRAINT uealectures_pkey PRIMARY KEY (lectureid);


--
-- TOC entry 2725 (class 2606 OID 16425)
-- Name: ueastaff ueastaff_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueastaff
    ADD CONSTRAINT ueastaff_pkey PRIMARY KEY (staff_id);


--
-- TOC entry 2723 (class 2606 OID 16412)
-- Name: ueastudent ueastudent_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueastudent
    ADD CONSTRAINT ueastudent_pkey PRIMARY KEY (student_id);


--
-- TOC entry 2721 (class 2606 OID 16404)
-- Name: ueausers ueausers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueausers
    ADD CONSTRAINT ueausers_pkey PRIMARY KEY (id);


--
-- TOC entry 2738 (class 2606 OID 16505)
-- Name: sessionattendance lectureattendance_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessionattendance
    ADD CONSTRAINT lectureattendance_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.ueastudent(student_id);


--
-- TOC entry 2737 (class 2606 OID 16492)
-- Name: ueafeedback ueafeedback_lecture_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueafeedback
    ADD CONSTRAINT ueafeedback_lecture_id_fkey FOREIGN KEY (lecture_id) REFERENCES public.ueasession(lectureid);


--
-- TOC entry 2736 (class 2606 OID 16442)
-- Name: ueasession uealectures_staff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueasession
    ADD CONSTRAINT uealectures_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.ueastaff(staff_id);


--
-- TOC entry 2735 (class 2606 OID 16426)
-- Name: ueastaff ueastaff_staff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueastaff
    ADD CONSTRAINT ueastaff_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.ueausers(id);


--
-- TOC entry 2734 (class 2606 OID 16413)
-- Name: ueastudent ueastudent_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ueastudent
    ADD CONSTRAINT ueastudent_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.ueausers(id);


-- Completed on 2020-05-20 23:24:14

--
-- PostgreSQL database dump complete
--

