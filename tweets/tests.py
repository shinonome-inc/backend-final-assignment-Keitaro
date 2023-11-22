from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import TWEET_MAX_LENGTH, Tweet

User = get_user_model()


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:home")
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/home.html")


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:create")
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")

    def test_success_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/create.html")

    def test_success_post(self):
        valid_data = {"content": "example"}
        response = self.client.post(self.url, valid_data)

        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(Tweet.objects.filter(content=valid_data["content"]).exists())

    def test_failure_post_with_empty_content(self):
        invalid_data = {"content": ""}
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tweet.objects.filter(content=invalid_data["content"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["content"])

    def test_failure_post_with_too_long_content(self):
        TWEET_LENGTH = TWEET_MAX_LENGTH + 1
        invalid_data = {"content": "a" * TWEET_LENGTH}
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tweet.objects.filter(content=invalid_data["content"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn(f"この値は {TWEET_MAX_LENGTH} 文字以下でなければなりません( {TWEET_LENGTH} 文字になっています)。", form.errors["content"])


# class TestTweetDetailView(TestCase):
#     def test_success_get(self):


# class TestTweetDeleteView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_incorrect_user(self):


# class TestLikeView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_liked_tweet(self):


# class TestUnLikeView(TestCase):

#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_unliked_tweet(self):
