from django.http import HttpResponse
from django.shortcuts import render

sharedVars = open("main/sharedVars.txt", "r")
content = sharedVars.readlines()

def main(request):
    return render(request, 'main.html', {'times': content[0][:-1].strip('][').split(','),
                                         'averages': content[1][:-1].strip('][').split(','),
                                         'min': content[2], 
                                         'max': content[3],
                                         'timeRange': content[4]}
)