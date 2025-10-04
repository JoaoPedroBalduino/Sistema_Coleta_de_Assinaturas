-- ============================================================================
-- 1️⃣ CRIAR TABELA DE USUÁRIOS PARA LOGIN
-- ============================================================================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    perfil VARCHAR(20) DEFAULT 'coletor',
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir usuários de teste
INSERT INTO usuarios (username, password, nome, perfil) VALUES
('admin', 'admin123', 'Administrador do Sistema', 'admin'),
('coletor', 'coletor123', 'Coletor Padrão', 'coletor'),
('supervisor', 'super123', 'Supervisor Geral', 'supervisor');

-- ============================================================================
-- 2️⃣ CRIAR TABELA DE MUNICÍPIOS COMPLETA
-- ============================================================================
CREATE TABLE municipio (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    codigo_ibge VARCHAR(10),
    regiao VARCHAR(20),
    populacao INTEGER,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir municípios COMPLETOS das capitais brasileiras
INSERT INTO municipio (nome, estado, codigo_ibge, regiao, populacao) VALUES
('São Paulo', 'SP', '3550308', 'Sudeste', 12325232),
('Rio de Janeiro', 'RJ', '3304557', 'Sudeste', 6747815),
('Brasília', 'DF', '5300108', 'Centro-Oeste', 3094325),
('Salvador', 'BA', '2927408', 'Nordeste', 2886698),
('Fortaleza', 'CE', '2304400', 'Nordeste', 2703391),
('Belo Horizonte', 'MG', '3106200', 'Sudeste', 2521564),
('Manaus', 'AM', '1302603', 'Norte', 2219580),
('Curitiba', 'PR', '4106902', 'Sul', 1963726),
('Recife', 'PE', '2611606', 'Nordeste', 1653461),
('Goiânia', 'GO', '5208707', 'Centro-Oeste', 1555626),
('Porto Alegre', 'RS', '4314902', 'Sul', 1488252),
('Belém', 'PA', '1501402', 'Norte', 1506420),
('Guarulhos', 'SP', '3518800', 'Sudeste', 1398778),
('Campinas', 'SP', '3509502', 'Sudeste', 1213792),
('São Luís', 'MA', '2111300', 'Nordeste', 1108975),
('São Gonçalo', 'RJ', '3304904', 'Sudeste', 1091737),
('Maceió', 'AL', '2704302', 'Nordeste', 1025360),
('Duque de Caxias', 'RJ', '3301702', 'Sudeste', 924624),
('Natal', 'RN', '2408102', 'Nordeste', 890480),
('Teresina', 'PI', '2211001', 'Nordeste', 868075),
('Campo Grande', 'MS', '5002704', 'Centro-Oeste', 906092),
('Nova Iguaçu', 'RJ', '3303500', 'Sudeste', 821128),
('São Bernardo do Campo', 'SP', '3548708', 'Sudeste', 844483),
('João Pessoa', 'PB', '2507507', 'Nordeste', 817511),
('Santo André', 'SP', '3547809', 'Sudeste', 721368),
('Osasco', 'SP', '3534401', 'Sudeste', 698418);

-- ============================================================================
-- 3️⃣ CRIAR TABELA DE COLETORES COMPLETA
-- ============================================================================
CREATE TABLE coletor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14),
    rg VARCHAR(20),
    telefone VARCHAR(20),
    email VARCHAR(100),
    endereco TEXT,
    municipio_id INTEGER REFERENCES municipio(id),
    cargo VARCHAR(50),
    data_contratacao DATE,
    meta_mensal INTEGER DEFAULT 100,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir coletores COMPLETOS
INSERT INTO coletor (nome, cpf, rg, telefone, email, municipio_id, cargo, data_contratacao, meta_mensal) VALUES
('Ana Clara Silva Santos', '123.456.789-01', '12.345.678-9', '(11) 99999-0001', 'ana.silva@email.com', 1, 'Coordenadora Regional', '2024-01-15', 200),
('Carlos Roberto Santos Lima', '123.456.789-02', '12.345.679-0', '(21) 99999-0002', 'carlos.santos@email.com', 2, 'Coletor Senior', '2024-01-20', 150),
('Maria Fernanda Oliveira Costa', '123.456.789-03', '12.345.680-1', '(61) 99999-0003', 'maria.oliveira@email.com', 3, 'Supervisora', '2024-02-01', 180),
('João Paulo Pereira Alves', '123.456.789-04', '12.345.681-2', '(71) 99999-0004', 'joao.pereira@email.com', 4, 'Coletor Pleno', '2024-02-05', 120),
('Fernanda Regina Costa Souza', '123.456.789-05', '12.345.682-3', '(85) 99999-0005', 'fernanda.costa@email.com', 5, 'Coletor Junior', '2024-02-10', 100),
('Ricardo Henrique Lima Barbosa', '123.456.789-06', '12.345.683-4', '(31) 99999-0006', 'ricardo.lima@email.com', 6, 'Coletor Senior', '2024-02-15', 140),
('Juliana Cristina Ferreira Gomes', '123.456.789-07', '12.345.684-5', '(92) 99999-0007', 'juliana.ferreira@email.com', 7, 'Coordenadora', '2024-02-20', 190),
('Roberto Carlos Alves Mendes', '123.456.789-08', '12.345.685-6', '(41) 99999-0008', 'roberto.alves@email.com', 8, 'Coletor Pleno', '2024-03-01', 130),
('Patrícia Helena Souza Araújo', '123.456.789-09', '12.345.686-7', '(81) 99999-0009', 'patricia.souza@email.com', 9, 'Supervisora', '2024-03-05', 160),
('André Luis Barbosa Silva', '123.456.789-10', '12.345.687-8', '(62) 99999-0010', 'andre.barbosa@email.com', 10, 'Coletor Junior', '2024-03-10', 110),
('Camila Beatriz Rodrigues Costa', '123.456.789-11', '12.345.688-9', '(51) 99999-0011', 'camila.rodrigues@email.com', 11, 'Coletor Senior', '2024-03-15', 145),
('Marcos Antonio Mendes Lima', '123.456.789-12', '12.345.689-0', '(91) 99999-0012', 'marcos.mendes@email.com', 12, 'Coordenador', '2024-03-20', 170),
('Luciana Patricia Araújo Santos', '123.456.789-13', '12.345.690-1', '(86) 99999-0013', 'luciana.araujo@email.com', 20, 'Coletor Pleno', '2024-04-01', 125),
('Diego Fernando Cardoso Alves', '123.456.789-14', '12.345.691-2', '(67) 99999-0014', 'diego.cardoso@email.com', 21, 'Coletor Junior', '2024-04-05', 105),
('Renata Cristiane Gomes Ferreira', '123.456.789-15', '12.345.692-3', '(83) 99999-0015', 'renata.gomes@email.com', 24, 'Supervisora', '2024-04-10', 155);

-- ============================================================================
-- 4️⃣ CRIAR/ATUALIZAR TABELA DE ASSINATURAS
-- ============================================================================
CREATE TABLE IF NOT EXISTS eleitor_assinatura (
    id SERIAL PRIMARY KEY,
    nome_completo VARCHAR(200) NOT NULL,
    nome_mae VARCHAR(200) NOT NULL,
    titulo_eleitor VARCHAR(12) NOT NULL UNIQUE,
    zona_eleitoral INTEGER NOT NULL,
    secao_eleitoral INTEGER NOT NULL,
    municipio VARCHAR(100),
    municipio_uf VARCHAR(2),
    municipio_id INTEGER REFERENCES municipio(id),
    coletor VARCHAR(100),
    coletor_id INTEGER REFERENCES coletor(id),
    data_assinatura DATE NOT NULL,
    observacoes TEXT,
    status VARCHAR(20) DEFAULT 'ativa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 5️⃣ CRIAR VIEW PARA RELATÓRIO DE MUNICÍPIOS
-- ============================================================================
CREATE OR REPLACE VIEW vw_assinaturas_por_municipio AS
SELECT 
    m.id AS municipio_id,
    m.nome AS municipio,
    m.estado,
    m.regiao,
    m.populacao,
    COUNT(ea.id) AS total_assinaturas,
    ROUND((COUNT(ea.id)::decimal / NULLIF(m.populacao, 0)) * 100000, 2) AS assinaturas_por_100k_hab
FROM municipio m
LEFT JOIN eleitor_assinatura ea ON ea.municipio_id = m.id
GROUP BY m.id, m.nome, m.estado, m.regiao, m.populacao
ORDER BY total_assinaturas DESC;

-- ============================================================================
-- 6️⃣ CRIAR FUNÇÃO PARA TOTAL DE ASSINATURAS POR COLETOR
-- ============================================================================
CREATE OR REPLACE FUNCTION fn_total_assinaturas_coletor(p_coletor_id INT)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    total INT;
BEGIN
    SELECT COUNT(*) 
    INTO total
    FROM eleitor_assinatura
    WHERE coletor_id = p_coletor_id;

    RETURN COALESCE(total, 0);
END;
$$;

-- ============================================================================
-- 7️⃣ CRIAR FUNÇÃO PARA ESTATÍSTICAS DETALHADAS DO COLETOR
-- ============================================================================
CREATE OR REPLACE FUNCTION fn_estatisticas_coletor(p_coletor_id INT)
RETURNS TABLE(
    nome_coletor VARCHAR(100),
    total_assinaturas INT,
    meta_mensal INT,
    percentual_meta DECIMAL(5,2),
    ultima_assinatura DATE,
    municipio_atuacao VARCHAR(100)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.nome,
        COUNT(ea.id)::INT,
        c.meta_mensal,
        ROUND((COUNT(ea.id)::decimal / NULLIF(c.meta_mensal, 0)) * 100, 2),
        MAX(ea.data_assinatura),
        m.nome
    FROM coletor c
    LEFT JOIN eleitor_assinatura ea ON ea.coletor_id = c.id
    LEFT JOIN municipio m ON c.municipio_id = m.id
    WHERE c.id = p_coletor_id
    GROUP BY c.id, c.nome, c.meta_mensal, m.nome;
END;
$$;

-- ============================================================================
-- 8️⃣ CRIAR ÍNDICES PARA PERFORMANCE
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_eleitor_titulo ON eleitor_assinatura(titulo_eleitor);
CREATE INDEX IF NOT EXISTS idx_eleitor_municipio ON eleitor_assinatura(municipio_id);
CREATE INDEX IF NOT EXISTS idx_eleitor_coletor ON eleitor_assinatura(coletor_id);
CREATE INDEX IF NOT EXISTS idx_eleitor_data ON eleitor_assinatura(data_assinatura);
CREATE INDEX IF NOT EXISTS idx_eleitor_zona ON eleitor_assinatura(zona_eleitoral);

-- ============================================================================
-- 9️⃣ INSERIR ALGUMAS ASSINATURAS DE EXEMPLO (OPCIONAL)
-- ============================================================================
INSERT INTO eleitor_assinatura (nome_completo, nome_mae, titulo_eleitor, zona_eleitoral, secao_eleitoral, municipio, municipio_uf, municipio_id, coletor, coletor_id, data_assinatura, observacoes) VALUES
('José Silva Santos', 'Maria Silva', '123456789012', 1, 1, 'São Paulo', 'SP', 1, 'Ana Clara Silva Santos', 1, '2024-09-20', 'Primeira assinatura de teste'),
('Maria Santos Oliveira', 'Ana Santos', '234567890123', 1, 2, 'São Paulo', 'SP', 1, 'Ana Clara Silva Santos', 1, '2024-09-21', 'Segunda assinatura de teste'),
('João Pereira Costa', 'Joana Pereira', '345678901234', 2, 1, 'Rio de Janeiro', 'RJ', 2, 'Carlos Roberto Santos Lima', 2, '2024-09-22', 'Assinatura no Rio');

-- ============================================================================
-- 🔍 VERIFICAÇÃO FINAL
-- ============================================================================
SELECT 
    'Usuários criados: ' || COUNT(*) AS resultado FROM usuarios
UNION ALL
SELECT 
    'Municípios criados: ' || COUNT(*) FROM municipio
UNION ALL
SELECT 
    'Coletores criados: ' || COUNT(*) FROM coletor
UNION ALL
SELECT 
    'Assinaturas exemplo: ' || COUNT(*) FROM eleitor_assinatura;
