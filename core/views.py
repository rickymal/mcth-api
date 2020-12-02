from django.core import serializers
from .models import Judge
from .models import Team
from collections import defaultdict
from .models import Mentor
from .models import Mentoring
from .models import Challenge
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
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Student
from .controllers import AuthenticationController as authentication
import json
import http


@csrf_exempt
def get_listOf_project(request):
    user_model = request.user
    try:
        Judger_model = Judge.objects.get(user_id=user_model)
    except:
        return HttpResponse("O usuário logado não é um jurado, você está tentando burlar o sistema?")
    lof_teams = Team.objects.filter(
        challenge=Judger_model.challenge,).exclude(link_project=None)
    data = lof_teams.values()

    return JsonResponse(list(data), safe=False)


@csrf_exempt
def sendprojectlink(request):
    try:
        student_model = Student.objects.get(user_id=request.user)
    except:
        return HttpResponse("Usuário não é um estudante")
    team_model = student_model.team_id
    team_model.link_project = request.GET.get("link")

    team_model.save()
    return HttpResponse("OK")


@csrf_exempt
def register__old__Team(request):

    data = json.loads(request.body)
    try:
        team_name = data['team_name']
        desafio_id = 0  # O primeiro elemento vai ser um desafio nulo

        Team.objects.create(name=team_name, desafio_id=desafio_id)

        return JsonResponse({
            "status": "OK",
        }, safe=False)
    except:
        return JsonResponse({
            "status": "failed",
        }, safe=False)


    #authentication.registerTeam(team_name = data["team_name"])
state = defaultdict(None)


def get_selections_mentor(request):
    user = request.user
    student = Student.objects.filter(user_id=user)
    student_first = student.first()

    if student_first is None:
        # Checando se o valor é de outro tipo
        isMentor = Mentor.objects.filter(user=user).exists()
        isJudger = Judge.objects.filter(user_id=user).exists()
        if isMentor:
            return HttpResponse("Usuário é um mentor")
        elif isJudger:
            return HttpResponse("Usuário é um jurado")

    if student_first.team_id is None:
        return HttpResponse("O estudante não tem um time")

    mentoring_for_the_team = Mentoring.objects.filter(
        team=student_first.team_id)
    lof_mentoring_for_the_team = list(mentoring_for_the_team.values())

    filter_ = [x['mentor_id'] for x in lof_mentoring_for_the_team]
    for ind, id_ in enumerate(filter_):
        mentor = Mentor.objects.get(id=id_)
        lof_mentoring_for_the_team[ind]["mentor_name"] = mentor.user.first_name + \
            " " + mentor.user.last_name
        lof_mentoring_for_the_team[ind]['data_meeting'] = lof_mentoring_for_the_team[ind]['time_meeting']
        del lof_mentoring_for_the_team[ind]["time_meeting"]

    return JsonResponse(lof_mentoring_for_the_team, safe=False)


@csrf_exempt
def check_user_type(request):
    user_model = request.user
    isStudent = Student.objects.filter(user_id=user_model).exists()
    isMentor = Mentor.objects.filter(user=user_model).exists()
    isJudger = Judge.objects.filter(user_id=user_model).exists()

    if isStudent:
        return HttpResponse("Student")
    elif isMentor:
        return HttpResponse("Mentor")
    elif isJudger:
        return HttpResponse("Judger")


def get_mentor_info(request):
    user_model = request.user
    mentor_model = Mentor.objects.get(user=user_model)
    data = dict()

    data['user'] = {
        'name': user_model.first_name + " " + user_model.last_name
    }

    data['challenge'] = {
        "id": mentor_model.challenge.id,
        "name": mentor_model.challenge.name,
        "enterprise": mentor_model.challenge.empresa_desafiadora,
        "description": mentor_model.challenge.description
    }
    data['id'] = mentor_model.id
    data["kind"] = "Mentor"

    return JsonResponse(data)


@csrf_exempt
def get_user_info(request):
    user = request.user
    data = dict()
    user_category = Student.objects.filter(user_id=user)
    if user_category.exists():
        user_category_model = user_category.first()
        #team_id = Team.objects.filter(id = user_category_model.team_id)
        team_id = user_category_model.team_id

        data['user'] = {
            'name': user_category_model.user_id.first_name + " " + user_category_model.user_id.last_name
        }

        if team_id is not None:
            team_id_model = team_id
            data['team'] = {
                "id": team_id_model.id,
                "challenge": team_id_model.challenge.name,
            }
        else:
            data['team'] = None
    else:
        data['user'] = None
        user_category = Mentor.objects.filter(user=user)
        if user_category.exists():
            return get_mentor_info(request)

    data['kind'] = "Student"
    return JsonResponse(data)


@csrf_exempt
@login_required
def get_teams(request):
    judger = Judge.objects.get(user_id=request.user)
    # Apenas a equipe que contem o desafio do jurado
    teams = Team.objects.filter(challenge_id=judger.challenge_id)
    lofs = list(teams.values())
    challenges_ids = [x['challenge_id'] for x in lofs]
    challenge_list = []
    for x in challenges_ids:
        challenge_unique = Challenge.objects.get(id=x)
        challenge_list.append({
            "id": challenge_unique.id,
            "name": challenge_unique.name,
            "challenger_enterprise": challenge_unique.empresa_desafiadora
        })

    for ind, val in enumerate(lofs):
        lofs[ind]['challenge_id'] = challenge_list[ind]
    temp = lofs
    # Retornando os dados no estilo json
    json_format = JsonResponse(temp, safe=False)
    return json_format


@csrf_exempt
def set_points(request):
    # Receber o juiz
    judger = Judge.objects.get(user_id=request.user)
    # Realizar a inserção da nota
    # Obter o team_id que será enviado pelo sistema
    team_id = request.GET.get("team_id")
    noteJudger = request.GET.get("note")
    team = Team.objects.get(id=int(team_id))
    team.judger_assign = judger
    team.noteJudger = float(noteJudger)
    team.save()

    return HttpResponse("OK")


def select_mentor(request):
    """
    Esta função já partirá do princípio que a lista dos mentores assim como seu identificado já foi enviado para o front-end, logo o front-end apenas irá realizar uma requisição
    dado o id e o nome do mentor junto com a data da mentoria disponível.
    """

    # obtendo os dados
    user = request.user
    mentor_name = request.GET.get('mentor_name')
    mentor_id = request.GET.get('mentor_id')
    meeting_data = request.GET.get('data_meeting')  # str
    student = Student.objects.get(user_id=request.user)
    team = student.team_id

    # Verificar se a mentoria já foi selecionada.
    data_info_formated = parser.parse(meeting_data)
    mentor_model = Mentor.objects.get(id=mentor_id)

    try:
        # Captura todas as mentorias disponíveis do mentor
        mentoring_model = Mentoring.objects.get(
            mentor=mentor_model, team=None, time_meeting=data_info_formated)
    except:
        return HttpResponse("Mentoria não encontrada")
    mentoring_model.team = team
    mentoring_model.save()
    return HttpResponse("Mentoria registrada!")

    # Inserindo a nova mentoria

    newMentoring = Mentoring(mentor=mentor_model,
                             team=team, time_meeting=data_info_formated)

    newMentoring.save()
    return HttpResponse("Meeting made")
    # return JsonResponse(data, safe = False)


@csrf_exempt
def show_disposable_mentors(request):
    """
    Esta função fará a seleção dos mentores disponível para então mostrar para o usuário
    """

    # Precisamos checar se a mentorias selecionada faz parte do setor de interesse do usuário.
    user_model = request.user
    team_model = Student.objects.get(user_id=user_model).team_id

    if team_model is None:
        return HttpResponse("O usuário inserido não possui um time")
    #challenge_id = mentorias_model.mentor_id.challenge_id

    mentorias_model = Mentoring.objects.filter(
        mentor_id__challenge_id=team_model.challenge_id
    )  # filtrando apenas as mentorias que estão livres
    #disposable_meetings = mentorias_model.filter(mentor_id__challenge_id = team_model.challenge_id)
    #values = list(disposable_meetings.objects.values())

    # mentor_info = mentorias_model.
    values = list(mentorias_model.values())
    filter_ = [v['mentor_id'] for v in values]

    for ind, v in enumerate(filter_):
        first_name = Mentor.objects.get(id=v).user.first_name
        last_name = Mentor.objects.get(id=v).user.last_name
        values[ind]["name"] = f"{first_name} {last_name}"
    #response = Mentor.objects.get(id__in = filter_)

    #mentor_filter = Mentor.objects.filter(id__in = filter_).get("user_id")

    # return HttpResponse("OK")
    return JsonResponse(values, safe=False)


def insert_data_meeting(request):
    """
    Função que fará a inserção dos horário de mentoria
    """
    user_model = request.user  # usuário precisa ser um mentor
    meeting_hour = request.GET.get('meeting_hour')
    try:
        mentor_model = Mentor.objects.get(user=user_model)
    except:
        return HttpResponse("Usuário não é um mentor")
    from datetime import datetime
    #datetime_formated = datetime.strptime(date = meeting_hour,format = "%d/%m/%Y %H:%M:%S")
    datetime_formated = parser.parse(meeting_hour)
    time_meeting = datetime_formated
    Mentoring.objects.create(
        mentor=mentor_model, team=None, time_meeting=time_meeting)

    return HttpResponse("WORK!")


@csrf_exempt
def integrate_team(request):
    user_model = request.user
    # Ger Json data {"Team" : ["e-mail1","e-mail2"]}
    data = json.loads(request.body)
    emails = data['email']
    student_model = Student.objects.get(user_id=user_model)
    team_model = student_model.team_id
    lof_status = []

    #anothers_user_models = User.objects.filter(email__in = emails)

    #students_user_models = Student.objects.filter(user_id__in = anothers_user_models)

    #students_user_models_without_team = students_user_models.filter(team_id = None)

    # students_user_models_with_team = students_user_models.exclude(team_id = None) # Finalizar esta parte para retornar as pessoas que não foram inseridas na equipe
    #students_user_models_without_team.update(team_id = team_model)

    for email in emails:
        # try:

        another_user_model = User.objects.get(email=email)

        another_student_model = Student.objects.get(user_id=another_user_model)

        another_student_model.team_id = team_model
        another_student_model.save()

        lof_status.append({
            "name": another_user_model.first_name + " " + another_user_model.last_name,
            "status": "integrated"
        })

    resposta = JsonResponse(lof_status, safe=False)
    #resposta["Access-Control-Allow_Origin"] = "*"
    #resposta["Access-Control-Allow_Methods"] = ['GET','POST','OPTION']
    #resposta["Access-Control-Allow_Headers"] = "*"

    return resposta


@csrf_exempt
def getout_team(request):
    user_model = request.user
    student_model = Student.objects.get(user_id=user_model)

    if student_model.isLeader:
        QueryStudentSet = Student.objects.filter(team_id=student_model.team_id)
        QueryStudentSet.team_id = None
        student_model.team_id.delete()

    student_model.team_id = None
    student_model.save()
    return HttpResponse("OK")


@csrf_exempt
def create_team(request):
    """
    Quando o time é criado, automaticamente este está associado a um desafio
    """

    user_model = request.user
    challenge_name = request.GET.get("challenge")
    try:
        challenge_model = Challenge.objects.get(name=challenge_name)
    except:
        return JsonResponse({
            "status": "challenge canno't be found"
        })

    student_model = Student.objects.get(user_id=user_model)
    team_model = Team.objects.create(challenge_id=challenge_model.id)
    student_model.team_id = team_model
    student_model.save()

    return JsonResponse({
        "status": "OK"
    })


def create_challenge(request):
    # No momento a criação dos desafios seá feita diretamente na página do administrador

    challenge_name = request.GET.get("challenge")
    check_exists = Challenge.objects.filter(name=challenge_name)

    if len(check_exists):
        return JsonResponse({
            'status': 'challenge already exist'
        })
    else:

        challenge_model = Challenge.objects.create(name=challenge_name)
        return JsonResponse({
            "status": "ok"
        })


@csrf_exempt
def loginUser(request):

    username = request.GET.get('username')
    logout(request)
    login_field = login(request, user_authentication,)

    if username is not None:
        return JsonResponse({
            "status": "ok",
        })
    else:
        return JsonResponse({
        })


@csrf_exempt
def register(request):
    username = request.GET.get('username')
    email = request.GET.get('email')
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    category = request.GET.get('category')
    # será o id do desafio pois na tela de login o jurado recebera o id do desafio
    challenge_id = request.GET.get('challenge')
    challenge = challenge_id
    check_user = User.objects.filter(email=email)

    # O usuário já existe?
    if len(check_user):
        # login(request,usuario)
        return JsonResponse({
            'status': 'User already exist',
        }, safe=False)
    else:
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.save()

        if category == 'student':
            student_model = Student.objects.create(
                user_id=user_model, team_id=None, isLeader=False)
        elif category == 'judger':
            challenge = Challenge.objects.get(id=challenge_id)
            jugder_mode = Judge.objects.create(
                user_id=user_model, challenge=challenge)

        elif category == 'mentor':
            # mentor_model = Mentor.objects.create(user = user_model, challenge)
            challenge = Challenge.objects.get(id=challenge_id)
            mentor_model = Mentor.objects.create(
                user=user_model, challenge=challenge)

        return JsonResponse({
            'status': 'created'
        }, safe=False)
