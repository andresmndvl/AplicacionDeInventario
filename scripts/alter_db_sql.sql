-- Agregar tabla usuarios si no existe
CREATE TABLE IF NOT EXISTS usuarios (
  nombre TEXT PRIMARY KEY,
  password TEXT NOT NULL,
  fecha_hora_ultimo_inicio TEXT,
  rol TEXT NOT NULL CHECK (rol IN ('ADMIN','PRODUCTOS','ALMACENES'))
);

-- Agregar columnas a productos y almacenes si no existen (SQLite permite ADD COLUMN)
ALTER TABLE productos ADD COLUMN fecha_hora_creacion TEXT DEFAULT (datetime('now')) ;
ALTER TABLE productos ADD COLUMN fecha_hora_ultima_modificacion TEXT ;
ALTER TABLE productos ADD COLUMN ultimo_usuario_en_modificar TEXT ;

ALTER TABLE almacenes ADD COLUMN fecha_hora_creacion TEXT DEFAULT (datetime('now')) ;
ALTER TABLE almacenes ADD COLUMN fecha_hora_ultima_modificacion TEXT ;
ALTER TABLE almacenes ADD COLUMN ultimo_usuario_en_modificar TEXT ;
