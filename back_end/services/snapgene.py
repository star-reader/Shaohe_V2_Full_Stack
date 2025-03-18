import tempfile
import os
from Bio import SeqIO
import base64
import subprocess

def extract_features(record):
    """Extract features from a sequence record"""
    features = {
        'promoters': [],
        'genes': [],
        'regulatory': [],
        'misc': []
    }
    
    for feature in record.features:
        if feature.type == 'promoter':
            features['promoters'].append({
                'name': feature.qualifiers.get('label', [''])[0],
                'location': str(feature.location)
            })
        elif feature.type in ['CDS', 'gene']:
            features['genes'].append({
                'name': feature.qualifiers.get('gene', [''])[0],
                'product': feature.qualifiers.get('product', [''])[0],
                'location': str(feature.location)
            })
        # Add more feature types as needed
    
    return features

def parse_snapgene_file(file):
    try:
        allowed_extensions = {'.dna', '.gb', '.gbk'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return None, '不支持的文件格式'

        with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        record = next(SeqIO.parse(temp_path, 'genbank' if file_ext in {'.gb', '.gbk'} else 'snapgene'))
        
        features = extract_features(record)
        
        data = {
            'name': record.name,
            'description': record.description,
            'sequence_length': len(record.seq),
            'features': features,
            'circular': record.annotations.get('topology', '') == 'circular'
        }
        
        os.unlink(temp_path)
        return data, None
        
    except Exception as e:
        if 'temp_path' in locals():
            os.unlink(temp_path)
        return None, str(e)
