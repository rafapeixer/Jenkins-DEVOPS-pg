-- Seed compatível com PostgreSQL (rodará apenas no primeiro start do volume)
-- O banco já é criado pelo POSTGRES_DB. Não use 'USE ...' no Postgres.

CREATE TABLE IF NOT EXISTS atividade02(
  id INTEGER PRIMARY KEY,
  firstname VARCHAR(30) NOT NULL,
  lastname  VARCHAR(100),
  age       INTEGER,
  height    NUMERIC(4,2)
);

INSERT INTO atividade02 (id, firstname, lastname, age, height) VALUES
(1,'Emilly','Isabelle Gomes',19,1.70),
(2,'Kaio','Roberto Castro',26,1.71),
(3,'Stella','Beatriz Nunes',26,1.71),
(4,'Caroline','Mirella Dias',21,1.53),
(5,'Cecília','Heloísa Almeida',36,1.81),
(6,'Lorenzo','Luan Lima',30,1.66),
(7,'Emanuel','Paulo Ribeiro',18,1.79),
(8,'Elisa','Thaís Rocha',33,1.70),
(9,'Larissa','Maya Gomes',32,1.62),
(10,'Kevin','Igor da Paz',22,1.64),
(11,'Erick','Breno Gonçalves',24,1.61),
(12,'Isis','Rebeca Fernandes',29,1.78),
(13,'Arthur','Emanuel da Mata',24,1.62),
(14,'Maysa','Sophia Correia',23,1.73),
(15,'Guilherme','Guilherme Pinto',22,1.56),
(16,'Marcos','Roberto Ferreira',31,1.58),
(17,'Cauê','Rodrigues',20,1.60),
(18,'Kauã','Cardoso',35,1.84),
(19,'Isis','da Costa',28,1.79),
(20,'Marisa','Mendes',32,1.68);
