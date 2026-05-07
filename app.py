from flask import Flask, render_template, request, jsonify
from db import get_supabase_client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
supabase = get_supabase_client()

@app.route('/')
def index():
    """Página principal - Dashboard"""
    try:
        # Obtener datos de la tabla (ajusta el nombre según tu BD)
        response = supabase.table('items').select('*').execute()
        items = response.data if response.data else []
        return render_template('index.html', items=items)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', items=[])

@app.route('/form')
def form_page():
    """Página del formulario"""
    return render_template('form.html')

@app.route('/api/items', methods=['GET'])
def get_items():
    """API para obtener todos los items"""
    try:
        response = supabase.table('items').select('*').execute()
        return jsonify({'success': True, 'data': response.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/items', methods=['POST'])
def create_item():
    """API para crear un nuevo item"""
    try:
        data = request.get_json()
        response = supabase.table('items').insert(data).execute()
        return jsonify({'success': True, 'data': response.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """API para actualizar un item"""
    try:
        data = request.get_json()
        response = supabase.table('items').update(data).eq('id', item_id).execute()
        return jsonify({'success': True, 'data': response.data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """API para eliminar un item"""
    try:
        response = supabase.table('items').delete().eq('id', item_id).execute()
        return jsonify({'success': True, 'message': 'Item eliminado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
