# This is where we write our functional tests with selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
import factory
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from polls.models import Choice, Question

class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
    username = 'admin'
    password = factory.PostGenerationMethodCall('set_password', '123456')

    is_superuser = True
    is_staff = True
    is_active = True

class ChoiceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Choice

class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question
"""
class AdminUserTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        admin_user = UserFactory.create()

    def tearDown(self):
        self.browser.quit()

    def test_can_access_admin_page(self):

        self.browser.get((self.live_server_url) + "/admin/")

        input_username = self.browser.find_element_by_id("id_username")
        input_username.send_keys("admin")

        input_password = self.browser.find_element_by_id("id_password")
        input_password.send_keys("123456")

        button_login = self.browser.find_element_by_class_name("submit-row").find_element_by_tag_name("input")
        button_login.click()

        # Checks if admin logged in successfuly
        user_tools = self.browser.find_element_by_id("user-tools")
        self.assertIn("admin",user_tools.text)

    def test_admin_can_create_poll(self):

        self.browser.get((self.live_server_url) + "/admin/")

        input_username = self.browser.find_element_by_id("id_username")
        input_username.send_keys("admin")

        input_password = self.browser.find_element_by_id("id_password")
        input_password.send_keys("123456")

        button_login = self.browser.find_element_by_class_name("submit-row").find_element_by_tag_name("input")
        button_login.click()
    """
class HomePageTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        admin_user = UserFactory.create()

        # Sets up question_list
        question = QuestionFactory.create(
            question = "Hey buddy, sup"
        )

        choice1 = ChoiceFactory.create(
            question = question,
            text = "Not much"
        )

        choice1 = ChoiceFactory.create(
            question = question,
            text = "And you?"
        )

    def tearDown(self):
        self.browser.quit()

    def test_can_see_home_page(self):

        self.browser.get((self.live_server_url)+"/polls/")

        title = self.browser.find_element_by_tag_name("h1").text
        self.assertEqual(title,"Poll app")

        # User sees list
        self.assertEqual(self.is_element_present(By.ID, "list_questions"),True)

        # User sees a single question
        list_questions = self.browser.find_element_by_id("list_questions").find_element_by_tag_name("tbody")
        self.assertEqual(len(list_questions.find_elements_by_tag_name("tr")),1)

        questions_rows = list_questions.find_elements_by_tag_name("tr")
        for row in questions_rows:
            # User sees a vote link
            self.assertEqual(len(row.find_elements_by_link_text("VOTE")),1)
            # User sees a result link
            self.assertEqual(len(row.find_elements_by_link_text("RESULTS")),1)

        # User clicks on the first results button
        questions_rows[0].find_element_by_link_text("RESULTS").click()

        # Check if user was redirected to a proper page
        self.assertRegex(self.browser.current_url,"polls/\d+/")

        # Check if new page has a results table with id "question_results"
        self.assertEqual(len(self.browser.find_elements_by_id("question_results")),1)

        # Goes back to main url
        self.browser.get((self.live_server_url)+"/polls/")

        # Clicks in vote
        list_questions = self.browser.find_element_by_id("list_questions").find_element_by_tag_name("tbody")
        questions_rows = list_questions.find_elements_by_tag_name("tr")
        questions_rows[0].find_element_by_link_text("VOTE").click()

        # Sees two options, selects the first, hits confirm
        list_options = self.browser.find_element_by_id("options")
        option_first = list_options.find_elements_by_tag_name("li")[0].find_element_by_tag_name("input")
        option_first.click()

        submit_buttom = self.browser.find_element_by_id("submit")
        submit_buttom.click()

        # Checks if redirected to right page
        self.assertRegex(self.browser.current_url,"polls/\d+/")

        # Check if first option value is 1
        results_table_body = self.browser.find_element_by_id("question_results").find_element_by_tag_name("tbody")
        result_value = results_table_body.find_elements_by_tag_name("tr")[0].find_elements_by_tag_name("td")[-1].text

        self.assertEqual(result_value,"1")
        # Close browser, then open again to vote again
        self.browser.quit()

        self.browser = webdriver.Firefox()
        self.browser.get((self.live_server_url)+"/polls/")

        # Clicks in vote
        list_questions = self.browser.find_element_by_id("list_questions").find_element_by_tag_name("tbody")
        questions_rows = list_questions.find_elements_by_tag_name("tr")
        questions_rows[0].find_element_by_link_text("VOTE").click()

        # Sees two options, selects the first, hits confirm
        list_options = self.browser.find_element_by_id("options")
        option_first = list_options.find_elements_by_tag_name("li")[0].find_element_by_tag_name("input")
        option_first.click()

        submit_buttom = self.browser.find_element_by_id("submit")
        submit_buttom.click()

        # Checks if redirected to right page
        self.assertRegex(self.browser.current_url,"polls/\d+/")

        # Check if first option value is 2
        results_table_body = self.browser.find_element_by_id("question_results").find_element_by_tag_name("tbody")
        result_value = results_table_body.find_elements_by_tag_name("tr")[0].find_elements_by_tag_name("td")[-1].text

        self.assertEqual(result_value,"2")
        
    def is_element_present(self, how, what):
        try: self.browser.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True
