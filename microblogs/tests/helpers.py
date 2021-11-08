from django.urls import reverse

def reverse_with_next(url_name, next_url):
    return reverse(url_name) + f"?next={next_url}"

class LogInTester:
    """Helper class to test if the client is logged in."""
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()
