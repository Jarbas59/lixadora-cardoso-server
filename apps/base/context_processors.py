from config.models import GoogleAnalytics, Logo, SEOHome, Scripts


def get_logo(request):
    return{
        'logo': Logo.objects.all().first()
    }

def get_seo(request):
    return {
        'seo': SEOHome.objects.first()
    }

def get_ga_code(request):
    return {
        'ga_code': GoogleAnalytics.objects.first()
    }

def get_scripts(request):
    return {
        'header_scripts': Scripts.objects.filter(place='HD', is_active=True),
        'footer_scripts': Scripts.objects.filter(place='FT', is_active=True),
    }
