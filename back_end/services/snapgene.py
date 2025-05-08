import tempfile
import os
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature
import re

def parse_snapgene_file(file):
    """
    Parse a SnapGene (.dna) or GenBank (.gb/.gbk) file and extract plasmid information
    that matches the format expected by DataEntry.vue
    """
    try:
        allowed_extensions = {'.dna', '.gb', '.gbk'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return None, '不支持的文件格式'

        with tempfile.NamedTemporaryFile(suffix=file_ext, delete=False) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        # For GenBank files, we can use BioPython's parser
        if file_ext in {'.gb', '.gbk'} or file_ext == '.dna':
            try:
                record = next(SeqIO.parse(temp_path, 'genbank'))
                parsed_data = parse_genbank_record(record)
                os.unlink(temp_path)
                return parsed_data, None
            except Exception as e:
                # If standard GenBank parsing fails for .dna, try alternative methods
                if file_ext == '.dna':
                    with open(temp_path, 'r', errors='ignore') as f:
                        content = f.read()
                    parsed_data = parse_dna_content(content, os.path.basename(file.filename))
                    os.unlink(temp_path)
                    return parsed_data, None
                else:
                    raise e
        
        os.unlink(temp_path)
        return None, '无法解析文件格式'
        
    except Exception as e:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)
        return None, str(e)

def parse_genbank_record(record):
    """Parse a BioPython SeqRecord from a GenBank file and extract structured data"""
    
    # Initialize the data structure to match DataEntry.vue's expectations
    data = {
        'title': record.name or record.id,
        'description': record.description,
        'backbone': {
            'name': '',
            'type': [],
            'size': '0',
            'total_size': f'{len(record.seq)}'
        },
        'growth': {
            'resistance': [],
            'temperature': '',
            'strain': '',
            'copy_number': ''
        },
        'gene_insert': {
            'name': '',
            'species': '',
            'size': 0,
            'promoter': '',
            'tags': []
        },
        'cloning': {
            'method': '',
            'forward_primer': '',
            'reverse_primer': ''
        }
    }
    
    # Extract information from source feature
    for feature in record.features:
        if feature.type == 'source':
            if 'organism' in feature.qualifiers:
                data['gene_insert']['species'] = feature.qualifiers['organism'][0]
            if 'mol_type' in feature.qualifiers:
                mol_type = feature.qualifiers['mol_type'][0].lower()
                if 'vector' in mol_type:
                    data['backbone']['name'] = record.name
    
    # Extract backbone information based on common patterns
    backbone_patterns = {
        'pet': 'pET', 
        'pbr': 'pBR', 
        'puc': 'pUC',
        'pcag': 'pCAG', 
        'plvx': 'pLVX', 
        'pcdna': 'pcDNA',
        'paav': 'pAAV'
    }
    
    for pattern, name in backbone_patterns.items():
        if pattern in record.name.lower():
            data['backbone']['name'] = name
            break
    
    # Infer vector type from name or features
    vector_types = []
    backbone_name = data['backbone']['name'].lower()
    
    if 'pet' in backbone_name:
        vector_types.append('原核表达')
    if 'pcdna' in backbone_name or 'pcag' in backbone_name:
        vector_types.append('真核表达')
    if 'plvx' in backbone_name or 'plko' in backbone_name:
        vector_types.append('慢病毒')
    if 'paav' in backbone_name:
        vector_types.append('AAV')
    if 'pcrispr' in backbone_name:
        vector_types.append('CRISPR')
    
    if not vector_types and 'shuttle' in record.description.lower():
        vector_types.append('穿梭质粒')
    
    data['backbone']['type'] = vector_types
    
    # Process features
    genes = []
    promoters = []
    resistance_markers = []
    tags = []
    primers = {'forward': [], 'reverse': []}
    
    for feature in record.features:
        # Handle CDS/gene features
        if feature.type in ['CDS', 'gene']:
            gene_name = feature.qualifiers.get('gene', [''])[0] or feature.qualifiers.get('label', [''])[0]
            product = feature.qualifiers.get('product', [''])[0]
            
            if gene_name:
                genes.append({
                    'name': gene_name,
                    'product': product,
                    'start': int(feature.location.start),
                    'end': int(feature.location.end),
                    'size': len(feature)
                })
            
            # Check for resistance genes
            resistance_keywords = {
                'amp': '氨苄青霉素(Amp)',
                'kan': '卡那霉素(Kan)',
                'cat': '氯霉素(Cm)',
                'tet': '四环素(Tet)',
                'bla': '氨苄青霉素(Amp)',
                'neo': '新霉素(Neo)',
                'hyg': '潮霉素(Hyg)',
                'bleo': '博莱霉素(Bleo)',
                'spec': '壮观霉素(Spec)'
            }
            
            gene_text = (gene_name + ' ' + product).lower()
            for key, value in resistance_keywords.items():
                if key in gene_text:
                    resistance_markers.append(value)
            
            # Check for tags
            tag_keywords = ['his', 'flag', 'ha', 'myc', 'gst', 'gfp', 'rfp', 'yfp', 'cfp', 
                           'mcherry', 'egfp', 'luciferase', '3xflag', 'v5']
            
            for tag in tag_keywords:
                if tag in gene_text.lower():
                    # Map to proper case format
                    tag_map = {
                        'his': 'His', 'flag': 'FLAG', 'ha': 'HA', 'myc': 'Myc',
                        'gst': 'GST', 'gfp': 'GFP', 'rfp': 'RFP', 'yfp': 'YFP',
                        'cfp': 'CFP', 'mcherry': 'mCherry', 'egfp': 'EGFP',
                        'luciferase': 'Luciferase', '3xflag': '3xFLAG', 'v5': 'V5'
                    }
                    tags.append(tag_map.get(tag, tag.upper()))
        
        # Handle promoter features
        elif feature.type == 'promoter':
            promoter_name = feature.qualifiers.get('label', [''])[0] or feature.qualifiers.get('note', [''])[0]
            if promoter_name:
                promoters.append(promoter_name)
        
        # Handle primer binding sites
        elif feature.type == 'primer_bind':
            primer_name = feature.qualifiers.get('label', [''])[0] or feature.qualifiers.get('note', [''])[0]
            if primer_name:
                strand = feature.location.strand
                primer_seq = str(record.seq[feature.location.start:feature.location.end])
                if strand > 0:
                    primers['forward'].append({'name': primer_name, 'sequence': primer_seq})
                else:
                    primers['reverse'].append({'name': primer_name, 'sequence': primer_seq})
    
    # Find main gene insert (usually the largest non-backbone gene)
    if genes:
        # Sort by size, descending
        genes.sort(key=lambda g: g['size'], reverse=True)
        main_gene = genes[0]
        data['gene_insert']['name'] = main_gene['name']
        data['gene_insert']['size'] = main_gene['size']
    
    # Add resistance information
    data['growth']['resistance'] = list(set(resistance_markers))
    
    # Add tag information
    data['gene_insert']['tags'] = list(set(tags))
    
    # Add promoter information
    if promoters:
        # Map to standard promoter names
        promoter_map = {
            't7': 'T7', 'cmv': 'CMV', 'cag': 'CAG', 'ef1': 'EF1α',
            'u6': 'U6', 'h1': 'H1', 'tre': 'TRE', 'ltr': 'LTR',
            'sv40': 'SV40', 'pgk': 'PGK', 'ubc': 'UBC', 'mscv': 'MSCV'
        }
        
        for promoter in promoters:
            for key, value in promoter_map.items():
                if key in promoter.lower():
                    data['gene_insert']['promoter'] = value
                    break
            
            if data['gene_insert']['promoter']:
                break
    
    # Add primer information
    if primers['forward'] and len(primers['forward']) > 0:
        data['cloning']['forward_primer'] = primers['forward'][0]['sequence']
    if primers['reverse'] and len(primers['reverse']) > 0:
        data['cloning']['reverse_primer'] = primers['reverse'][0]['sequence']
    
    # Estimate backbone size (total size minus inserted genes)
    gene_sizes = sum(g['size'] for g in genes)
    if gene_sizes > 0 and gene_sizes < len(record.seq):
        data['backbone']['size'] = f'{len(record.seq) - gene_sizes}'
    else:
        data['backbone']['size'] = f'{len(record.seq)}'
    
    # Look for cloning method hints in annotations
    cloning_methods = {
        'restriction': '限制性内切酶',
        'gibson': 'Gibson Assembly',
        'infusion': 'In-Fusion',
        'gateway': 'Gateway',
        'topo': 'TOPO',
        'golden gate': 'Golden Gate',
        'lic': 'LIC',
        'rf cloning': 'RF Cloning'
    }
    
    for comment in record.annotations.get('comment', []):
        for keyword, method in cloning_methods.items():
            if keyword in comment.lower():
                data['cloning']['method'] = method
                break
    
    # Infer copy number from ori descriptions
    copy_numbers = {'pbr322': '中拷贝', 'colE1': '高拷贝', 'pUC': '高拷贝', 'pMB1': '高拷贝'}
    for feature in record.features:
        if feature.type == 'rep_origin':
            for key, value in copy_numbers.items():
                if 'note' in feature.qualifiers and key.lower() in feature.qualifiers['note'][0].lower():
                    data['growth']['copy_number'] = value
                    break
    
    return data

def parse_dna_content(content, filename):
    """Parse raw content from a SnapGene .dna file if BioPython fails"""
    
    # Initialize with default values
    data = {
        'title': os.path.splitext(filename)[0],
        'description': 'Imported from SnapGene',
        'backbone': {
            'name': '',
            'type': [],
            'size': '',
            'total_size': ''
        },
        'growth': {
            'resistance': [],
            'temperature': '',
            'strain': '',
            'copy_number': ''
        },
        'gene_insert': {
            'name': '',
            'species': '',
            'size': 0,
            'promoter': '',
            'tags': []
        },
        'cloning': {
            'method': '',
            'forward_primer': '',
            'reverse_primer': ''
        }
    }
    
    # Try to extract LOCUS line
    locus_match = re.search(r'LOCUS\s+(\S+)\s+(\d+)\s+bp', content)
    if locus_match:
        data['title'] = locus_match.group(1)
        data['backbone']['total_size'] = f'{int(locus_match.group(2))}'
    
    # Try to extract DEFINITION line
    definition_match = re.search(r'DEFINITION\s+(.+?)(?=\n\w)', content, re.DOTALL)
    if definition_match:
        data['description'] = definition_match.group(1).strip()
    
    # Try to extract ORGANISM line
    organism_match = re.search(r'ORGANISM\s+(.+?)(?=\n\w)', content, re.DOTALL)
    if organism_match:
        data['gene_insert']['species'] = organism_match.group(1).strip()
    
    # Look for common resistance genes
    resistance_markers = []
    if 'ampR' in content or '/gene="bla"' in content:
        resistance_markers.append('氨苄青霉素(Amp)')
    if 'kanR' in content or '/gene="kan"' in content:
        resistance_markers.append('卡那霉素(Kan)')
    if 'chloramphenicol' in content or '/gene="cat"' in content:
        resistance_markers.append('氯霉素(Cm)')
    if 'tetracycline' in content or '/gene="tet"' in content:
        resistance_markers.append('四环素(Tet)')
    
    data['growth']['resistance'] = resistance_markers
    
    # Look for common tags
    tag_patterns = {
        'his': 'His',
        'flag': 'FLAG',
        'ha': 'HA',
        'myc': 'Myc',
        'gst': 'GST',
        'gfp': 'GFP',
        'rfp': 'RFP',
        'yfp': 'YFP',
        'cfp': 'CFP',
        'cherry': 'mCherry',
        'egfp': 'EGFP',
        'luciferase': 'Luciferase'
    }
    
    tags = []
    for pattern, tag in tag_patterns.items():
        if pattern in content.lower():
            tags.append(tag)
    
    data['gene_insert']['tags'] = tags
    
    # Extract gene names
    gene_matches = re.finditer(r'/gene="([^"]+)"', content)
    genes = [m.group(1) for m in gene_matches]
    
    # Find important genes (ignore common backbone genes)
    backbone_genes = {'bla', 'amp', 'cat', 'kan', 'tet', 'lacZ'}
    important_genes = [g for g in genes if g.lower() not in backbone_genes]
    
    if important_genes:
        data['gene_insert']['name'] = important_genes[0]
    
    # Look for promoters
    promoter_patterns = {
        't7': 'T7',
        'cmv': 'CMV',
        'cag': 'CAG',
        'ef1': 'EF1α',
        'u6': 'U6', 
        'h1': 'H1',
        'tre': 'TRE',
        'sv40': 'SV40'
    }
    
    for pattern, promoter in promoter_patterns.items():
        if f'{pattern} promoter' in content.lower():
            data['gene_insert']['promoter'] = promoter
            break
    
    # Try to extract information from file name
    filename_lower = filename.lower()
    
    # Infer backbone from filename
    backbone_patterns = {
        'pet': 'pET',
        'pbr': 'pBR',
        'puc': 'pUC',
        'pcag': 'pCAG',
        'plvx': 'pLVX',
        'pcdna': 'pcDNA',
        'paav': 'pAAV'
    }
    
    for pattern, name in backbone_patterns.items():
        if pattern in filename_lower:
            data['backbone']['name'] = name
            break
    
    # Infer vector type from filename
    vector_types = []
    
    if 'pet' in filename_lower:
        vector_types.append('原核表达')
    if 'pcdna' in filename_lower or 'pcag' in filename_lower:
        vector_types.append('真核表达')
    if 'plvx' in filename_lower or 'plko' in filename_lower:
        vector_types.append('慢病毒')
    if 'paav' in filename_lower:
        vector_types.append('AAV')
    if 'pcrispr' in filename_lower:
        vector_types.append('CRISPR')
    
    data['backbone']['type'] = vector_types
    
    return data
