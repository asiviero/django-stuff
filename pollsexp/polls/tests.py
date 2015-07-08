from django.test import TestCase
from polls.models import Choice, Question

# Create your tests here.
class ModelTestCase(TestCase):

    def test_can_create_poll(self):
        question = Question.objects.create(
            question = "Question 1"
        )
        choice_1 = Choice.objects.create(
            text = "Choice 1",
            question = question
        )
        choice_2 = Choice.objects.create(
            text = "Choice 2",
            question = question
        )

        question_list = Question.objects.all()
        # What do I need checking?
        # If only one question was created
        self.assertEqual(Question.objects.count(), 1)
        # If the question label is correct
        question_generated = Question.objects.first()
        # If this question has two choices
        self.assertEqual(question_generated.choice_set.count(), 2)
        # If those choices were created with the right labels and
        # 0 votes
        choices_generated = question_generated.choice_set.all()
        self.assertEqual(question_generated.choice_set.all()[0].text,"Choice 1")
        self.assertEqual(question_generated.choice_set.all()[0].vote_count,0)
        self.assertEqual(question_generated.choice_set.all()[1].text,"Choice 2")
        self.assertEqual(question_generated.choice_set.all()[1].vote_count,0)
        #self.assertEqual(question.choice_set.all(), 2)

class HomePageTestCase(TestCase):

    def test_home_page_uses_home_template(self):
        response = self.client.get("/polls/")
        self.assertTemplateUsed(response,"home.html")

class ResultTestCase(TestCase):

    def test_template_for_result(self):
        question = Question.objects.create(
            question = "Question 1"
        )
        choice_1 = Choice.objects.create(
            text = "Choice 1",
            question = question
        )
        choice_2 = Choice.objects.create(
            text = "Choice 2",
            question = question
        )

        question_generated = Question.objects.first()
        response = self.client.get("/polls/%d/" % question_generated.id)
        self.assertTemplateUsed(response,"result.html")

class OptionsTestCase(TestCase):

    def test_template_for_options(self):
        question = Question.objects.create(
            question = "Question 1"
        )
        choice_1 = Choice.objects.create(
            text = "Choice 1",
            question = question
        )
        choice_2 = Choice.objects.create(
            text = "Choice 2",
            question = question
        )

        question_generated = Question.objects.first()
        response = self.client.get("/polls/%d/options/" % question_generated.id)
        self.assertTemplateUsed(response,"options.html")

    def test_vote_in_choice(self):
        question = Question.objects.create(
            question = "Question 1"
        )
        choice_1 = Choice.objects.create(
            text = "Choice 1",
            question = question
        )
        choice_2 = Choice.objects.create(
            text = "Choice 2",
            question = question
        )

        question_generated = Question.objects.first()
        choice_first = question_generated.choice_set.first()
        previous_votes = choice_first.vote_count
        choice_first.vote()
        new_first = question_generated.choice_set.first()
        self.assertEqual(new_first.vote_count,previous_votes+1)

    def test_check_redirect_after_vote(self):
        question = Question.objects.create(
            question = "Question 1"
        )
        choice_1 = Choice.objects.create(
            text = "Choice 1",
            question = question
        )
        choice_2 = Choice.objects.create(
            text = "Choice 2",
            question = question
        )

        question_generated = Question.objects.first()
        choice_first = question_generated.choice_set.first()

        response = self.client.post("/polls/%d/vote" % question_generated.id,
            data={"choice_id":choice_first.id}
        )

        self.assertRedirects(response, '/polls/%d/' % (question_generated.id,))
