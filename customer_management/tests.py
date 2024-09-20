from django.test import TestCase
from django.shortcuts import reverse


class HomePageTest(TestCase):

    def test_status_code(self):
        # TODO: test status code on HOME page
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

class SignUpViewTest(TestCase):

    #TODO: test status code on SIGNUP page
    def test_status_code(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")