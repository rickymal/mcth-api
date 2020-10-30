from django.shortcuts import render

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

import logging

from dateutil import parser


# Create your views here.

from django.contrib.auth.models import User


from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .models import Student
from .controllers import AuthenticationController as authentication
import json

import http

@csrf_exempt
def register__old__Team(request):
    print("[REGISTER] make registration of a team")
    data = json.loads(request.body)
    try:
        team_name = data['team_name']
        desafio_id = 0 # O primeiro elemento vai ser um desafio nulo

        Team.objects.create(name = team_name,desafio_id = desafio_id)

        return JsonResponse({
            "status" : "OK",
        },safe = False)
    except:
        return JsonResponse({
            "status" : "failed",
        }, safe = False)

    #authentication.registerTeam(team_name = data["team_name"])

from .models import Team
from .models import Challenge
from .models import Mentoring
from .models import Mentor

from collections import defaultdict

state = defaultdict(None)

def unselect_mentor(request):
    pass

from .models import Judge




def createJudger(request):
    pass

from django.core import serializers

@csrf_exempt
@login_required
def get_teams(request):
    judger = Judge.objects.get(user_id = request.user)
    teams = Team.objects.filter(challenge_id = judger.challenge_id) # Apenas a equipe que contem o desafio do jurado



    lofs = list(teams.values())
    challenges_ids = [x['challenge_id'] for x in lofs]

    challenge_list = []
    for x in challenges_ids:
        challenge_unique = Challenge.objects.get(id = x)
        challenge_list.append({
            "id" : challenge_unique.id,
            "name" : challenge_unique.name,
            "challenger_enterprise" : challenge_unique.empresa_desafiadora
        })


    for ind,val in enumerate(lofs):
        lofs[ind]['challenge_id'] = challenge_list[ind]



    temp = lofs
    print(temp)
    json_format = JsonResponse(temp,safe = False ) # Retornando os dados no estilo json
    print(json_format)
    
    
    
    
    return json_format
    pass

@csrf_exempt
def set_points(request):
    # Receber o juiz
    judger = Judge.objects.get(user_id = request.user)

    # Realizar a inserção da nota 
    team_id = request.GET.get("team_id") # Obter o team_id que será enviado pelo sistema
    print("ID DO SISTEMA",team_id)
    team = Team.objects.get(id = int(team_id))


    return HttpResponse("OK")
    pass


def select_mentor(request):
    """
    Esta função já partirá do princípio que a lista dos mentores assim como seu identificado já foi enviado para o front-end, logo o front-end apenas irá realizar uma requisição
    dado o id e o nome do mentor junto com a data da mentoria disponível.
    """

    # obtendo os dados
    user = request.user
    mentor_name = request.GET.get('name')
    mentor_id = request.GET.get('mentor_id')
    meeting_data = request.GET.get('data_meeting') # str
    
    student = Student.objects.get(user_id = request.user)
    team = student.team_id
    
    
    

    # Verificar se a mentoria já foi selecionada.
    
    data_info_formated = parser.parse(meeting_data)
    mentor_model = Mentor.objects.get(id = mentor_id)
    print(type(mentor_model))
    try:
        mentoring_model = Mentoring.objects.get(mentor = mentor_model,team = None, time_meeting = data_info_formated) # Captura todas as mentorias disponíveis do mentor
    except:
        return HttpResponse("Mentoria não encontrada")
    print("DASDHJH".center(80,'-'))
    print(mentoring_model)

    

    

    
    mentoring_model.team = team
    mentoring_model.save()
    return HttpResponse("Mentoria registrada!")

    # Inserindo a nova mentoria


    newMentoring = Mentoring(mentor = mentor_model,
     team = team, time_meeting = data_info_formated)
    


    newMentoring.save()


    return HttpResponse("Meeting made")
    #return JsonResponse(data, safe = False)

    

    
    
    pass

@csrf_exempt
def show_disposable_mentors(request):
    """
    Esta função fará a seleção dos mentores disponível para então mostrar para o usuário
    """

    user_model = request.user # Precisamos checar se a mentorias selecionada faz parte do setor de interesse do usuário.
    team_model = Student.objects.get(user_id = user_model).team_id

    
    if team_model is None:
        return HttpResponse("O usuário inserido não possui um time")
    #challenge_id = mentorias_model.mentor_id.challenge_id
    
    mentorias_model = Mentoring.objects.filter(
    mentor_id__challenge_id = team_model.challenge_id
    ) #filtrando apenas as mentorias que estão livres
    #disposable_meetings = mentorias_model.filter(mentor_id__challenge_id = team_model.challenge_id)
    #values = list(disposable_meetings.objects.values())

    #mentor_info = mentorias_model.
    values = list(mentorias_model.values())
    
    filter_ = [v['mentor_id'] for v in values]

    for ind,v in enumerate(filter_):
        first_name = Mentor.objects.get(id = v).user.first_name
        last_name = Mentor.objects.get(id = v).user.last_name
        print(first_name)
        print(last_name)
        values[ind]["name"] = f"{first_name} {last_name}"
    #response = Mentor.objects.get(id__in = filter_)
    


    #mentor_filter = Mentor.objects.filter(id__in = filter_).get("user_id")

    #print(list(mentor_filter.values()))
    print(values)
    #print(team_model.objects.all())

    
    #return HttpResponse("OK")
    return JsonResponse(values,safe = False)

    pass


def insert_data_meeting(request):
    """
    Função que fará a inserção dos horário de mentoria
    """

    user_model = request.user # usuário precisa ser um mentor
    meeting_hour = request.GET.get('meeting_hour')
    try:
        mentor_model = Mentor.objects.get(user = user_model)
    except:
        return HttpResponse("Usuário não é um mentor")

    from datetime import datetime

    #datetime_formated = datetime.strptime(date = meeting_hour,format = "%d/%m/%Y %H:%M:%S")
    
    datetime_formated = parser.parse(meeting_hour)
    print(f"Datetime formated : {datetime_formated}")
    
    time_meeting = datetime_formated


    Mentoring.objects.create(mentor = mentor_model,team = None,time_meeting= time_meeting)

    return HttpResponse("WORK!")

@csrf_exempt
def integrate_team(request):
    user_model = request.user
    data = json.loads(request.body) # Ger Json data {"Team" : ["e-mail1","e-mail2"]}
    emails = data['email']
    student_model = Student.objects.get(user_id = user_model)
    team_model = student_model.team_id
    lof_status = []

    print(user_model)
    print(data)
    print(emails)

    anothers_user_models = User.objects.filter(email__in = emails)
    students_user_models = Student.objects.filter(user_id__in = anothers_user_models)
    students_user_models_without_team = students_user_models.filter(team_id = None)
    #students_user_models_with_team = students_user_models.exclude(team_id = None) # Finalizar esta parte para retornar as pessoas que não foram inseridas na equipe
    students_user_models_without_team.update(team_id = team_model)
    """
    for email in emails:
        #try:
        
        another_user_model = User.objects.get(email = email)
        print("[integration] another user found")

        #another_user_model.update(team_id = team_model)
        another_user_model.
        another_user_model.save()
        print("[integration] another user sucessfull loaded to the team")

        lof_status.append({
            "name" : another_user_model.first_name + " " +another_user_model.last_name,
            "status" : "integrated"
        })

        print("Next... \r\n")

        except:
            print("[integration] an error ocurr when adding a person to your team")
            lof_status.append({
                "name" : another_user_model.first_name + " " +another_user_model.last_name,
                "status" : "not integrated"
            })
    """

            
    return JsonResponse("OK", safe = False)
        




@csrf_exempt
def getout_team(request):
    user_model = request.user
    student_model = Student.objects.get(user_id = user_model)
    

    if student_model.isLeader:

        QueryStudentSet = Student.objects.filter(team_id = student_model.team_id)
        QueryStudentSet.team_id = None
        student_model.team_id.delete()

    student_model.team_id = None
    

    student_model.save()
    


    return HttpResponse("OK")

@csrf_exempt
@login_required
def create_team(request):
    """
    Quando o time é criado, automaticamente este está associado a um desafio
    """
    print('debug'.center(80,'-'))
    print("[team creation] creating a new team")
    user_model = request.user
    print(user_model)
    challenge_name = request.GET.get("challenge")
    try:
        challenge_model = Challenge.objects.get(name = challenge_name)
    except:
        return JsonResponse({
            "status" : "challenge canno't be found"
        })
    
    student_model = Student.objects.get(user_id = user_model)
    print("Student found")

    team_model = Team.objects.create(challenge_id = challenge_model)
    print("Team created")

    #student_model.update(equipe_id = team_model) update method don't work when u "get" de model, only when you "Filter" the model do get a QuerySet objects
    student_model.team_id = team_model
    student_model.save()

    print("Student updated")
    student_model.save()
    
    return  JsonResponse({
        "status" : "OK"
    })





def create_challenge(request):
    # No momento a criação dos desafios seá feita diretamente na página do administrador

    challenge_name = request.GET.get("challenge")
    check_exists = Challenge.objects.filter(name = challenge_name)

    if len(check_exists):
        return JsonResponse({
            'status' : 'challenge already exist'
        })
    else:

        challenge_model = Challenge.objects.create(name = challenge_name)
        return JsonResponse({
            "status" : "ok"
        })
    

@csrf_exempt
def loginUser(request):
    print("ASHJDASDHI".center(80,'-'))
    username = request.GET.get('username')
    password = request.GET.get('password')

    print(f'username : {username} and password : {password}')
    
    logout(request)
    
    user_authentication = authenticate(username = username, password = password,)
    #print(f"User {username} authenticated")
    login_field = login(request, user_authentication)
    #print(f"User {username} logged")

    if username is not None:                
        return JsonResponse({
            "status" : "ok",
        })
    else:
        return JsonResponse({
            "status" : "user didn't not found, maybe user or password is incorrect"
        })
    
    

@csrf_exempt
def register(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    email = request.GET.get('email')
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')

    category = request.GET.get('category')
    challenge_id = request.GET.get('challenge') # será o id do desafio pois na tela de login o jurado recebera o id do desafio
    challenge = challenge_id

    #usuario = authenticate(username = username, password = password,)
    check_user = User.objects.filter(email = email)
    print(check_user)
    print(len(check_user))
    
    # O usuário já existe?
    if len(check_user):
        #login(request,usuario)
        return JsonResponse({
            'status' : 'User already exist',
        }, safe = False)

    else:
        user_model = User.objects.create_user(username,email,password)
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.save()


        if category == 'student':
            student_model = Student.objects.create(user_id = user_model, team_id = None, isLeader = False)
        elif category == 'judger':
            challenge = Challenge.objects.get(id = challenge_id)
            jugder_mode = Judge.objects.create(user_id = user_model, challenge = challenge)
            pass
        elif category == 'mentor':
            #mentor_model = Mentor.objects.create(user = user_model, challenge)
            challenge = Challenge.objects.get(id = challenge_id)
            mentor_model = Mentor.objects.create(user = user_model, challenge = challenge)
            
        
        return JsonResponse({
            'status' : 'created'
        }, safe = False)
