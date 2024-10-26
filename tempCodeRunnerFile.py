class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    raca = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    data_perdido = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'raca': self.raca,
            'cidade': self.cidade,
            'descricao': self.descricao,
            'data_perdido': self.data_perdido.isoformat()
        }
