\connect stocksdb stocksuser;

BEGIN TRANSACTION;

INSERT INTO public.stocks_code(name, code) VALUES('Bitcoin', 'BTC-USD');
INSERT INTO public.stocks_code(name, code) VALUES('Dogecoin', 'DOGE-USD');
INSERT INTO public.stocks_code(name, code) VALUES('Shibainu', 'SHIB-USD');
INSERT INTO public.stocks_code(name, code) VALUES('Accenture', 'ACN');
INSERT INTO public.stocks_code(name, code) VALUES('Apple', 'AAPL');
INSERT INTO public.stocks_code(name, code) VALUES('Google', 'GOOG');


END TRANSACTION;