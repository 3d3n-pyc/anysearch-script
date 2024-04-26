import os
import shlex
import re
import json
import urllib.request
import urllib.response

version = '1.5'

class colors:
    red = '[38;2;255;0;0m'
    orange = '[38;2;255;165;0m'
    green = '[38;2;100;255;100m'
    black = '[38;2;0;0;0m'
    pink = '[38;2;255;0;255m'
    purple = '[38;2;113;41;255m'
    blue = '[38;2;92;120;255m'
    white = '[38;2;255;255;255m'
    gray = '[38;2;200;200;200m'
    light_gray = '[38;2;150;150;150m'


watermark = '''
  █████╗ ███╗   ██╗██╗   ██╗███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗
 ██╔══██╗████╗  ██║╚██╗ ██╔╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║
 ███████║██╔██╗ ██║ ╚████╔╝ ███████╗█████╗  ███████║██████╔╝██║     ███████║
 ██╔══██║██║╚██╗██║  ╚██╔╝  ╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║
 ██║  ██║██║ ╚████║   ██║   ███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║
 ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝'''

print(watermark
      .replace('█', colors.purple + '█')
      .replace('╗', colors.blue + '╗')
      .replace('║', colors.blue + '║')
      .replace('╝', colors.blue + '╝')
      .replace('═', colors.blue + '═')
      .replace('╔', colors.blue + '╔')
      + '\n' + colors.white)

while True:
    command = shlex.split(input(f'''{colors.purple}┌──({colors.blue}AnySearch{colors.purple})-[{colors.white}~{colors.purple}]
└─{colors.blue}$ {colors.white}'''))
    
    if len(command) == 0:
        print()
        continue
    
    command[0] = command[0].lower()
    
    
    if command[0] == 'help':
        print(f'''\
{colors.gray}Si vous avez besoin d'aide, contactez @3d3n.pyc sur Discord.

 {colors.white}search {colors.light_gray}[value]
 {colors.white}linked {colors.light_gray}[ip]
 {colors.white}lookup {colors.light_gray}[ip]
 {colors.white}key    {colors.light_gray}[key]
 {colors.white}info   {colors.light_gray}
 {colors.white}clear  {colors.light_gray}
''')
        continue
    
    
    if command[0] == 'search':
        if len(command) < 2:
            print('S\'il vous plaît, tapez un nom à rechercher.\n')
            continue
        
        value = command[1].replace(' ', '%20')
        
        if not os.path.exists('KEY'):
            open('KEY', 'w').write('')
        
        key = open('KEY', 'r').read()
        
        if not key:
            print(f'{colors.orange}S\'il vous plaît, mettez votre clé pour rechercher.\n')
            continue
        
        try:
            response:urllib.response = urllib.request.urlopen(f'http://154.51.39.141:19201/api?key={key}&name={value}')
            content = response.read().decode()
        except:
            print(f'{colors.red}Impossible de se connecter à l\'API.\n')
            continue
        
        responseData:dict = json.loads(content)
        
        if responseData.get('error') and responseData.get('error') == 'Rate limit exceeded: Tu fais trop de requêtes !':
            print(f'{colors.red}Vous faites trop de requêtes ! {colors.gray}(5/minute)\n')
        
        elif responseData['code'] == 200:
            ips = responseData["data"]
            for ip in ips:
                response:urllib.response = urllib.request.urlopen(f'http://ip-api.com/json/{ip}?fields=mobile,proxy,hosting')
                content = response.read().decode()
                data:dict = json.loads(content)
                if data == {}:
                    print(f'{colors.red}{ip} {colors.gray}(erreur)')
                elif data['hosting']:
                    print(f'{colors.orange}{ip} {colors.gray}(hébergement)')
                elif data['proxy']:
                    print(f'{colors.orange}{ip} {colors.gray}(proxy)')
                elif data['mobile']:
                    print(f'{colors.orange}{ip} {colors.gray}(mobile)')
                else:
                    print(f'{colors.green}{ip} {colors.gray}')
            print()
        
        elif responseData['code'] == 404:
            print(f'{colors.red}Aucun résultat trouvé.\n')
        
        elif responseData['code'] == 401:
            print(f'{colors.red}Clé API invalide.\n')
        
        else:
            print(f'{colors.red}Une erreur est survenue.\n')
        
        continue
    
    
    if command[0] == 'linked':
        if not os.path.exists('KEY'):
            open('KEY', 'w').write('')
        
        key = open('KEY', 'r').read()
        
        if not key:
            print(f'{colors.orange}S\'il vous plaît, mettez votre clé pour rechercher.\n')
            continue
        
        ip = command[1]
        
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            print(f'{colors.orange}S\'il vous plaît, veuillez entrer une adresse IP valide.\n')
            continue
        
        try:
            response:urllib.response = urllib.request.urlopen(f'http://154.51.39.141:19201/api/ip?key={key}&value={ip}')
            content = response.read().decode()
        except:
            print(f'{colors.red}Impossible de se connecter à l\'API.\n')
            continue
        
        data:dict = json.loads(content)
        
        if data.get('error') and data.get('error') == 'Rate limit exceeded: Tu fais trop de requêtes !':
            print(f'{colors.red}Vous faites trop de requêtes ! {colors.gray}(5/minute)\n')
        
        elif data['code'] == 200:
            names = data['data']
            for name in names:
                print(f'{colors.green}{name} {colors.gray}')
            print()
        
        elif data['code'] == 404:
            print(f'{colors.red}Aucun résultat trouvé.\n')
        
        elif data['code'] == 401:
            print(f'{colors.red}Clé API invalide.\n')
        
        else:
            print(f'{colors.red}Une erreur est survenue.\n')
        
        continue
    
    
    if command[0] == 'lookup':
        if not os.path.exists('KEY'):
            open('KEY', 'w').write('')
        
        key = open('KEY', 'r').read()
        
        if not key:
            print(f'{colors.orange}S\'il vous plaît, mettez votre clé pour rechercher.\n')
            continue
        
        ip = command[1]
        
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            print(f'{colors.orange}S\'il vous plaît, veuillez entrer une adresse IP valide.\n')
            continue
        
        response:urllib.response = urllib.request.urlopen(f'http://ip-api.com/json/{ip}')
        content = response.read().decode()
        data:dict = json.loads(content)
        
        response2:urllib.response = urllib.request.urlopen(f'http://ip-api.com/json/{ip}?fields=mobile,proxy,hosting')
        content2 = response2.read().decode()
        data2:dict = json.loads(content2)
        
        content = ''
        
        if data2 == {}:
            if data2['proxy']:
                content += 'Proxy'
            if data2['hosting']:
                content += 'Hébergement'
            if data2['mobile']:
                content += 'Mobile'
        
        if data['status'] == 'fail':
            print(f'{colors.red}Adresse IP invalide.\n')
        
        elif data['status'] == 'success':
            print(f'''\
{colors.gray}Pays: {colors.light_gray}{data['country']}
{colors.gray}Ville: {colors.light_gray}{data['city']}
{colors.gray}Code Postal: {colors.light_gray}{data['zip']}

{colors.gray}Fournisseur: {colors.light_gray}{data['isp']}
{colors.gray}Organisation: {colors.light_gray}{data['org']}

{colors.gray}VPN: {colors.light_gray}{data2['proxy']}
{colors.gray}Hébergement: {colors.light_gray}{data2['hosting']}
{colors.gray}Mobile: {colors.light_gray}{data2['mobile']}
''')
        
        continue
        
    
    if command[0] == 'key':
        if len(command) < 2:
            print(f'{colors.orange}S\'il vous plaît, veuillez entrer une clé.\n')
            continue
        
        key = command[1]
        
        open('KEY', 'w').write(key)
        
        print(f'{colors.green}Clé API enregistrée.\n')
        continue
    
    
    if command[0] == 'info':
        try:
            response:urllib.response = urllib.request.urlopen(f'http://154.51.39.141:19201/info')
            content = response.read().decode()
        except:
            print(f'{colors.red}Impossible de se connecter à l\'API.\n')
            continue
        
        data:dict = json.loads(content)['data']

        print(f'''\
{colors.gray}Version: {colors.light_gray}{version}
{colors.gray}API Version: {colors.light_gray}{data['version']}
{colors.gray}Auteur: {colors.light_gray}@3d3n.pyc

{colors.gray}Elements dans la base de données: {colors.light_gray}{data['count']}
''')
        continue
    
    if command[0] == 'clear':
        os.system('cls')
        print(watermark
              .replace('█', colors.purple + '█')
              .replace('╗', colors.blue + '╗')
              .replace('║', colors.blue + '║')
              .replace('╝', colors.blue + '╝')
              .replace('═', colors.blue + '═')
              .replace('╔', colors.blue + '╔')
              + '\n' + colors.white)
        continue
        
    
    print(f"{colors.white}Command '{command[0]}' not found.\n")
