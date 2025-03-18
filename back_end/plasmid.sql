
-- 创建质粒表
CREATE TABLE IF NOT EXISTS plasmids (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建载体信息表
CREATE TABLE IF NOT EXISTS backbone_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plasmid_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    size INT,
    total_size INT,
    FOREIGN KEY (plasmid_id) REFERENCES plasmids(id) ON DELETE CASCADE
);

-- 创建载体类型关联表
CREATE TABLE IF NOT EXISTS vector_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- 创建载体-类型关联表
CREATE TABLE IF NOT EXISTS backbone_vector_types (
    backbone_id INT NOT NULL,
    vector_type_id INT NOT NULL,
    PRIMARY KEY (backbone_id, vector_type_id),
    FOREIGN KEY (backbone_id) REFERENCES backbone_info(id) ON DELETE CASCADE,
    FOREIGN KEY (vector_type_id) REFERENCES vector_types(id) ON DELETE CASCADE
);

-- 创建培养信息表
CREATE TABLE IF NOT EXISTS growth_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plasmid_id INT NOT NULL,
    strain VARCHAR(50),
    temperature VARCHAR(20),
    copy_number VARCHAR(20),
    FOREIGN KEY (plasmid_id) REFERENCES plasmids(id) ON DELETE CASCADE
);

-- 创建抗性表
CREATE TABLE IF NOT EXISTS resistance_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- 创建培养-抗性关联表
CREATE TABLE IF NOT EXISTS growth_resistance (
    growth_id INT NOT NULL,
    resistance_id INT NOT NULL,
    PRIMARY KEY (growth_id, resistance_id),
    FOREIGN KEY (growth_id) REFERENCES growth_info(id) ON DELETE CASCADE,
    FOREIGN KEY (resistance_id) REFERENCES resistance_types(id) ON DELETE CASCADE
);

-- 创建基因/插入片段信息表
CREATE TABLE IF NOT EXISTS gene_insert_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plasmid_id INT NOT NULL,
    name VARCHAR(255),
    species VARCHAR(100),
    size INT,
    promoter VARCHAR(50),
    FOREIGN KEY (plasmid_id) REFERENCES plasmids(id) ON DELETE CASCADE
);

-- 创建标签表
CREATE TABLE IF NOT EXISTS tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- 创建基因-标签关联表
CREATE TABLE IF NOT EXISTS gene_tags (
    gene_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (gene_id, tag_id),
    FOREIGN KEY (gene_id) REFERENCES gene_insert_info(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- 创建克隆信息表
CREATE TABLE IF NOT EXISTS cloning_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plasmid_id INT NOT NULL,
    method VARCHAR(100),
    forward_primer TEXT,
    reverse_primer TEXT,
    FOREIGN KEY (plasmid_id) REFERENCES plasmids(id) ON DELETE CASCADE
);

-- 创建质粒图谱表
CREATE TABLE IF NOT EXISTS plasmid_maps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plasmid_id INT NOT NULL,
    image_data MEDIUMBLOB,
    FOREIGN KEY (plasmid_id) REFERENCES plasmids(id) ON DELETE CASCADE
);

-- 插入预设的载体类型数据
INSERT INTO vector_types (name) VALUES 
('原核表达'), ('真核表达'), ('穿梭质粒'), ('慢病毒'), ('腺病毒'),
('AAV'), ('报告基因'), ('基因编辑'), ('CRISPR'), ('shRNA'), ('sgRNA');

-- 插入预设的抗性数据
INSERT INTO resistance_types (name) VALUES 
('氨苄青霉素(Amp)'), ('卡那霉素(Kan)'), ('氯霉素(Cm)'), ('四环素(Tet)'),
('潮霉素(Hyg)'), ('新霉素(Neo)'), ('博莱霉素(Bleo)'), ('壮观霉素(Spec)');

-- 插入预设的标签数据
INSERT INTO tags (name) VALUES 
('His'), ('FLAG'), ('HA'), ('Myc'), ('GST'), ('GFP'), ('RFP'), ('YFP'), ('CFP'),
('mCherry'), ('EGFP'), ('Luciferase'), ('3xFLAG'), ('V5'); 