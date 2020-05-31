from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from task_management.models import *
import json
from django.core import serializers
import requests
from django.views.decorators.csrf import csrf_exempt
import time
from time import strftime
# Create your views here.


def login(request):
    return render(request, 'task_management/login.html')


def Create_Users(request):

    if request.method == 'POST':
        name = request.POST['strFullName']
        username = request.POST['LoginID']
        password = request.POST['Password']
        data = {}
        try:
            tbu = tblUser(
                Name=name,
                username=username,
                password=password
            )
            tbu.save()
            data['Status'] = 'Success'
            data['Name'] = tbu.Name
        except:
            data['Status'] = 'Error'
            data['message'] = 'smething went wrong with data base'
    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)


def LoginValidate(request):
    if request.method == 'POST':
        LoginID = request.POST['LoginID']
        Password = request.POST['Password']
        request.session['UserLoginid'] = LoginID
        data = {
            # 'message': serializers.serialize('json', tblUser.objects.filter(username=LoginID))
        }
        try:
            tbu = serializers.serialize(
                'json', tblUser.objects.filter(username=LoginID))
            if len(tbu) > 0:
                data['Status'] = 'Success'
                parsed_json = (json.loads(tbu))
                dataJsn = json.dumps(parsed_json, indent=4, sort_keys=True)
                loaded_json = json.loads(dataJsn)
                if loaded_json[0]["fields"]["password"] == Password:
                    data['message'] = loaded_json[0]["fields"]["Name"]
                else:
                    data['Status'] = 'Error'
                    data['message'] = "Invalid password"
        except:
            data['Status'] = 'Error'
            data['message'] = 'smething went wrong with data base'
    return JsonResponse(data, content_type="application/json", safe=False)
    # return render(request, 'task_management/projectlist.html', {'data': data})


def ProjectList(request):
    return render(request, 'task_management/projectlist.html')


@csrf_exempt
def ProjectInsertUpdate(request):
    if request.method == 'POST':
        ProjectID = request.POST['ProjectID']
        ProjectName = request.POST['ProjectName']
        Duration = request.POST['Duration']
        ProjectManager = request.POST['ProjectManager']
        Description = request.POST['Description']
        data = {}
        try:
            if ProjectID == "0":
                tblp = tblAllProject(
                    ProjectName=ProjectName,
                    Duration=Duration,
                    ProjectManager=ProjectManager,
                    Description=Description
                )
                tblp.save()
            else:
                tblp = tblAllProject.objects.get(pk=int(ProjectID))
                tblp.ProjectName = ProjectName
                tblp.Duration = Duration
                tblp.ProjectManager = ProjectManager
                tblp.Description = Description
                tblp.save()
            data['Status'] = 'Success'
            data['message'] = 'Saved SuccessFully'
        except:
            data['Status'] = 'Error'
            data['message'] = 'smething went wrong with data base'
    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)


@csrf_exempt
def getProjectlist(request):
    if request.method == 'POST':
        data = tblAllProject.objects.all().values('id',
                                                  'ProjectName', 'Duration', 'ProjectManager', 'Description')
        # datajsn = serializers.serialize('json', data)
        # datajsn = json.loads(datajsn)
        datalist = list(data)
    return JsonResponse(datalist, content_type="application/json", safe=False)


@csrf_exempt
def ProjectDelete(request):
    if request.method == 'POST':
        ProjectID = request.POST['ProjectID']
        data = {}
        try:
            tblp = tblAllProject.objects.get(pk=int(ProjectID))
            tblp.delete()
            data['Status'] = 'Success'
            data['message'] = 'Deleted SuccessFully'
        except:
            data['Status'] = 'Error'
            data['message'] = 'smething went wrong with data base'
    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)


@csrf_exempt
def ProjectDetails(request, ProjectID):
    tblp = tblAllProject.objects.get(pk=int(ProjectID))
    return render(request, 'task_management/ProjectDetails.html', {'id': tblp.id, 'ProjectName': tblp.ProjectName, 'Duration': tblp.Duration,
                                                                   'ProjectManager': tblp.ProjectManager,
                                                                   'Description': tblp.Description})


@csrf_exempt
def getTasklist(request):
    if request.method == 'POST':
        data = tblTaskList.objects.all().values('id', 'TaskName', 'ProjectID',
                                                'startDate', 'EndDate', 'Description', 'Assignee')
        # datalist = list(data)
    return JsonResponse(list(data), content_type="application/json", safe=False)


@csrf_exempt
def TaskInsertUpdate(request):
    if request.method == 'POST':
        TaskID = request.POST['TaskID']
        ProjectID = request.POST['ProjectID']
        TaskName = request.POST['TaskName']
        StartDate = request.POST['StartDate']
        EndDate = request.POST['EndDate']
        TaskDescription = request.POST['TaskDescription']
        Assignee = request.POST['Assignee']
        data = {}
        try:
            if TaskID == "0":
                tblTask = tblTaskList(
                    TaskName=TaskName,
                    ProjectID=int(ProjectID),
                    startDate=StartDate,
                    EndDate=EndDate,
                    Description=TaskDescription,
                    Assignee=Assignee
                )
                tblTask.save()
            else:
                tblTask = tblTaskList.objects.get(pk=int(TaskID))
                tblTask.TaskName = TaskName
                tblTask.ProjectID = int(ProjectID)
                tblTask.startDate = StartDate
                tblTask.EndDate = EndDate
                tblTask.Description = TaskDescription
                tblTask.Assignee = Assignee
                tblTask.save()
            data['Status'] = 'Success'
            data['message'] = 'Saved SuccessFully'
        except Exception as e:
            data['Status'] = 'Error'
            data['message'] = type(e)
    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)


@csrf_exempt
def getAssigneeName(request):
    if request.method == 'POST':
        data = tblUser.objects.all().values('id', 'Name')
    return JsonResponse(list(data), content_type="application/json", safe=False)


@csrf_exempt
def TaskDelete(request):
    if request.method == 'POST':
        TaskID = request.POST['TaskID']
        data = {}
        try:
            tblTask = tblTaskList.objects.get(pk=int(TaskID))
            tblTask.delete()
            data['Status'] = 'Success'
            data['message'] = 'Deleted SuccessFully'
        except:
            data['Status'] = 'Error'
            data['message'] = 'smething went wrong with data base'
    return JsonResponse(json.dumps(data), content_type="application/json", safe=False)


@csrf_exempt
def TaskDetails(request, ProjectID, TaskID):
    tblTask = tblTaskList.objects.get(pk=int(TaskID))
    return render(request, 'task_management/TaskList.html', {'id': tblTask.id, 'TaskName': tblTask.TaskName, 'ProjectID': tblTask.ProjectID, 'startDate': tblTask.startDate, 'EndDate': tblTask.EndDate, 'Description': tblTask.Description, 'Assignee': tblTask.Assignee})
