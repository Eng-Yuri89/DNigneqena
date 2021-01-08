from core.models import Setting
from core.views.setting_views import setting


def site_profile(request):
    return {'setting': Setting.objects.get_or_create(id=request.user.id)

            }
