from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup

search_bp = Blueprint('search', __name__)

@search_bp.route('/', methods=['GET'])
def search():
    query = request.args.get('q')
    category = request.args.get('category', 'plasmids')
    base_url = 'https://www.addgene.org'
    search_url = f'{base_url}/search/catalog/{category}/?q={query}'

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        results = []
        for result in soup.select('.search-result-item'):
            try:
                title = result.select_one('.search-result-title a').get_text(strip=True)
                link = result.select_one('.search-result-title a')['href']
                plasmid_id = link.split('/')[-2]
                image = result.select_one('.map-column img')['src'] if result.select_one('.map-column img') else ''
                description = result.select_one('.product-detail-section .col-xs-10').get_text(strip=True) if result.select_one('.product-detail-section .col-xs-10') else 'No description'
                category = result.select_one('.result-item-category').get_text(strip=True) if result.select_one('.result-item-category') else 'Unknown category'
                
                # Additional info
                depositor = result.select_one('.depositor-name').get_text(strip=True) if result.select_one('.depositor-name') else ''
                availability = result.select_one('.availability-text').get_text(strip=True) if result.select_one('.availability-text') else ''

                results.append({
                    'id': plasmid_id,
                    'title': title,
                    'image': image,
                    'description': description,
                    'category': category,
                    'link': f'{base_url}{link}',
                    'depositor': depositor,
                    'availability': availability,
                    'source': 'addgene'
                })
            except Exception as e:
                print(f'Error processing result: {e}')
                continue

        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        print('Error fetching data:', e)
        return jsonify({
            'success': False,
            'message': f'Error fetching data: '
        }), 500

@search_bp.route('/getdata/<plasmid_id>', methods=['GET'])
def get_data(plasmid_id):
    base_url = 'https://www.addgene.org'
    detail_url = f'{base_url}/{plasmid_id}'

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(detail_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract basic information
        title = soup.select_one('div.panel-heading > div > h1 > span').get_text(strip=True) if soup.select_one('div.panel-heading > div > h1 > span') else ''
        category = '质粒'
        i_type = 'sgRNA/Cas9'
        description = soup.select_one('#plasmid-description-list > li:nth-child(1) > div > div.field-content').get_text(strip=True) if soup.select_one('#plasmid-description-list > li:nth-child(1) > div > div.field-content') else ''
        views = 5
        depositor = soup.select_one('#plasmid-description-list > li:nth-child(2) > div > div.field-content > a').get_text(strip=True) if soup.select_one('#plasmid-description-list > li:nth-child(2) > div > div.field-content > a') else ''
        publication = soup.select_one('#plasmid-description-list > li:nth-child(3) > div > div.field-content > a > cite').get_text(strip=True) if soup.select_one('#plasmid-description-list > li:nth-child(3) > div > div.field-content > a > cite') else ''
        prize_str = soup.select_one(f'#marginal-price-{plasmid_id}').get_text(strip=True) if soup.select_one(f'#marginal-price-{plasmid_id}') else '50'
        prize = round(int(prize_str) * 7.5)
        availability = 'academics and nonprofits only'
        img = soup.select_one('#maps-container img').get('src') if soup.select_one('#maps-container img') else ''
        
        # Backbone info
        backbone = {
            'name': soup.select_one('#detail-sections > div:nth-child(2) > section:nth-child(1) > ul > li:nth-child(1)').get_text(strip=True) if soup.select_one('#detail-sections > div:nth-child(2) > section:nth-child(1) > ul > li:nth-child(1)') else '',
            'type': [
                soup.select_one('#detail-sections > div:nth-child(2) > section:nth-child(1) > ul > li:nth-child(5)').get_text(strip=True) if soup.select_one('#detail-sections > div:nth-child(2) > section:nth-child(1) > ul > li:nth-child(5)') else ''
            ]
        }
        
        # Growth data
        growth = {
            'resistance': soup.select_one('#detail-sections > div:nth-child(2) > section:nth-child(2) > ul > li:nth-child(1)').get_text(strip=True) if soup.select_one('#detail-sections > div:nth-child(2) > section:nth-child(2) > ul > li:nth-child(1)') else '',
            'temperature': soup.select_one('#detail-sections > div:nth-child(2) > section:nth-child(2) > ul > li:nth-child(2)').get_text(strip=True) if soup.select_one('#detail-sections > div:nth-child(2) > section:nth-child(2) > ul > li:nth-child(2)') else '',
            'strain': soup.select_one('#detail-sections > div:nth-child(2) > section:nth-child(2) > ul > li:nth-child(3)').get_text(strip=True) if soup.select_one('#detail-sections > div:nth-child(2) > section:nth-child(2) > ul > li:nth-child(3)') else '',
            'copyNumber': soup.select_one('#detail-sections > div:nth-child(2) > section:nth-child(2) > ul > li:nth-child(4)').get_text(strip=True) if soup.select_one('#detail-sections > div:nth-child(2) > section:nth-child(2) > ul > li:nth-child(4)') else ''
        }
        
        # Gene insert data
        gene_insert = {
            'name': soup.select_one('#detail-sections > div:nth-child(3) > section:nth-child(1) > ul > li:nth-child(1)').get_text(strip=True) if soup.select_one('#detail-sections > div:nth-child(3) > section:nth-child(1) > ul > li:nth-child(1)') else '',
            'mutation': soup.select_one('#detail-sections > div:nth-child(3) > section:nth-child(1) > ul > li:nth-child(2)').get_text(strip=True) if soup.select_one('#detail-sections > div:nth-child(3) > section:nth-child(1) > ul > li:nth-child(2)') else '',
            'promoter': soup.select_one('#detail-sections > div:nth-child(3) > section:nth-child(1) > ul > li:nth-child(4)').get_text(strip=True) if soup.select_one('#detail-sections > div:nth-child(3) > section:nth-child(1) > ul > li:nth-child(4)') else '',
            'cloningMethod': soup.select_one('#detail-sections > div:nth-child(3) > section:nth-child(2) > ul > li:nth-child(1)').get_text(strip=True) if soup.select_one('#detail-sections > div:nth-child(3) > section:nth-child(2) > ul > li:nth-child(1)') else '',
            'sequence': 'GGT TTT CAG TAT AAT GTT ACA TGC G'
        }

        return jsonify({
            'success': True,
            'data': {
                'id': plasmid_id,
                'name': title,
                'category': category,
                'type': i_type,
                'description': description,
                'img': img,
                'views': views,
                'depositor': depositor,
                'publication': publication,
                'backbone': backbone,
                'markers': ['nourseothricin'],
                'growth': growth,
                'geneInsert': gene_insert,
                'prize': prize,
                'availability': availability,
                'sequences': [
                    {
                        'name': 'Complete Sequence',
                        'format': 'Genbank',
                        'size': '12.3 kb'
                    }
                ]
            }
        })

    except Exception as e:
        print('Error fetching data:', str(e))
        return jsonify({
            'success': False,
            'message': f'Failed to fetch plasmid data: '
        }), 500

