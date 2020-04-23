import os
import unittest

from application import create_app
from application.api.database import db
from application.api.models.person import Person
from application.api.models.attempt import Attempt


class DatabaseTestCase(unittest.TestCase):
    '''This class represents the database test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_person_creation(self):
        '''Test app can create a person'''
        with self.app.app_context():
            person = Person()
            self.assertIsInstance(person, Person)

    def test_attempt_creation(self):
        '''Test app can create an attempt'''
        with self.app.app_context():
            attempt = Attempt()
            self.assertIsInstance(attempt, Attempt)

    def test_person_store_instance(self):
        '''Test app can store a person instance using an instance method
        and retrieve it'''
        with self.app.app_context():
            person = Person()
            person.upsert_this()
            result = Person.query.filter_by(id=person.id).first()
            self.assertIsInstance(result, Person)

    def test_person_store_class(self):
        '''Test app can store a person instance using a class method
        and retrieve it'''
        with self.app.app_context():
            person = Person()
            Person.upsert(person)
            result = Person.query.filter_by(id=person.id).first()
            self.assertIsInstance(result, Person)

    def test_person_deletion_instance(self):
        '''Test app can delete a person instance using an instance method'''
        with self.app.app_context():
            person = Person()
            person.upsert_this()
            result = Person.query.first()
            self.assertIsInstance(result, Person)
            person.delete_this()
            result = Person.query.all()
            self.assertEqual(len(result), 0)

    def test_person_deletion_class(self):
        '''Test app can delete a person instance using a class method'''
        with self.app.app_context():
            person = Person()
            Person.upsert(person)
            result = Person.query.first()
            self.assertIsInstance(result, Person)
            Person.delete(person)
            result = Person.query.all()
            self.assertEqual(len(result), 0)

    def test_person_store_multiple_class(self):
        '''Test app can store a multiple person instances using a class method
        and retrieve them'''
        with self.app.app_context():
            people = [Person() for n in range(10)]
            Person.upsert(people)
            result = Person.query.all()
            self.assertEqual(len(result), len(people))
            self.assertIsInstance(result[0], Person)

    def test_person_deletion_multiple_class(self):
        '''Test app can delete multiple person instances using
        a class method'''
        with self.app.app_context():
            people = [Person() for n in range(10)]
            Person.upsert(people)
            result = Person.query.all()
            self.assertEqual(len(result), len(people))
            self.assertIsInstance(result[0], Person)
            Person.delete(people)
            result = Person.query.all()
            self.assertEqual(len(result), 0)

    def test_person_clear_all(self):
        '''Test app can delete all person instances using
        a class method'''
        with self.app.app_context():
            people = [Person() for n in range(10)]
            Person.upsert(people)
            result = Person.query.all()
            self.assertEqual(len(result), len(people))
            self.assertIsInstance(result[0], Person)
            Person.clear_all()
            result = Person.query.all()
            self.assertEqual(len(result), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
