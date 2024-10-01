import unittest
import json
from app import app, db, Animal

class AnimalAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_animal(self):
        response = self.client.post('/animais', data=json.dumps({
            'nome': 'Rex',
            'idade': 5,
            'raca': 'Labrador',
            'cidade': 'São Paulo',
            'data_perdido': '2023-01-01'
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Rex', response.data)

    def test_get_animals(self):
        self.client.post('/animais', data=json.dumps({
            'nome': 'Rex',
            'idade': 5,
            'raca': 'Labrador',
            'cidade': 'São Paulo',
            'data_perdido': '2023-01-01'
        }), content_type='application/json')

        response = self.client.get('/animais')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Rex', response.data)

    def test_update_animal(self):
        response = self.client.post('/animais', data=json.dumps({
            'nome': 'Rex',
            'idade': 5,
            'raca': 'Labrador',
            'cidade': 'São Paulo',
            'data_perdido': '2023-01-01'
        }), content_type='application/json')

        animal_id = json.loads(response.data)['id']
        
        response = self.client.put(f'/animais/{animal_id}', data=json.dumps({
            'nome': 'Rex Atualizado',
            'idade': 6,
            'raca': 'Labrador',
            'cidade': 'São Paulo',
            'data_perdido': '2023-01-01'
        }), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Rex Atualizado', response.data)

    def test_delete_animal(self):
        response = self.client.post('/animais', data=json.dumps({
            'nome': 'Rex',
            'idade': 5,
            'raca': 'Labrador',
            'cidade': 'São Paulo',
            'data_perdido': '2023-01-01'
        }), content_type='application/json')

        animal_id = json.loads(response.data)['id']
        
        response = self.client.delete(f'/animais/{animal_id}')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()
