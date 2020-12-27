"""solarpanelproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('login', loginPage, name='loginPage'),
    path('loggedin/', loggedin, name='loggedin'),
    path('', upComingMatches, name="UpComingMatches"),
    path('matchresults', matchResults, name="matchresults"),
    path('org-login', orgLogin, name="organizerLoginPage"),
    path('allOrganizers', allOrganizers, name='allOrganizers'),
    path('allTournaments', allTournaments, name='allTournaments'),
    path('Tournaments', Tournaments, name='Tournaments'),
    path('allTeams', allTeams, name='allTeams'),
    path('allMatches', allMatches, name='allMatches'),
    path('addorganizer', addOrganizer, name='addorganizer'),
    path('addtournament', addtournament, name='addtournament'),
    path('AddTeamInTournament', AddTeamInTournament, name='AddTeamInTournament'),
    path('AddMatchInTournament', AddMatchInTournament, name='AddMatchInTournament'),
    path('teamsintournament/<int:pk>/', teamsintournament, name='teamsintournament'),
    path('teamsintournamentad/<int:pk>/', teamsintournamentad, name='teamsintournamentad'),
    path('matchesintournament/<int:pk>/', matchesintournament, name='matchesintournament'),
    path('matchesintournamentad/<int:pk>/', matchesintournamentad, name='matchesintournamentad'),
    path('upruntournaments', upruntournaments, name='upruntournaments'),
    path('allcaptain/', allcaptain, name='allcaptain'),
    path('createTeam/', createTeam, name='createTeam'),
    path('sendrequest/<int:tourid>/', sendrequest, name='sendrequest'),
    path('myrequests', myrequests,name="myrequests" ),
    path('approvereq/<int:reqid>', approvereq, name="approve"),
    path('rejectreq/<int:reqid>', rejectreq, name="reject"),
    path('latestrequests', latestrequests, name='latestrequests'),
    path('updatematchresult/<int:match>/', updatematchresult, name='updatematch'),
    path('addcaptain/', addcaptain, name='addcaptain'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)