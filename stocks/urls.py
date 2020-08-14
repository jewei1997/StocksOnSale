from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from stocks import views

urlpatterns = [
    path('pe_ratios/', views.PeRatios.as_view()),
    path('market_caps/', views.MarketCaps.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
