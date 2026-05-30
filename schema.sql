-- ============================================================
-- SISTEMA DE GESTIÓN DE MANTENIMIENTO DE EQUIPOS
-- Script de Base de Datos (SQLite)
-- ============================================================

-- Activar claves foráneas
PRAGMA foreign_keys = ON;

-- ============================================================
-- TABLAS
-- ============================================================

-- Tabla de Equipos
CREATE TABLE IF NOT EXISTS equipos (
    codigo          TEXT PRIMARY KEY,
    nombre          TEXT NOT NULL,
    tipo            TEXT NOT NULL,
    ubicacion       TEXT NOT NULL,
    fecha_instalacion TEXT NOT NULL,  -- formato YYYY-MM-DD
    estado          TEXT NOT NULL DEFAULT 'operativo'
        CHECK (estado IN ('operativo', 'en mantenimiento', 'fuera de servicio'))
);

-- Tabla de Técnicos
CREATE TABLE IF NOT EXISTS tecnicos (
    documento       TEXT PRIMARY KEY,
    nombre          TEXT NOT NULL,
    especialidad    TEXT NOT NULL,
    telefono        TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE
);

-- Tabla de Órdenes de Trabajo
CREATE TABLE IF NOT EXISTS ordenes_trabajo (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_solicitud     TEXT NOT NULL,  -- formato YYYY-MM-DD
    descripcion_falla   TEXT NOT NULL,
    prioridad           TEXT NOT NULL
        CHECK (prioridad IN ('alta', 'media', 'baja')),
    equipo_codigo       TEXT NOT NULL,
    tecnico_documento   TEXT NOT NULL,
    fecha_ejecucion     TEXT,           -- NULL hasta que se ejecute
    costo_repuestos     REAL DEFAULT 0.0,
    solucion_aplicada   TEXT,
    estado              TEXT NOT NULL DEFAULT 'pendiente'
        CHECK (estado IN ('pendiente', 'en proceso', 'completada', 'cancelada')),

    FOREIGN KEY (equipo_codigo)
        REFERENCES equipos(codigo)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    FOREIGN KEY (tecnico_documento)
        REFERENCES tecnicos(documento)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- ============================================================
-- ÍNDICES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_ordenes_equipo
    ON ordenes_trabajo(equipo_codigo);

CREATE INDEX IF NOT EXISTS idx_ordenes_tecnico
    ON ordenes_trabajo(tecnico_documento);

CREATE INDEX IF NOT EXISTS idx_ordenes_estado
    ON ordenes_trabajo(estado);

CREATE INDEX IF NOT EXISTS idx_ordenes_fecha_solicitud
    ON ordenes_trabajo(fecha_solicitud);

CREATE INDEX IF NOT EXISTS idx_equipos_estado
    ON equipos(estado);

-- ============================================================
-- DATOS DE EJEMPLO — EQUIPOS (15 registros)
-- ============================================================

INSERT OR IGNORE INTO equipos (codigo, nombre, tipo, ubicacion, fecha_instalacion, estado) VALUES
('EQ-001', 'Compresor Industrial Atlas', 'Compresor', 'Planta A - Zona 1', '2019-03-15', 'operativo'),
('EQ-002', 'Torno CNC Haas ST-10', 'Torno CNC', 'Planta A - Zona 2', '2020-06-22', 'operativo'),
('EQ-003', 'Bomba Centrífuga Grundfos', 'Bomba', 'Planta B - Cuarto de Bombas', '2018-11-10', 'en mantenimiento'),
('EQ-004', 'Caldera de Vapor Cleaver-Brooks', 'Caldera', 'Planta B - Zona Térmica', '2017-01-08', 'operativo'),
('EQ-005', 'Banda Transportadora Flexco', 'Banda Transportadora', 'Planta A - Línea 1', '2021-02-14', 'operativo'),
('EQ-006', 'Generador Eléctrico Caterpillar', 'Generador', 'Subestación Principal', '2016-09-30', 'fuera de servicio'),
('EQ-007', 'Soldadora MIG Lincoln Electric', 'Soldadora', 'Taller de Soldadura', '2022-04-18', 'operativo'),
('EQ-008', 'Prensa Hidráulica Enerpac', 'Prensa', 'Planta A - Zona 3', '2019-08-05', 'operativo'),
('EQ-009', 'Motor Eléctrico Siemens 50HP', 'Motor', 'Planta B - Línea 2', '2020-12-01', 'operativo'),
('EQ-010', 'Sistema HVAC Carrier', 'Climatización', 'Edificio Administrativo', '2021-07-20', 'operativo'),
('EQ-011', 'Fresadora CNC DMG Mori', 'Fresadora CNC', 'Planta A - Zona 2', '2023-01-10', 'operativo'),
('EQ-012', 'Montacargas Toyota 8FGU25', 'Montacargas', 'Bodega Principal', '2020-05-12', 'operativo'),
('EQ-013', 'Cortadora Láser Trumpf', 'Cortadora', 'Planta A - Zona 4', '2022-09-25', 'operativo'),
('EQ-014', 'Transformador ABB 500kVA', 'Transformador', 'Subestación Principal', '2015-04-03', 'operativo'),
('EQ-015', 'Puente Grúa Konecranes 10T', 'Grúa', 'Planta B - Nave Industrial', '2018-06-17', 'operativo');

-- ============================================================
-- DATOS DE EJEMPLO — TÉCNICOS (12 registros)
-- ============================================================

INSERT OR IGNORE INTO tecnicos (documento, nombre, especialidad, telefono, email) VALUES
('1001234567', 'Carlos Alberto Ramírez', 'Mecánica Industrial', '3101234567', 'carlos.ramirez@mantenimiento.com'),
('1009876543', 'Ana María López', 'Electricidad Industrial', '3209876543', 'ana.lopez@mantenimiento.com'),
('1005551234', 'Jorge Enrique Martínez', 'Instrumentación', '3155551234', 'jorge.martinez@mantenimiento.com'),
('1007778899', 'María Fernanda Torres', 'Soldadura Especializada', '3007778899', 'maria.torres@mantenimiento.com'),
('1002223344', 'Pedro Luis García', 'Hidráulica y Neumática', '3112223344', 'pedro.garcia@mantenimiento.com'),
('1006667788', 'Laura Cristina Díaz', 'Automatización', '3186667788', 'laura.diaz@mantenimiento.com'),
('1003334455', 'Andrés Felipe Rojas', 'Refrigeración y HVAC', '3053334455', 'andres.rojas@mantenimiento.com'),
('1008889900', 'Sandra Milena Vargas', 'Mecatrónica', '3148889900', 'sandra.vargas@mantenimiento.com'),
('1004445566', 'Diego Alejandro Herrera', 'Electrónica de Potencia', '3174445566', 'diego.herrera@mantenimiento.com'),
('1001112233', 'Camila Andrea Ruiz', 'Mecánica de Precisión', '3001112233', 'camila.ruiz@mantenimiento.com'),
('1005556677', 'Roberto Carlos Mendoza', 'Mantenimiento Predictivo', '3125556677', 'roberto.mendoza@mantenimiento.com'),
('1009990011', 'Valentina Salazar Pinto', 'Lubricación Industrial', '3199990011', 'valentina.salazar@mantenimiento.com');

-- ============================================================
-- DATOS DE EJEMPLO — ÓRDENES DE TRABAJO (15 registros)
-- Notas:
--   - Variedad de estados, prioridades y costos
--   - Algunas OTs antiguas sin completar (para reporte de atrasadas)
--   - Equipo EQ-003 con OT en proceso (estado 'en mantenimiento')
--   - Equipos EQ-013, EQ-014, EQ-015 sin OTs (para reporte sin mantenimiento)
-- ============================================================

INSERT OR IGNORE INTO ordenes_trabajo (fecha_solicitud, descripcion_falla, prioridad, equipo_codigo, tecnico_documento, fecha_ejecucion, costo_repuestos, solucion_aplicada, estado) VALUES
-- OTs completadas
('2025-01-10', 'Fuga de aceite en sistema hidráulico', 'alta', 'EQ-001', '1001234567', '2025-01-12', 350000.00, 'Reemplazo de sellos y empaques del sistema hidráulico', 'completada'),
('2025-02-05', 'Vibración excesiva en husillo principal', 'alta', 'EQ-002', '1001112233', '2025-02-08', 1200000.00, 'Cambio de rodamientos del husillo y balanceo dinámico', 'completada'),
('2025-03-18', 'Falla en contactor principal del motor', 'media', 'EQ-009', '1009876543', '2025-03-19', 280000.00, 'Reemplazo de contactor y revisión del circuito de potencia', 'completada'),
('2025-04-02', 'Desgaste en rodillos de la banda', 'media', 'EQ-005', '1001234567', '2025-04-05', 450000.00, 'Cambio de rodillos y alineación de la banda transportadora', 'completada'),
('2025-04-20', 'Falla en sistema de encendido', 'alta', 'EQ-006', '1004445566', '2025-04-25', 2500000.00, 'Reparación del módulo de control y cambio de bujías industriales', 'completada'),
('2025-05-01', 'Sobrecalentamiento del compresor', 'alta', 'EQ-001', '1001234567', '2025-05-03', 680000.00, 'Limpieza de radiador, cambio de aceite y filtros', 'completada'),
('2025-05-10', 'Fuga en válvula de seguridad', 'alta', 'EQ-004', '1002223344', '2025-05-11', 520000.00, 'Reemplazo de válvula de seguridad y prueba hidrostática', 'completada'),
('2025-06-15', 'Desgaste en electrodo de soldadura', 'baja', 'EQ-007', '1003334455', '2025-06-16', 150000.00, 'Cambio de antorcha y regulación del alimentador de alambre', 'completada'),

-- OTs en proceso
('2026-05-10', 'Cavitación en impulsor de la bomba', 'alta', 'EQ-003', '1002223344', NULL, 0.00, NULL, 'en proceso'),
('2026-05-18', 'Fallo en variador de frecuencia', 'media', 'EQ-009', '1006667788', NULL, 0.00, NULL, 'en proceso'),

-- OTs pendientes (algunas atrasadas — más de 7 días)
('2026-05-01', 'Desalineación del sistema de transmisión', 'media', 'EQ-012', '1001234567', NULL, 0.00, NULL, 'pendiente'),
('2026-05-05', 'Ruido anormal en sistema de enfriamiento', 'baja', 'EQ-010', '1003334455', NULL, 0.00, NULL, 'pendiente'),
('2026-05-20', 'Falla en cilindro hidráulico', 'alta', 'EQ-008', '1002223344', NULL, 0.00, NULL, 'pendiente'),

-- OT cancelada
('2025-07-01', 'Revisión preventiva programada', 'baja', 'EQ-011', '1008889900', NULL, 0.00, NULL, 'cancelada'),

-- OT completada adicional para EQ-002 (más intervenciones)
('2025-08-12', 'Error en sistema de control numérico', 'alta', 'EQ-002', '1006667788', '2025-08-15', 1800000.00, 'Actualización de firmware y reemplazo de tarjeta de control', 'completada');
