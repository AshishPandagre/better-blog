# contains the code which updates the code on pythonanywhere.

import git
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import mechanize
import getpass
import time
import json


def reload():

    with open(os.path.join(BASE_DIR, 'secrets.json')) as secret_file:
        secret = json.load(secret_file)

    username = secret['username']
    password = secret['password']
    domain = 'betterblog.pythonanywhere.com'

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open('https://www.pythonanywhere.com/login/')
    time.sleep(1)

    br.select_form(nr=0)
    br['username'] = username
    br['password'] = password

    br.submit()
    time.sleep(1)
    resp = br.open('https://www.pythonanywhere.com/user/{username}/webapps/{domain}/reload')
    print(resp.read())
    time.sleep(1)

    br.open('https://www.pythonanywhere.com/logout')



@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("better-blog") 
        origin = repo.remotes.origin

        origin.pull()
        reload()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere...")
