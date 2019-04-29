from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List


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


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()        
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={"item_text": "A new list item"})

        # check that an new item was saved to database
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={"item_text": "A new list item"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")        
