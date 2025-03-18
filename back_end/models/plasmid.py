from datetime import datetime
from . import db

class Plasmid(db.Model):
    __tablename__ = 'plasmids'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    backbone = db.relationship('BackboneInfo', backref='plasmid', uselist=False)
    growth = db.relationship('GrowthInfo', backref='plasmid', uselist=False)
    gene_insert = db.relationship('GeneInsertInfo', backref='plasmid', uselist=False)
    cloning = db.relationship('CloningInfo', backref='plasmid', uselist=False)
    plasmid_map = db.relationship('PlasmidMap', backref='plasmid', uselist=False)

class BackboneInfo(db.Model):
    __tablename__ = 'backbone_info'
    id = db.Column(db.Integer, primary_key=True)
    plasmid_id = db.Column(db.Integer, db.ForeignKey('plasmids.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer)
    total_size = db.Column(db.Integer)
    vector_types = db.relationship('VectorType', secondary='backbone_vector_types')

class VectorType(db.Model):
    __tablename__ = 'vector_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class BackboneVectorType(db.Model):
    __tablename__ = 'backbone_vector_types'
    backbone_id = db.Column(db.Integer, db.ForeignKey('backbone_info.id'), primary_key=True)
    vector_type_id = db.Column(db.Integer, db.ForeignKey('vector_types.id'), primary_key=True)

class GrowthInfo(db.Model):
    __tablename__ = 'growth_info'
    id = db.Column(db.Integer, primary_key=True)
    plasmid_id = db.Column(db.Integer, db.ForeignKey('plasmids.id'), nullable=False)
    strain = db.Column(db.String(50))
    temperature = db.Column(db.String(20))
    copy_number = db.Column(db.String(20))
    resistance_types = db.relationship('ResistanceType', secondary='growth_resistance')

class ResistanceType(db.Model):
    __tablename__ = 'resistance_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class GrowthResistance(db.Model):
    __tablename__ = 'growth_resistance'
    growth_id = db.Column(db.Integer, db.ForeignKey('growth_info.id'), primary_key=True)
    resistance_id = db.Column(db.Integer, db.ForeignKey('resistance_types.id'), primary_key=True)

class GeneInsertInfo(db.Model):
    __tablename__ = 'gene_insert_info'
    id = db.Column(db.Integer, primary_key=True)
    plasmid_id = db.Column(db.Integer, db.ForeignKey('plasmids.id'), nullable=False)
    name = db.Column(db.String(255))
    species = db.Column(db.String(100))
    size = db.Column(db.Integer)
    promoter = db.Column(db.String(50))
    tags = db.relationship('Tag', secondary='gene_tags')

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class GeneTag(db.Model):
    __tablename__ = 'gene_tags'
    gene_id = db.Column(db.Integer, db.ForeignKey('gene_insert_info.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class CloningInfo(db.Model):
    __tablename__ = 'cloning_info'
    id = db.Column(db.Integer, primary_key=True)
    plasmid_id = db.Column(db.Integer, db.ForeignKey('plasmids.id'), nullable=False)
    method = db.Column(db.String(100))
    forward_primer = db.Column(db.Text)
    reverse_primer = db.Column(db.Text)

class PlasmidMap(db.Model):
    __tablename__ = 'plasmid_maps'
    id = db.Column(db.Integer, primary_key=True)
    plasmid_id = db.Column(db.Integer, db.ForeignKey('plasmids.id'), nullable=False)
    image_data = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.now)
