from .models import Profile

def set_user_profile(request):

    profile = None

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        
    return {'profile': profile}