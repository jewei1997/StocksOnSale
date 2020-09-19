from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from stocks import views

urlpatterns = [
    path('pe_ratios/', views.PeRatios.as_view()),
    path('market_caps/', views.MarketCaps.as_view()),
    path('percentage_change/<int:days>/', views.PercentageChange.as_view()),
    path('snp500/', views.Snp500.as_view()),
    path('dow/', views.Dow.as_view()),
    path('nasdaq/', views.Nasdaq.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
