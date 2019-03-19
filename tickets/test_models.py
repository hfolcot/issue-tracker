from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .import choices
from .models import TicketUpdate, BugTicket, NewFeatureTicket

from accounts.models import DeveloperProfile

# Create your tests here.

class TestTicketUpdate(TestCase):
	def setUp(self):
		user = User.objects.create_user('updatetest', 'updatetest@test.test', 'testing321')
		bug = BugTicket.objects.create(customer=User.objects.get(username='updatetest'),
			title='Test Update',
			description='Test description')
		NewFeatureTicket.objects.create(customer=User.objects.get(username='updatetest'),
			title='Test Update on feature',
			description='Test description')
		TicketUpdate.objects.create(timestamp=timezone.now(),
			object_id=bug.id,
			content_type=bug.get_content_type,
			user = user)

	def test_time_spent_defaults_to_0(self):
		update = TicketUpdate.objects.get(pk=1)
		self.assertEqual(update.time_spent, 0)

	def test_correct_object_logged_against_update(self):
		update = TicketUpdate.objects.get(pk=1)
		bug = BugTicket.objects.get(pk=1)
		self.assertEqual(update.content_object, bug)




class TestBugTicket(TestCase):
	def setUp(self):
		dev = User.objects.create_user('unassigned', 'unassigned@test.test', 'testing321')
		DeveloperProfile.objects.create(user=dev, 
			first_name='Not currently', 
			last_name='assigned')
		User.objects.create_user('test', 'test@test.test', 'testing321')
		BugTicket.objects.create(customer=User.objects.get(username='test'),
			title='Test Bug',
			description='Test description')

	def test_timestamp_autonow(self):
		bug = BugTicket.objects.create(customer=User.objects.get(username='test'),
			title='Another Test Bug',
			description='Another Test description')
		self.assertTrue(bug.timestamp <= timezone.now())

	def test_assigned_defaults_to_unassigned(self):
		bug = BugTicket.objects.get(pk=1)
		self.assertEqual(bug.assigned.id, choices.UNASSIGNED)

	def test_status_defaults_to_pending(self):
		bug = BugTicket.objects.get(pk=1)
		self.assertEqual(bug.status, choices.PENDING)

	def test_priority_defaults_to_medium(self):
		bug = BugTicket.objects.get(pk=1)
		self.assertEqual(bug.priority, choices.MEDIUM)

	def test_rating_defaults_to_0(self):
		bug = BugTicket.objects.get(pk=1)
		self.assertEqual(bug.rating, 0)

	def test_time_spent_defaults_to_0(self):
		bug = BugTicket.objects.get(pk=1)
		self.assertEqual(bug.time_spent, 0)



class TestNewFeatureTicket(TestCase):

	def setUp(self):
		dev = User.objects.create_user('unassigned', 'unassigned@test.test', 'testing321')
		DeveloperProfile.objects.create(user=dev, 
			first_name='Not currently', 
			last_name='assigned')
		User.objects.create_user('test', 'test@test.test', 'testing321')
		NewFeatureTicket.objects.create(customer=User.objects.get(username='test'),
			title='Test feature',
			description='Test description')

	def test_assigned_defaults_to_unassigned(self):
		feature = NewFeatureTicket.objects.get(pk=1)
		self.assertEqual(feature.assigned.id, choices.UNASSIGNED)

	def test_quoted_defaults_to_false(self):
		feature = NewFeatureTicket.objects.get(pk=1)
		self.assertFalse(feature.quoted)

	def test_cost_defaults_to_0(self):
		feature = NewFeatureTicket.objects.get(pk=1)
		self.assertEqual(feature.cost, 0.00)

	def test_status_defaults_to_awaiting_quote(self):
		feature = NewFeatureTicket.objects.get(pk=1)
		self.assertEqual(feature.status, choices.AWAITINGQUOTE)

	def test_time_spent_defaults_to_0(self):
		feature = NewFeatureTicket.objects.get(pk=1)
		self.assertEqual(feature.time_spent, 0)

	def test_number_of_donations_defaults_to_0(self):
		feature = NewFeatureTicket.objects.get(pk=1)
		self.assertEqual(feature.number_of_donations, 0)

	def test_rating_defaults_to_0(self):
		feature = NewFeatureTicket.objects.get(pk=1)
		self.assertEqual(feature.rating, 0)
