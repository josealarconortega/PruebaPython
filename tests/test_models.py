import math
import os
import random
import statistics
import unittest
from typing import List

from scipy import stats

from application import create_app
from application.api.database import db
from application.api.models.people import People
from application.api.models.person import Person
from application.api.models.attempt import Attempt
from application.api.models.tree import Tree


class ModelsTestCase(unittest.TestCase):
    '''This class represents the models test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_person_rand_uniform(self):
        '''Test app can generate random numbers with a uniform distribution
        [IF FAILS TRY AGAIN, KOLMOGOROV-SMIRNOV & SHAPIRO-WILL TEST
        RESULTS ARE NOT ALWAYS CONCLUSIVE TO CONFIRM DISTRIBUTION FOR ALL
        POPULATIONS]'''
        numbers = ([Person.rand(False) for n in range(4000)])
        self.assertGreater(stats.kstest(numbers, 'uniform',
                                        args=(0, 1))[1], 0.05)
        self.assertLessEqual(stats.shapiro(numbers)[1], 0.05)

    def test_person_rand_gaussian(self):
        '''Test app can generate random numbers with a gaussian distribution
        [IF FAILS TRY AGAIN, KOLMOGOROV-SMIRNOV & SHAPIRO-WILL TEST
        RESULTS ARE NOT ALWAYS CONCLUSIVE TO CONFIRM DISTRIBUTION FOR ALL
        POPULATIONS]'''
        numbers = ([Person.rand(True) for n in range(4000)])
        self.assertGreater(stats.shapiro(numbers)[1], 0.05)
        self.assertLessEqual(stats.kstest(numbers, 'uniform',
                                          args=(0, 1))[1], 0.05)

    def test_person_random_pick(self):
        '''Test app can do a random pick from a population'''
        options = ([Person.rand(False) for n in range(10)])
        choice = Person.random_pick(options)
        self.assertIn(choice, options)

    def test_person_creation_uniform(self):
        '''Test app can create a person using uniform distribution'''
        with self.app.app_context():
            person = Person(False)
            self.assertIsInstance(person, Person)

    def test_person_creation_gaussian(self):
        '''Test app can create a person using uniform distribution'''
        with self.app.app_context():
            person = Person(True)
            self.assertIsInstance(person, Person)

    def test_person_p_recruit(self):
        '''Test app can calculate the chance of recruiting for
        a given Person'''
        with self.app.app_context():
            recruiter = Person(True)
            p_recruit = recruiter.p_recruit
            self.assertEqual(p_recruit,
                             recruiter.experience * recruiter.charisma *
                             (1.0 - math.log(len(recruiter.investors) + 1,
                                             10)))

    def test_person_p_invest(self):
        '''Test app can calculate the chance of investing for a given Person'''
        with self.app.app_context():
            investor = Person(True)
            p_invest = investor.p_invest
            self.assertEqual(p_invest,
                             investor.innocence * (1.0 - investor.experience))

    def test_person_max_weeks(self):
        '''Test app can calculate the maximum number of weeks for
        a given Person without recovering its investment'''
        with self.app.app_context():
            member = Person(True)
            max_weeks = member.max_weeks
            self.assertEqual(max_weeks,
                             math.floor(
                                 (1 - member.innocence) *
                                 member.experience *
                                 member.charisma * 10))

    def test_person_recruit_invest_attempt(self):
        '''Test app can run a successful recruit invest attempt'''
        with self.app.app_context():
            people = People.populate(3, True)

            recruiter = people[0]
            recruiter.first_week = 0
            recruiter.charisma = 1
            recruiter.experience = 1
            recruiter.innocence = 0

            investor = people[1]
            investor.innocence = 1
            investor.experience = 0
            investor.charisma = 0

            not_investor = people[2]
            not_investor.innocence = 0
            not_investor.experience = 1
            not_investor.charisma = 0

            successful = recruiter.recruit_attempt([investor], 1)
            self.assertIsInstance(successful, Attempt)
            self.assertIsInstance(successful.investor, Person)

            failed = recruiter.recruit_attempt([not_investor], 2)
            self.assertIsInstance(failed, Attempt)
            self.assertIsNone(failed.investor)

    def test_people_populate_uniform(self):
        '''Test app can create and store a population that
        follows a uniform distribution
        [IF FAILS TRY AGAIN, KOLMOGOROV-SMIRNOV & SHAPIRO-WILL TEST
        RESULTS ARE NOT ALWAYS CONCLUSIVE TO CONFIRM DISTRIBUTION FOR ALL
        POPULATIONS]'''
        with self.app.app_context():
            Person.clear_all()
            people = People.populate(4000, False)
            Person.upsert(people)
            results = Person.query.all()

            inn = ([person.innocence for person in results])
            exp = ([person.experience for person in results])
            cha = ([person.charisma for person in results])

            self.assertGreater(stats.kstest(inn, 'uniform',
                                            args=(0, 1))[1], 0.05)
            self.assertGreater(stats.kstest(exp, 'uniform',
                                            args=(0, 1))[1], 0.05)
            self.assertGreater(stats.kstest(cha, 'uniform',
                                            args=(0, 1))[1], 0.05)

            self.assertLessEqual(stats.shapiro(inn)[1], 0.05)
            self.assertLessEqual(stats.shapiro(exp)[1], 0.05)
            self.assertLessEqual(stats.shapiro(cha)[1], 0.05)

    def test_people_populate_gaussian(self):
        '''Test app can create and store a population that
        follows a gaussian distribution
        [IF FAILS TRY AGAIN, KOLMOGOROV-SMIRNOV & SHAPIRO-WILL TEST RESULTS
        ARE NOT ALWAYS CONCLUSIVE TO CONFIRM DISTRIBUTION FOR ALL
        POPULATIONS]'''
        with self.app.app_context():
            Person.clear_all()
            people = People.populate(4000, True)
            Person.upsert(people)
            results = Person.query.all()

            inn = ([person.innocence for person in results])
            exp = ([person.experience for person in results])
            cha = ([person.charisma for person in results])

            self.assertGreater(stats.shapiro(inn)[1], 0.05)
            self.assertGreater(stats.shapiro(exp)[1], 0.05)
            self.assertGreater(stats.shapiro(cha)[1], 0.05)

            self.assertLessEqual(stats.kstest(inn, 'uniform',
                                              args=(0, 1))[1], 0.05)
            self.assertLessEqual(stats.kstest(exp, 'uniform',
                                              args=(0, 1))[1], 0.05)
            self.assertLessEqual(stats.kstest(cha, 'uniform',
                                              args=(0, 1))[1], 0.05)

    def test_people_not_members(self):
        '''Test app can filter non-members from a given population'''
        with self.app.app_context():
            people = People.populate(10, True)
            mummy = people[0]
            mummy.first_week = 0
            self.assertEqual(len(people.not_members()), 9)

    def test_people_active_members(self):
        '''Test app can filter active members from a given population'''
        with self.app.app_context():
            people = People.populate(10, True)
            mummy = people[0]
            mummy.first_week = 0
            active_member = people[1]
            active_member.first_week = 1
            active_member.recruiter_id = mummy.id
            self.assertEqual(len(people.active_members()), 2)

    def test_people_inactive_members(self):
        '''Test app can filter inactive members from a given population'''
        with self.app.app_context():
            people = People.populate(10, True)
            mummy = people[0]
            mummy.first_week = 0
            active_member = people[1]
            active_member.first_week = 1
            active_member.recruiter_id = mummy.id
            inactive_member = people[1]
            inactive_member.first_week = 2
            inactive_member.last_week = 20
            inactive_member.recruiter_id = mummy.id
            self.assertEqual(len(people.inactive_members()), 1)

    def test_people_new_members(self):
        '''Test app can filter new members from a given population'''
        with self.app.app_context():
            people = People.populate(10, True)
            mummy = people[0]
            mummy.first_week = 0
            new_member = people[1]
            new_member.first_week = 1
            new_member.recruiter_id = mummy.id
            self.assertEqual(len(people.new_members(1)), 1)

    def test_people_leaving_members(self):
        '''Test app can filter leaving members from a given population'''
        with self.app.app_context():
            people = People.populate(10, True)
            mummy = people[0]
            mummy.first_week = 0
            active_member = people[1]
            active_member.first_week = 1
            active_member.recruiter_id = mummy.id
            inactive_member = people[1]
            inactive_member.first_week = 2
            inactive_member.last_week = 20
            inactive_member.recruiter_id = mummy.id
            self.assertEqual(len(people.leaving_members(20)), 1)

    def test_people_random_pick(self):
        '''Test app can do a random pick from a population'''
        with self.app.app_context():
            options = People.populate(10, True)
            choice = options.random_pick()
            self.assertIn(choice, options)

    def test_people_recruit_cycle_success(self):
        '''Test app can do a successful recruit cycle'''
        with self.app.app_context():
            people = People.populate(2, True)

            recruiter = people[0]
            recruiter.first_week = 0
            recruiter.charisma = 1
            recruiter.experience = 1
            recruiter.innocence = 0

            investor = people[1]
            investor.innocence = 1
            investor.experience = 0
            investor.charisma = 0

            successful = People.recruit_cycle(people, 1)
            self.assertEqual(len(successful), 1)
            self.assertIsInstance(successful[0], Person)

    def test_people_recruit_cycle_fail(self):
        '''Test app can do a failed recruit cycle'''
        with self.app.app_context():
            people = People.populate(2, True)

            recruiter = people[0]
            recruiter.first_week = 0
            recruiter.charisma = 1
            recruiter.experience = 1
            recruiter.innocence = 0

            not_investor = people[1]
            not_investor.innocence = 0
            not_investor.experience = 1
            not_investor.charisma = 0

            successful = People.recruit_cycle(people, 1)
            self.assertEqual(len(successful), 0)

    def test_people_get_children(self):
        '''Test app can get a Recruiter\'s direct Investors'''
        with self.app.app_context():
            people = People.populate(4, True)

            recruiter = people[0]
            recruiter.first_week = 0

            investor_1 = people[1]
            investor_1.first_week = 1
            investor_1.recruiter_id = recruiter.id

            investor_2 = people[2]
            investor_2.first_week = 2
            investor_2.recruiter_id = investor_1.id

            investor_3 = people[3]
            investor_3.first_week = 3
            investor_3.recruiter_id = recruiter.id

            children_0 = people.get_children(recruiter)
            self.assertEqual(len(children_0), 2)
            self.assertIsInstance(children_0, People)
            self.assertIsInstance(children_0[0], Person)
            self.assertIsInstance(children_0[1], Person)

            children_1 = people.get_children(investor_1)
            self.assertEqual(len(children_1), 1)
            self.assertIsInstance(children_1, People)
            self.assertIsInstance(children_1[0], Person)

            children_2 = people.get_children(investor_2)
            self.assertEqual(len(children_2), 0)
            self.assertIsInstance(children_2, People)

            children_3 = people.get_children(investor_3)
            self.assertEqual(len(children_3), 0)
            self.assertIsInstance(children_3, People)

    def test_people_get_descendants(self):
        '''Test app can get all Recruiter\'s Investors'''
        with self.app.app_context():
            people = People.populate(4, True)

            recruiter = people[0]
            recruiter.first_week = 0

            investor_1 = people[1]
            investor_1.first_week = 1
            investor_1.recruiter_id = recruiter.id

            investor_2 = people[2]
            investor_2.first_week = 2
            investor_2.recruiter_id = investor_1.id

            investor_3 = people[3]
            investor_3.first_week = 3
            investor_3.recruiter_id = recruiter.id

            descendants_0 = people.get_descendants(recruiter)
            self.assertEqual(len(descendants_0), 3)
            self.assertIsInstance(descendants_0, People)
            self.assertIsInstance(descendants_0[0], Person)
            self.assertIsInstance(descendants_0[1], Person)
            self.assertIsInstance(descendants_0[2], Person)

            descendants_1 = people.get_descendants(investor_1)
            self.assertEqual(len(descendants_1), 1)
            self.assertIsInstance(descendants_1, People)
            self.assertIsInstance(descendants_1[0], Person)

            descendants_2 = people.get_descendants(investor_2)
            self.assertEqual(len(descendants_2), 0)
            self.assertIsInstance(descendants_2, People)

            descendants_3 = people.get_descendants(investor_3)
            self.assertEqual(len(descendants_3), 0)
            self.assertIsInstance(descendants_3, People)

    def test_people_get_tree(self):
        '''Test app can get all Recruiter\'s Investor Tree'''
        with self.app.app_context():
            people = People.populate(4, True)

            recruiter = people[0]
            recruiter.first_week = 0

            investor_1 = people[1]
            investor_1.first_week = 1
            investor_1.recruiter_id = recruiter.id

            investor_2 = people[2]
            investor_2.first_week = 2
            investor_2.recruiter_id = investor_1.id

            investor_3 = people[3]
            investor_3.first_week = 3
            investor_3.recruiter_id = recruiter.id

            tree_0 = people.get_tree(recruiter)
            self.assertIsInstance(tree_0.member, Person)
            self.assertIsInstance(tree_0.children, list)
            self.assertEqual(len(tree_0.children), 2)
            self.assertIsInstance(tree_0.children[0], Tree)
            self.assertIsInstance(tree_0.children[1], Tree)

            tree_1 = tree_0.children[0]
            self.assertIsInstance(tree_1.member, Person)
            self.assertIsInstance(tree_1.children, list)
            self.assertEqual(len(tree_1.children), 1)
            self.assertIsInstance(tree_1.children[0], Tree)

            tree_2 = tree_1.children[0]
            self.assertIsInstance(tree_2.member, Person)
            self.assertIsInstance(tree_2.children, list)
            self.assertEqual(len(tree_2.children), 0)

            tree_3 = tree_0.children[1]
            self.assertIsInstance(tree_3.member, Person)
            self.assertIsInstance(tree_3.children, list)
            self.assertEqual(len(tree_3.children), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
