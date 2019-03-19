from django.contrib.auth.models import User
from django.test import TestCase

from .models import Vote

from tickets.models import NewFeatureTicket, BugTicket

# Create your tests here.

class TestVote(TestCase):
	def setUp(self):
		user = User.objects.create_user('updatetest', 'updatetest@test.test', 'testing321')
		bug = BugTicket.objects.create(customer=User.objects.get(username='updatetest'),
			title='Test Vote',
			description='Test description')
		NewFeatureTicket.objects.create(customer=User.objects.get(username='updatetest'),
			title='Test Vote on feature',
			description='Test description')
		Vote.objects.create(positive_vote=True,
			user = user,
			content_type = bug.get_content_type,
			object_id = bug.id)

	def test_vote_assigned_to_correct_object(self):
		vote = Vote.objects.get(pk=1)
		bug = BugTicket.objects.get(title='Test Vote')
		self.assertEqual(vote.content_object, bug)