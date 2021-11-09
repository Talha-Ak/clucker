from django.urls import reverse
from microblogs.models import Post

def reverse_with_next(url_name, next_url):
    return reverse(url_name) + f"?next={next_url}"

def create_posts(author, from_count, to_count):
    """Create unique numbered posts for testing"""
    for count in range(from_count, to_count):
        text = f"Post__{count}"
        post = Post(author=author, text=text)
        post.save()

class LogInTester:
    """Helper class to test if the client is logged in."""
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()
