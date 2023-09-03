from django.http import HttpResponse
from django.shortcuts import render
import os


def main(request):
    file_path = os.path.join(os.path.dirname(__file__), 'sharedVars.txt')
    sharedVars = open(file_path, "r")
    content = sharedVars.readlines()
    return render(request, 'main.html', {'times': content[0][:-1].strip('][').split(','),
                                         'averages': content[1][:-1].strip('][').split(','),
                                         'min': content[2], 
                                         'max': content[3],
                                         'timeRange': content[4]}
)