from django.shortcuts import render

# Create your views here.
from datetime import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import *

from.models import *
from django.utils import timezone
# Create your views here.


@csrf_exempt
def loginPage(request):
    return render(request, "examples/pages/login.html")


def loggedin(request):
    if request.method == 'POST':
        current_username = request.POST.get('username')
        current_password = request.POST.get('password')
        total_orgs = User.objects.filter(user_type=2).count()
        total_tournaments = Tournament.objects.all().count()
        total_matches = Match.objects.all().count()
        total_teams = Team.objects.all().count()
        my_tournaments = Tournament.objects.filter(T_owner=request.user)
        context = {'total_orgs': total_orgs, 'total_tournaments': total_tournaments,
                   'total_matches': total_matches, 'total_teams': total_teams, 'my_tournaments':my_tournaments
                   }
        if User.objects.filter(username=current_username, password=current_password).exists():
            userobj = User.objects.get(username=current_username, password=current_password)
            login(request, userobj)
            if userobj.is_superuser:
                return render(request, 'examples/adminloggedin.html', context)
            elif userobj.is_authenticated and userobj.user_type==2:
                return render(request, 'examples/dashboard.html', context)
            else: #userobj.is_authenticated and userobj.user_type==3:
                return render(request, 'examples/captaindashboard.html', context)
        else:
            context = {'LoginError': 'Please enter valid username or password'}
            return render(request, 'examples/pages/login.html', context)
    else:
        total_orgs = User.objects.filter(user_type=2).count()
        total_tournaments = Tournament.objects.all().count()
        total_matches = Match.objects.all().count()
        total_teams = Team.objects.all().count()
        my_tournaments = Tournament.objects.filter(T_owner=request.user)
        context = {'total_orgs': total_orgs, 'total_tournaments': total_tournaments,
                   'total_matches': total_matches, 'total_teams': total_teams, 'my_tournaments':my_tournaments
                   }
        if request.user.is_superuser:
            return render(request, 'examples/adminloggedin.html', context)
        elif request.user.user_type==2:
            return render(request, 'examples/dashboard.html', context)
        else:
            return render(request, 'examples/captaindashboard.html', context)


def admindashboard(request):
    if request.method == 'POST':
        current_username = request.POST.get('username')
        current_password = request.POST.get('password')
        total_orgs = User.objects.filter(user_type=2).count()
        total_tournaments = Tournament.objects.all().count()
        total_matches = Match.objects.all().count()
        total_teams = Team.objects.all().count()
        context = {'total_orgs': total_orgs, 'total_tournaments': total_tournaments,
                   'total_matches': total_matches, 'total_teams': total_teams
                   }
        user = authenticate(username=current_username,
                            password=current_password)
        request.session['username'] = user.username
        if user is not None:
            login(request, user)
            return render(request, 'examples/adminloggedin.html', context)
        else:
            context = {'LoginError': 'Please enter valid username or password'}
            return render(request, 'examples/pages/adminlogin.html', context)
    else:
        total_orgs = User.objects.filter(user_type=2).count()
        total_tournaments = Tournament.objects.all().count()
        total_matches = Match.objects.all().count()
        total_teams = Team.objects.all().count()
        context = {'total_orgs': total_orgs, 'total_tournaments': total_tournaments,
                   'total_matches': total_matches, 'total_teams': total_teams
                   }
        return render(request, 'examples/adminloggedin.html', context)


def adminlogin(request):
    return render(request, 'examples/pages/adminlogin.html')


def upComingMatches(request):
    now = timezone.now()
    upComingmatches = Match.objects.filter(Date__gte=now).order_by('Date')
    context = {'upComingmatches':upComingmatches}
    return render(request, 'examples/upmatches.html', context)


def matchResults(request):
    now = timezone.now()
    matchResults = Match.objects.filter(Date__lte=now).order_by('-Date')
    context = {'matchResults':matchResults}
    return render(request, 'examples/matchResults.html', context)


def orgLogin(request):
    if request.method == 'POST':
        current_username = request.POST.get('username')
        current_password = request.POST.get('password')


def allOrganizers(request):
    organizers = User.objects.filter(is_superuser=False)
    context = {'organizers': organizers}
    return render(request, 'examples/organizers.html', context)


def allTournaments(request):
    tournaments = Tournament.objects.all()
    context = {'tournaments': tournaments}
    return render(request, 'examples/tournaments.html', context)


def allTeams(request):
    teams = Team.objects.all()
    context = {'teams': teams}
    return render(request, 'examples/teams.html', context)


def upruntournaments(request):
    now = timezone.now()
    upruntournaments = Tournament.objects.filter(Start_date__gte=now).order_by('Start_date') \
                       | Tournament.objects.filter(End_date__gte=now).order_by('End_date')
    context = {'upruntournaments': upruntournaments}
    return render(request, 'examples/upruntournaments.html', context)


def sendrequest(request, tourid):
    TournamentRequest.objects.create(
            tournament=Tournament.objects.get(id=tourid),
            to_organizer=User.objects.get(username=Tournament.objects.get(id=tourid).T_owner),
            team=Team.objects.get(Captain_name=request.user)
    )
    return redirect('myrequests')


def myrequests(request):
    myrequests = TournamentRequest.objects.filter(team=Team.objects.get(Captain_name=request.user))
    context = {
        'myrequests': myrequests
    }
    return render(request, 'examples/myrequests.html', context)


def latestrequests(request):
    latestrequests = TournamentRequest.objects.filter(status="Initiated", to_organizer=request.user)
    context = {
        'latestrequests': latestrequests
    }
    return render(request, 'examples/latestrequests.html', context)


def approvereq(request, reqid):
    req = TournamentRequest.objects.get(id=reqid)
    req.status = "Accepted"
    req.tournament.teams.add(req.team.id)
    req.tournament.save()
    req.save()
    return redirect('latestrequests')


def rejectreq(request, reqid):
    req = TournamentRequest.objects.get(id=reqid)
    req.status = "Rejected"
    req.tournament.teams.remove(req.team.id)
    req.tournament.save()
    req.save()
    return redirect('latestrequests')


def createTeam(request):
    if request.method == 'POST':
        Team.objects.create(Captain_name=User.objects.get(id=request.user.id),
                            team_player_1=request.POST['teamplayer1'],
                            team_player_2=request.POST['teamplayer2'],
                            team_player_3=request.POST['teamplayer3'],
                            team_player_4=request.POST['teamplayer4'],
                            team_player_5=request.POST['teamplayer5'],
                            team_player_6=request.POST['teamplayer6'],
                            team_player_7=request.POST['teamplayer7'],
                            team_player_8=request.POST['teamplayer8'],
                            team_player_9=request.POST['teamplayer9'],
                            team_player_10=request.POST['teamplayer10']
                            )
        return redirect('loggedin')
    else:
        return render(request, 'examples/createTeam.html')


def allMatches(request):
    matches = Match.objects.all()
    context = {'matches': matches}
    return render(request, 'examples/matches.html', context)


def addOrganizer(request):
    if request.method == 'POST':
        User.objects.create(first_name=request.POST['org_name'],
                            username=request.POST['org_username'],
                            password=request.POST['org_password'],
                            name=request.POST['org_name'],
                            address=request.POST['address'],
                            phone_number=request.POST['phoneno'],
                            email=request.POST['org_email'],
                            user_type=2
                                )
        return redirect('allOrganizers')
    else:
        return render(request, 'examples/addorganizer.html')


def addcaptain(request):
    if request.method == 'POST':
        User.objects.create(first_name=request.POST['name'],
                            username=request.POST['username'],
                            password=request.POST['password'],
                            name=request.POST['name'],
                            address=request.POST['address'],
                            phone_number=request.POST['phoneno'],
                            email=request.POST['cap_email'],
                            user_type=3
                                )
        return redirect('allcaptain')
    else:
        return render(request, 'examples/addcaptain.html')


def allcaptain(request):
    captains = User.objects.filter(user_type=3)
    context = {'captains': captains}
    return render(request, 'examples/captains.html', context)


def GalleryView(request):
    images = Gallery.objects.all()
    context = {'images': images}
    return render(request, 'examples/gallery.html', context)

def addtournament(request):
    if request.method == 'POST':
        Tournament.objects.create(T_name=request.POST['t_name'],
                                  Start_date=request.POST['t_startdate'],
                                  End_date=request.POST['t_enddate'],
                                  no_of_teams=request.POST['t_teams'],
                                  no_of_matches=request.POST['t_matches'],
                                  T_owner=request.user
                                )
        return redirect('Tournaments')
    else:
        return render(request, 'examples/addtournament.html')


def Tournaments(request):
    tournaments = Tournament.objects.all()
    context = {'tournaments': tournaments}
    return render(request, 'examples/tournament.html', context)


def AddTeamInTournament(request):
    if request.method == 'POST':
        tournament = Tournament.objects.get(id=request.POST.get('tournament_id'))
        team = Team.objects.get(id=request.POST.get('team_id'))
        if tournament.teams.filter(id=team.id).exists():
            tournament.teams.remove(team)
            return redirect('teamsintournament', pk=tournament.id)
        else:
            team = request.POST.get('team_id')
            tournament.teams.add(team)
            return redirect('teamsintournament', pk=tournament.id)
    else:
        tournaments = Tournament.objects.filter(T_owner=request.user)
        teams = Team.objects.all()
        context = {'tournaments':tournaments, 'teams':teams }
        return render(request, 'examples/addteamintournament.html',context)


def AddMatchInTournament(request):
    if request.method == 'POST':
        Match.objects.create(
            tournament=Tournament.objects.get(id=request.POST.get('tournament_id')),
            Match_team1=Team.objects.get(id=request.POST.get('team1_id')),
            Match_team2=Team.objects.get(id=request.POST.get('team2_id')),
            Date=request.POST.get('date'),
            Result="Not Played yet")
        return redirect('matchesintournament', pk=request.POST.get('tournament_id'))
    else:
        tournaments = Tournament.objects.filter(T_owner=request.user)
        teams = Team.objects.all()
        context = {'tournaments':tournaments, 'teams':teams }
        return render(request, 'examples/addmatchintour.html',context)


def teamsintournament(request, pk):
    tournament = Tournament.objects.get(id=pk)
    context = {'teams': tournament.teams.all()}
    return render(request, 'examples/teamsintournament.html', context)


def teamsintournamentad(request, pk):
    tournament = Tournament.objects.get(id=pk)
    context = {'teams': tournament.teams.all()}
    return render(request, 'examples/teamsintournamentad.html', context)


def matchesintournament(request, pk):
    tournament = Tournament.objects.get(id=pk)
    context = {'matches': Match.objects.filter(tournament=tournament)}
    return render(request, 'examples/matchesintour.html', context)


def matchesintournamentad(request, pk):
    tournament = Tournament.objects.get(id=pk)
    context = {'matches': Match.objects.filter(tournament=tournament)}
    return render(request, 'examples/matchesintourad.html', context)


def addGallery(request):
    if request.method == 'POST':
        Gallery.objects.create(
            description=request.POST['description'],
            image=request.FILES['image'],
        )
        return redirect('admindashboard')
    else:
        return render(request, 'examples/addgallery.html')


def updatematchresult(request, match):
    if request.method=='POST':
        matchobj = Match.objects.get(id=match)
        matchobj.Result = request.POST.get('result')
        matchobj.save()
        return redirect('matchesintournament', matchobj.tournament.id)
    else:
        matchobj = Match.objects.get(id=match)
        context = {'match': matchobj}
        return render(request, 'examples/updatematchresult.html', context)
























































































































































































































































"""switch (user.user_type):
        total_orgs = User.objects.filter(is_superuser=False).count()
        total_tournaments = Tournament.objects.all().count()
        total_matches = Match.objects.all().count()
        total_teams = Team.objects.all().count()
        context = {'total_orgs': total_orgs, 'total_tournaments': total_tournaments,
                   'total_matches': total_matches, 'total_teams': total_teams
                   }
        if User.objects.filter(username=current_username, password=current_password).exists():
            user = User.objects.get(username=current_username, password=current_password)
            if user.is_organizer == True and user.is_superuser==False:
                user = authenticate(username=current_username,
                                    password=current_password)
                login(request, user)
                #request.session['username'] = user.username
                return render(request, 'examples/dashboard.html', context)
            elif user.is_organizer == False and user.is_superuser == False:
                user = authenticate(username=current_username,
                                    password=current_password)
                login(request, user)
                #request.session['username'] = user.username
                return render(request, 'examples/captaindashboard.html', context)

        else:
            user = authenticate(username=current_username,
                                password=current_password)
            #request.session['username'] = user.username
            #Specific_User = User.objects.get(username=current_username)
            if user is not None:
                login(request, user)
                return render(request, 'examples/adminloggedin.html', context)
            else:
                context = {'LoginError': 'Please enter valid username or password'}
                return render(request, 'examples/pages/login.html', context)
    else:
        if request.user.is_organizer == True and request.user.is_superuser == False:
            total_orgs = User.objects.filter(is_superuser=False).count()
            total_tournaments = Tournament.objects.all().count()
            total_matches = Match.objects.all().count()
            total_teams = Team.objects.all().count()
            context = {'total_orgs': total_orgs, 'total_tournaments': total_tournaments,
                       'total_matches': total_matches, 'total_teams': total_teams
                       }
            return render(request, 'examples/dashboard.html', context)
        elif request.user.is_superuser == False and request.user.is_organizer == False :
            total_orgs = User.objects.filter(is_superuser=False).count()
            total_tournaments = Tournament.objects.all().count()
            total_matches = Match.objects.all().count()
            total_teams = Team.objects.all().count()
            context = {'total_orgs': total_orgs, 'total_tournaments': total_tournaments,
                       'total_matches': total_matches, 'total_teams': total_teams
                       }
            return render(request, 'examples/captaindashboard.html', context)
        else:
            total_orgs = User.objects.filter(is_superuser=False).count()
            total_tournaments = Tournament.objects.all().count()
            total_matches = Match.objects.all().count()
            total_teams = Team.objects.all().count()
            context = {'total_orgs': total_orgs, 'total_tournaments': total_tournaments,
                       'total_matches': total_matches, 'total_teams': total_teams}
            return render(request, 'examples/adminloggedin.html', context)



@csrf_exempt
def loggedin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            template_name = 'user_registration/login.html'
            current_username = request.POST.get('username')
            current_password = request.POST.get('password')
            user = authenticate(username=current_username,
                                password=current_password)
            request.session['username'] = user.username
            Specific_User = User.objects.get(username=current_username)
            if user is not None:
                login(request, user)
                total_orgs = User.objects.filter(is_superuser=False).count()
                total_tournaments = Tournament.objects.all().count()
                total_matches = Match.objects.all().count()
                total_teams = Team.objects.all().count()
                context = {'total_orgs': total_orgs, 'total_tournaments': total_tournaments,
                           'total_matches': total_matches, 'total_teams': total_teams
                           }
                return render(request, 'examples/adminloggedin.html', context)
            else:
                context = {'LoginError': 'Please enter valid username or password'}
                return render(request, 'examples/pages/login.html', context)
        else:
            current_username = request.POST.get('username')
            current_password = request.POST.get('password')
            if current_username != "":
                if User.objects.filter(username=current_username, password=current_password).exists():
                    organizer = User.objects.get(username=current_username)
                    login(request, organizer)
                    request.session['username'] = organizer.username
                    total_orgs = User.objects.filter(is_superuser=False).count()
                    total_tournaments = Tournament.objects.all().count()
                    total_matches = Match.objects.all().count()
                    total_teams = Team.objects.all().count()
                    context = {'total_orgs': total_orgs, 'total_tournaments': total_tournaments,
                               'total_matches': total_matches, 'total_teams': total_teams
                               }
                    return render(request, 'examples/dashboard.html', context)
                else:
                    context = {'LoginError': 'Please enter valid username or password'}
                    return render(request, 'examples/pages/login.html', context)
            else:
                context = {'LoginError': 'Please enter valid username or password'}
                return render(request, 'examples/pages/login.html', context)
    else:
        if request.user.is_superuser:
            total_orgs = User.objects.filter(is_superuser=False).count()
            total_tournaments = Tournament.objects.all().count()
            total_matches = Match.objects.all().count()
            total_teams = Team.objects.all().count()
            context = {'total_orgs': total_orgs, 'total_tournaments': total_tournaments,
                       'total_matches': total_matches, 'total_teams': total_teams
                       }
            return render(request, 'examples/adminloggedin.html', context)
        else:
            total_orgs = User.objects.filter(is_superuser=False).count()
            total_tournaments = Tournament.objects.all().count()
            total_matches = Match.objects.all().count()
            total_teams = Team.objects.all().count()
            context = {'total_orgs': total_orgs, 'total_tournaments': total_tournaments,
                           'total_matches': total_matches, 'total_teams':total_teams
                           }
            return render(request, 'examples/dashboard.html', context)
"""














