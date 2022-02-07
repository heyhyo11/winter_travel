from main_page.models import hot_view

def hot_item_reset():
    hot_view.objects.all().delete()
    return