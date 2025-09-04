-- CI-friendly: sempre começa limpo
DROP TABLE IF EXISTS atividade02;

CREATE TABLE IF NOT EXISTS atividade02 (
    id        SERIAL PRIMARY KEY,
    firstname VARCHAR(30)  NOT NULL,
    lastname  VARCHAR(100),
    age       INT,
    height    NUMERIC(4,2)
);

INSERT INTO atividade02 (id, firstname, lastname, age, height) VALUES
(1, 'Emilly', 'Isabelle Gomes', 19, 1.70),
(2, 'Kevin', 'Davi Assis', 76, 1.72),
(3, 'Henry', 'Manuel Moreira', 26, 1.86),
(4, 'Alice', 'Letícia dos Santos', 37, 1.75),
(5, 'Marina', 'Adriana Sabrina Rezende', 44, 1.50),
(6, 'Lorena', 'Antônia Carla Novaes', 71, 1.65),
(7, 'Otávio', 'Manuel Galvão', 51, 1.94),
(8, 'Elias', 'Samuel Murilo Corte Real', 49, 1.88),
(9, 'Caroline', 'Elza Vanessa Monteiro', 29, 1.79),
(10, 'Hadassa', 'Daiane Fátima Ribeiro', 66, 1.57),
(11, 'Adriana', 'Hadassa Souza', 60, 1.65),
(12, 'Rafaela', 'Lorena Santos', 40, 1.59),
(13, 'Kamilly', 'Marli Ayla Baptista', 76, 1.53),
(14, 'Bianca', 'Louise Almada', 66, 1.66),
(15, 'Matheus', 'Yuri de Paula', 30, 1.65),
(16, 'André', 'Francisco Osvaldo Lima', 49, 1.71),
(17, 'Marcelo', 'Mateus das Neves', 79, 1.88),
(18, 'Mariane', 'Gabrielly Clara Martins', 19, 1.79),
(19, 'Fátima', 'Isabel da Rosa', 47, 1.70),
(20, 'Evelyn', 'Raquel Laís da Conceição', 36, 1.84),
(21, 'Renan', 'Arthur da Cunha', 20, 1.80),
(22, 'Emanuel', 'Samuel da Cruz', 73, 1.73),
(23, 'Isaac', 'Fábio Tiago da Silva', 43, 1.82),
(24, 'Calebe', 'Rafael Danilo Vieira', 36, 1.73),
(25, 'Stella', 'Antônia Porto', 35, 1.50),
(26, 'Giovanni', 'Calebe Brito', 28, 1.73),
(27, 'Alice', 'Clarice da Luz', 51, 1.57),
(28, 'Marcos', 'Vinicius Thales Bento Almeida', 74, 1.69),
(29, 'Adriana', 'Lúcia Bianca Alves', 73, 1.63),
(30, 'Milena', 'Heloise Francisca Gonçalves', 41, 1.68)
ON CONFLICT (id) DO NOTHING;

-- deixa a sequência do SERIAL no último id existente
SELECT setval(
  pg_get_serial_sequence('atividade02', 'id'),
  COALESCE((SELECT MAX(id) FROM atividade02), 1),
  true
);
