\connect stocksdb stocksuser;

BEGIN TRANSACTION;

CREATE TABLE public.stocks_code (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) UNIQUE NOT NULL,
    code VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE public.stock (
    id SERIAL PRIMARY KEY,
    stock_id INTEGER REFERENCES public.stocks_code,
    stock_date DATE NOT NULL,
    open_val NUMERIC(10) NOT NULL,
    high_val NUMERIC(10) NOT NULL,
    low_val NUMERIC(10) NOT NULL,
    close_val NUMERIC(10) NOT NULL,
    adj_close_val NUMERIC(10) NOT NULL,
    volume NUMERIC(20) NOT NULL
);

END TRANSACTION;