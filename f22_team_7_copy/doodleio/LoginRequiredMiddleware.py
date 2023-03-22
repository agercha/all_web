from django.contrib.auth.mixins import LoginRequiredMixin

class AuthRequiredMiddleware(LoginRequiredMixin):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home')) # or http response
        return None
