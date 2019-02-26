from django.urls import resolve
from django.test import TestCase
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        # resolve is the function Django uses internally to resolve
        # URLs and find what view function they should map to
        # We’re checking that resolve, when called with “/”, the root
        # of the site, finds a function called home_page

        self.assertEqual(found.func, home_page)
