from django.shortcuts import render
from .models import db_search

# Create your views here.

def category2(request):
    data = {
        'landmarks': [],
        'museums': [],
        'lifestyles': [],
        'parks': [],
        'historic_sites': []
    }

    landmark = db_search.objects.filter(category='랜드마크')[:10]
    museum = db_search.objects.filter(category='전시관')[:10]
    lifestyle = db_search.objects.filter(category='라이프스타일')[:10]
    park = db_search.objects.filter(category='공원')[:10]
    historic_site = db_search.objects.filter(category='유적지')[:10]
    data['landmarks'] = landmark
    data['museums'] = museum
    data['lifestyles'] = lifestyle
    data['parks'] = park
    data['historic_sites'] = historic_site

    return render(request, 'category2/category2.html', data)
