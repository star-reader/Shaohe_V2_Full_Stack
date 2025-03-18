from flask import Blueprint, request, jsonify
from models.order import Order
from models import db
from utils import auth_jwt as jwt


token_required = jwt.token_required
admin_required = jwt.admin_required

order_db = Blueprint('order', __name__)

@order_db.route('/getOrder', methods=['GET'])
@token_required
def get_order(user):
    try:
        orders = Order.query.order_by(Order.order_time.desc()).filter_by(user_id=user.id).all()
        order_list = []
        for order in orders:
            order_data = {
                'order_id': order.order_id,
                'user_id': order.user_id,
                'username': order.username,
                'product_type': order.product_type,
                'product_name': order.product_name,
                'product_id': order.product_id,
                'order_time': order.order_time,
                'address': order.address,
                'quantity': order.quantity,
                'phone': order.phone,
                'prize': order.prize,
                'status': order.status
            }
            order_list.append(order_data)
        return jsonify({
            'success': True,
            'data': {
                'orders': order_list
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取订单失败: '
        }), 500
        
        
@order_db.route('/createOrder', methods=['POST'])
@token_required
def create_order(user):
    try:
        data = request.json
        print(data)
        print(user.id)
        order = Order(
            user_id=user.id,
            username=user.username,
            product_type=data['product_type'],
            product_name=data['product_name'],
            product_id=data['product_id'],
            order_time=data['order_time'],
            prize=data['prize'],
            quantity=data['quantity'],
            address=data['address'],
            phone=data['phone'],
            # quantity=order['quantity'],
            status=1
        )
        db.session.add(order)
        # db.session.flush()
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '订单创建成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'创建订单失败: '
        }), 500
        
@order_db.route('/updateOrder/<order_id>', methods=['POST'])
@admin_required
def update_order(order_id):
    try:
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify({
                'success': False,
                'message': '订单不存在'
            }), 404
        data = request.json
        order.status = data['status']
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '订单状态更新成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'更新订单失败: '
        }), 500
        
@order_db.route('/deleteOrder/<order_id>', methods=['POST'])
@admin_required
def delete_order(order_id):
    try:
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify({
                'success': False,
                'message': '订单不存在'
            }), 404
        db.session.delete(order)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': '订单删除成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'删除订单失败: '
        }), 500
    
@order_db.route('/all', methods=['GET'])
@admin_required
def get_all_order():
    try:
        orders = Order.query.order_by(Order.order_time.desc()).all()
        order_list = []
        for order in orders:
            order_data = {
            'order_id': order.order_id,
            'user_id': order.user_id,
            'username': order.username,
            'product_type': order.product_type,
            'product_name': order.product_name,
            'product_id': order.product_id,
            'order_time': order.order_time,
            'prize': order.prize,
            'status': order.status,
            'address': order.address,
            'quantity': order.quantity,
            'phone': order.phone,
            }
            order_list.append(order_data)
        return jsonify({
            'success': True,
            'data': {
            'orders': order_list
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取订单失败: '
        }), 500