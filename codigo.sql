-- criação
CREATE TABLE IF NOT EXISTS atividade02 (
  id SERIAL PRIMARY KEY,
  firstname TEXT NOT NULL,
  lastname  TEXT NOT NULL,
  age       INT  NOT NULL,
  height    NUMERIC(4,2) NOT NULL
);

-- seed idempotente
INSERT INTO atividade02 (id, firstname, lastname, age, height) VALUES
(1,'Fulano','da Silva',20,1.75),
(2,'Beltrano','Souza',22,1.78),
(3,'Ciclano','Pereira',21,1.81),
(4,'Maria','Oliveira',23,1.65),
(5,'João','Santos',24,1.80),
(6,'Ana','Lima',22,1.70),
(7,'Pedro','Costa',25,1.77),
(8,'Luiza','Almeida',21,1.68),
(9,'Carlos','Ferreira',26,1.82),
(10,'Julia','Gomes',20,1.60),
(11,'Rafael','Rocha',23,1.79),
(12,'Mariana','Carvalho',22,1.66),
(13,'Lucas','Ribeiro',24,1.74),
(14,'Fernanda','Teixeira',25,1.69),
(15,'Bruno','Barbosa',21,1.83),
(16,'Camila','Melo',22,1.72),
(17,'Gustavo','Martins',23,1.76),
(18,'Beatriz','Araujo',24,1.64),
(19,'Thiago','Cardoso',25,1.85),
(20,'Larissa','Pinto',21,1.67),
(21,'André','Batista',22,1.73),
(22,'Patrícia','Dias',23,1.62),
(23,'Diego','Nogueira',24,1.80),
(24,'Isabela','Cunha',25,1.71),
(25,'Rodrigo','Vieira',22,1.78),
(26,'Sophia','Ramos',23,1.63),
(27,'Felipe','Moreira',24,1.84),
(28,'Carolina','Lopes',25,1.70),
(29,'Eduardo','Barros',21,1.75),
(30,'Aline','Farias',22,1.66)
ON CONFLICT (id) DO NOTHING;

-- alinhar sequência do SERIAL ao maior id existente (idempotente)
-- (próximo nextval() será MAX(id)+1)
SELECT setval(
  pg_get_serial_sequence('atividade02','id'),
  COALESCE((SELECT MAX(id) FROM atividade02), 0),
  true
);
