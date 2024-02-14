"""
URL configuration for kingdomdeath project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from kingdomdeathapi.views import (
    login_user, register_user, PlayerView, SettlementView, ResourceView, MilestoneTypeView, MilestoneView, AbilityView, DisorderView, EventView, FightingArtView, WeaponProficiencyView)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'players', PlayerView, 'player')
router.register(r'settlements', SettlementView, 'settlement')
router.register(r'resources', ResourceView, 'resource')
router.register(r'milestone_types', MilestoneTypeView, 'milestone_type')
router.register(r'milestones', MilestoneView, 'milestone')
router.register(r'abilities', AbilityView, 'ability')
router.register(r'disorders', DisorderView, 'disorder')
router.register(r'events', EventView, 'event')
router.register(r'fighting_arts', FightingArtView, 'fighting_art')
router.register(r'weapon_proficiencies', WeaponProficiencyView, 'weapon_proficiency')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
