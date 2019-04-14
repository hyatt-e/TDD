from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page


class HomePageTest(TestCase):

    # this is tested when the Djando Test Client is used
    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve('/')
    #     # resolve is the function Django uses internally to resolve
    #     # URLs and find what view function they should map to
    #     # We’re checking that resolve, when called with “/”, the root
    #     # of the site, finds a function called home_page

    #     self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        # request = HttpRequest()
        # We create an HttpRequest object, which is what Django will
        # see when a user’s browser asks for a page.

        # response = home_page(request)
        # We pass it to our home_page view, which gives us a response.
        # You won’t be surprised to hear that this object is an
        # instance of a class called HttpResponse.
        response = self.client.get("/")

        # html = response.content.decode('utf8')
        # Then, we extract the .content of the response. These are the 
        # raw bytes, the ones and zeros that would be sent down the 
        # wire to the user’s browser. We call .decode() to convert 
        # them into the string of HTML that’s being sent to the user.
        # html = response.content.decode("utf8")

        # self.assertTrue(html.startswith('<html>'))
        # We want it to start with an <html> tag which gets closed
        # at the end.

        # self.assertIn('<title>To-Do lists</title>', html)
        # And we want a <title> tag somewhere in the middle, with the words
        # "To-Do lists" in it—​because that’s what we specified in our functional test.

        # self.assertTrue(html.strip().endswith('</html>'))
        #   We want it to start with an <html> tag which gets closed
        #   at the end.
        # .strip() makes sure there's no whitespace at the end of the file
        
        self.assertTemplateUsed(response, "home.html")
        # .assertTemplateUsed is the test method Django TestCase class provides us.
        # it lets us check what template was used to render a response 
        # (NB - it will only work for responses that were retrieved by the test client)
        
    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={"item_text": "A new list item"})
        self.assertIn("A new list item", response.content.decode())
        self.assertTemplateUsed(response, "home.html")
        
          
