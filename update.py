from os         import system, name, path
from urllib     import request, parse, error
from time       import sleep

class update:
    def request(url):
        req = request.Request(url, method='GET')
        resp = request.urlopen(req)
        return resp.read()

    def update_file(url, file):
        with open(file, 'wb') as f:
            f.write(update.request(url))
    

if __name__ == '__main__':
    sleep(1)
    
    update.update_file('https://raw.githubusercontent.com/3d3n-pyc/anysearch-script/v2/main.py', 'main.py')
    update.update_file('https://raw.githubusercontent.com/3d3n-pyc/anysearch-script/v2/VERSION', 'VERSION')
    
    system('python main.py')