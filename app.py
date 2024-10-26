
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from models import db, Animal
from database import init_db
from datetime import datetime




# Inicializa o banco de dados na criação do contexto da aplicação
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    raca = db.Column(db.String(80), nullable=False)
    cidade = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    data_perdido = db.Column(db.Date, nullable=False)

@app.route('/animais', methods=['GET', 'POST'])
def manage_animals():
    if request.method == 'GET':
        query_params = request.args
        query = Animal.query
        
        if 'nome' in query_params:
            query = query.filter(Animal.nome.ilike(f"%{query_params['nome']}%"))
        if 'idade' in query_params:
            query = query.filter(Animal.idade == query_params['idade'])
        if 'raca' in query_params:
            query = query.filter(Animal.raca.ilike(f"%{query_params['raca']}%"))
        if 'cidade' in query_params:
            query = query.filter(Animal.cidade.ilike(f"%{query_params['cidade']}%"))

        animais = query.all()
        return jsonify([animal.to_dict() for animal in animais]), 200

    elif request.method == 'POST':
        data = request.json
        new_animal = Animal(
            nome=data['nome'],
            idade=data['idade'],
            raca=data['raca'],
            cidade=data['cidade'],
            descricao=data.get('descricao', ''),
            data_perdido=datetime.strptime(data['data_perdido'], '%Y-%m-%d').date()
        )
        db.session.add(new_animal)
        db.session.commit()
        return jsonify(new_animal.to_dict()), 201

@app.route('/animais/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def animal_detail(id):
    animal = Animal.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(animal.to_dict()), 200

    elif request.method == 'PUT':
        data = request.json
        animal.nome = data['nome']
        animal.idade = data['idade']
        animal.raca = data['raca']
        animal.cidade = data['cidade']
        animal.descricao = data.get('descricao', animal.descricao)
        animal.data_perdido = datetime.strptime(data['data_perdido'], '%Y-%m-%d').date()
        db.session.commit()
        return jsonify(animal.to_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(animal)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
