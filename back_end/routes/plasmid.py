from flask import Blueprint, request, jsonify, send_file
import base64
from models.plasmid import (
    Plasmid, BackboneInfo, VectorType, GrowthInfo,
    ResistanceType, GeneInsertInfo, Tag, PlasmidMap
)
from models import db
import os
from werkzeug.utils import secure_filename

plasmid_bp = Blueprint('plasmid', __name__)

@plasmid_bp.route('/', methods=['GET'])
def get_plasmids():
    try:
        # page = request.args.get('page', 1, type=int)
        # per_page = request.args.get('per_page', 10, type=int)
        pagination = Plasmid.query.paginate()
        
        plasmids = []
        for plasmid in pagination.items:
            plasmid_data = {
                'id': plasmid.id,
                'title': plasmid.title,
                'description': plasmid.description,
                'created_at': plasmid.created_at.isoformat(),
                'backbone': {},
                'growth': {},
                'gene_insert': {},
                'cloning': {},
                'source': 'own',
                'prize': 355
            }
            # ... populate plasmid data ...
            plasmids.append(plasmid_data)
        
        return jsonify({
            'success': True,
            'data': {
                'plasmids': plasmids,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': pagination.page
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取质粒列表失败: '
        }), 500

@plasmid_bp.route('/', methods=['POST'])
def create_plasmid():
    try:
        data = request.json
        
        plasmid = Plasmid(
            title=data['title'],
            description=data['description']
        )
        db.session.add(plasmid)
        db.session.flush()
        
        if data.get('backbone'):
            backbone = BackboneInfo(
                plasmid_id=plasmid.id,
                name=data['backbone']['name'],
                size=data['backbone'].get('size'),
                total_size=data['backbone'].get('total_size')
            )
            db.session.add(backbone)
            
            if data['backbone'].get('type'):
                for type_name in data['backbone']['type']:
                    vector_type = VectorType.query.filter_by(name=type_name).first()
                    if vector_type:
                        backbone.vector_types.append(vector_type)
        
        if data.get('growth'):
            growth = GrowthInfo(
                plasmid_id=plasmid.id,
                strain=data['growth'].get('strain'),
                temperature=data['growth'].get('temperature'),
                copy_number=data['growth'].get('copy_number')
            )
            db.session.add(growth)
            
            if data['growth'].get('resistance'):
                for resistance_name in data['growth']['resistance']:
                    resistance = ResistanceType.query.filter_by(name=resistance_name).first()
                    if resistance:
                        growth.resistance_types.append(resistance)
        
        if data.get('plasmid_map'):
            image_data = data['plasmid_map'].get('image')
            if isinstance(image_data, str):
                # image_data = image_data.split(',')[1]
                # image_bytes = base64.b64decode(image_data)
                plasmid_map = PlasmidMap(
                    plasmid_id=plasmid.id,
                    image_data=image_data
                )
                db.session.add(plasmid_map)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '质粒信息保存成功',
            'data': {'id': plasmid.id}
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'保存失败: '
        }), 500

@plasmid_bp.route('/<int:plasmid_id>', methods=['PUT'])
def update_plasmid(current_user, plasmid_id):
    try:
        plasmid = Plasmid.query.get_or_404(plasmid_id)
        data = request.json
        
        # Update plasmid basic info
        plasmid.title = data.get('title', plasmid.title)
        plasmid.description = data.get('description', plasmid.description)
        
        # Update related info
        if data.get('backbone'):
            # Update backbone info
            if plasmid.backbone:
                plasmid.backbone.name = data['backbone'].get('name', plasmid.backbone.name)
                # ...update other backbone fields...
        
        db.session.commit()
        return jsonify({'success': True, 'message': '更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@plasmid_bp.route('/<int:plasmid_id>', methods=['DELETE'])
def delete_plasmid(plasmid_id):
    try:
        plasmid = Plasmid.query.get_or_404(plasmid_id)
        db.session.delete(plasmid)
        db.session.commit()
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@plasmid_bp.route('/search', methods=['GET'])
def search_plasmids():
    try:
        query = request.args.get('query', '')
        search_filter = Plasmid.query.filter(
            db.or_(
                Plasmid.title.ilike(f'%{query}%'),
                Plasmid.description.ilike(f'%{query}%'),
                BackboneInfo.name.ilike(f'%{query}%')
            )
        ).join(
            BackboneInfo, BackboneInfo.plasmid_id == Plasmid.id, isouter=True
        )
        
        results = search_filter.all()
        plasmids = []
        for plasmid in results:
            plasmid_data = {
                'id': plasmid.id,
                'title': plasmid.title,
                'description': plasmid.description,
                'created_at': plasmid.created_at.isoformat(),
                'backbone': {},
                'growth': {},
                'gene_insert': {},
                'cloning': {},
                'source': 'own'
            }
            # ...populate plasmid data...
            plasmids.append(plasmid_data)
        
        return jsonify({
            'success': True,
            'data': plasmids
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'搜索失败: '
        }), 500

@plasmid_bp.route('getdata/<int:plasmid_id>', methods=['GET'])
def get_target_data(plasmid_id):
    try:
        plasmid = Plasmid.query.get_or_404(plasmid_id)
        plasmid_data = {
            'id': plasmid.id,
            'name': plasmid.title,
            'category': '质粒',
            'type': 'sgRNA/Cas9',  # Placeholder value
            'description': plasmid.description,
            'views': 3,  # Placeholder value
            'depositor': '少和生物',  # Placeholder value
            'publication': 'sgRNA/Cas9 (unpublished)',  # Placeholder value
            'backbone': {},
            'markers': ['nourseothricin'],  # Placeholder value
            'growth': {},
            'geneInsert': {},
            'prize': 85,  # Placeholder value
            'availability': 'academics and nonprofits only',  # Placeholder value
            'sequences': [
                {
                    'name': 'Complete Sequence',
                    'format': 'Genbank',
                    'size': '12.3 kb'
                }
            ]  # Placeholder value
        }
        
        # Populate backbone data
        if plasmid.backbone:
            plasmid_data['backbone'] = {
                'name': plasmid.backbone.name,
                'type': [vt.name for vt in plasmid.backbone.vector_types]
            }
        
        # Populate growth data
        if plasmid.growth:
            plasmid_data['growth'] = {
                'resistance': ', '.join([rt.name for rt in plasmid.growth.resistance_types]),
                'temperature': plasmid.growth.temperature,
                'strain': plasmid.growth.strain,
                'copyNumber': plasmid.growth.copy_number
            }
        
        # Populate gene insert data
        if plasmid.gene_insert:
            plasmid_data['geneInsert'] = {
                'name': plasmid.gene_insert.name,
                'mutation': 'Silent mutation of the CspCI site',  # Placeholder value
                'promoter': plasmid.gene_insert.promoter,
                'cloningMethod': 'Gibson Cloning',  # Placeholder value
                'sequencingPrimer': 'GGT TTT CAG TAT AAT GTT ACA TGC G'  # Placeholder value
            }
        
        return jsonify({
            'success': True,
            'data': plasmid_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取质粒信息失败: '
        }), 500
        
        
# upload file using POST, storage in '../files' forlder, return url
@plasmid_bp.route('/upload_file', methods=['POST'])
def upload_image():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file part'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No selected file'}), 400
        
        if file:
            filename = secure_filename(file.filename)
            folder_path = './files'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, filename)
            file.save(file_path)
            file_url = f'https://api.biocodedatabase.com/api/plasmids/get_file/{filename}'
            
            return jsonify({'success': True, 'file_url': file_url})
    except Exception as e:
        return jsonify({'success': False, 'message': f'File upload failed: '}), 500
    

# get image file using GET, return image file
@plasmid_bp.route('/get_file/<string:filename>', methods=['GET'])
def get_image(filename):
    try:
        folder_path = './files'
        file_path = os.path.join(folder_path, filename)
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return jsonify({'success': False, 'message': 'File not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': f'File retrieval failed: '}), 500