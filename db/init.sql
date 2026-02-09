CREATE TABLE habitos (
    id_habito SERIAL PRIMARY KEY,
    nombre_habito VARCHAR(100) NOT NULL,
    tipo_habito  VARCHAR(15) NOT NULL,
    descripcion VARCHAR(100) NOT NULL
);

CREATE TABLE fecha (
    id_fecha SERIAL PRIMARY KEY,
    fecha_habitos DATE NOT NULL
);

CREATE TABLE registro_habitos (
    id_registro SERIAL PRIMARY KEY,
    id_habito INT NOT NULL REFERENCES habitos(id_habito),
    id_fecha INT NOT NULL REFERENCES fecha(id_fecha),
    completado BOOLEAN NOT NULL DEFAULT FALSE
);
