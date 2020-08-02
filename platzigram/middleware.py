from django.shortcuts import redirect
from django.urls import reverse


"""Middleware platzigram"""

allowed_urls = [
                    reverse('users:update_profile'),
                    reverse('users:logout'),
                    reverse('admin:index')
                ]

class ProfileCompletionMiddleware:
    """All users have profile (bio,picture)"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self,request):
        """Code before view is called"""

        if not request.user.is_anonymous:
            profile = request.user.profile
            if not profile.picture or not profile.biography:
                if request.path not in allowed_urls:
                    return redirect('users:update_profile')    
        response = self.get_response(request)
        return response