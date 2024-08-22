from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


# class CustomAdapter(DefaultSocialAccountAdapter):
#     def get_login_redirect_url(self, request):
#         return 'new_profile/'

class AccountAdapterCustom(DefaultAccountAdapter):

	def get_login_redirect_url(self, request):
		if hasattr(request.user, 'dueno') or hasattr(request.user, 'empleado'):
			return '/backoffice/home/'
		if not hasattr(request.user, 'profile'):
			return '/new_profile/'
		return '/'
