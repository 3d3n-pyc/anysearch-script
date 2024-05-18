from traceback  import format_exc
from os         import system, name, path
from urllib     import request, parse, error
from ctypes     import windll
from json       import loads, dump
from datetime   import datetime


class colors:
    light_red = '\033[91m'
    light_green = '\033[92m'
    light_gray = '\033[37m'
    tan = '\033[93m'
    red = '\033[31m'
    orange = '\033[33m'
    white = '\033[97m'
    reset = '\033[0m'


class requests:
    def get(url, params:dict = {}):
        params = parse.urlencode(params)
        req = request.Request(f'{url}?{params}' if params else url, method='GET')
        resp = request.urlopen(req)
        return loads( resp.read().decode() )
    
    def post(url, data:dict = {}):
        data = parse.urlencode(data).encode()
        req = request.Request(url, data=data, method='POST')
        resp = request.urlopen(req)
        return loads( resp.read().decode() )
    
    def delete(url, data:dict = {}):
        data = parse.urlencode(data).encode()
        req = request.Request(url, data=data, method='DELETE')
        resp = request.urlopen(req)
        return loads( resp.read().decode() )



version = open('VERSION', 'r').read() if path.exists('VERSION') else 'Aucune version'

if name == 'nt':
    windll.kernel32.SetConsoleTitleW(f'AnySearch v{version} - @3D3N')


class utilsClass:
    def __init__(self):
        self.space = ' '*10
        self.host = 'http://154.51.39.141:19201'
    
    def update(self):
        system('start update.py')
        exit()
    
    def get_config(self):
        if not path.exists('config.json'):
            default = {
                'spy': {
                    'sent_messages': True,
                    'deleted_messages': True,
                    'edited_messages': True,
                    'member_joins': True,
                    'member_leaves': True,
                    'member_bans': True,
                    'member_unbans': True,
                    'user_updates': True,
                    'voice_state_updates': True
                }
            }
            dump(default, open('config.json', 'w'), indent=4)
            return default
        
        return loads( open('config.json', 'r').read() )
    
    def get_key(self):
        if not path.exists('KEY'):
            open('KEY', 'w').write('')
            return 'none'
        
        return open('KEY', 'r').read()
    
    def get_info(self):
        response = requests.get(f'{self.host}/info')
        return response
    
    def get_cooldown(self):
        response = requests.get(f'{self.host}/api/cooldown', params={'key': self.get_key()})
        
        if response['data']['status'] == '👑':
            return {'status': '👑', 'status_name': 'King', 'amount': response['data']['amount'], 'maximum': 3600, 'lastReset': response['data']['lastReset']}
        
        if response['data']['status'] == '🌀':
            return {'status': '🌀', 'status_name': 'Cyclone', 'amount': response['data']['amount'], 'maximum': 720, 'lastReset': response['data']['lastReset']}
        
        if response['data']['status'] == '💠':
            return {'status': '💠', 'status_name': 'Diamond', 'amount': response['data']['amount'], 'maximum': 120, 'lastReset': response['data']['lastReset']}
        
        if response['data']['status'] == '💜':
            return {'status': '💜', 'status_name': 'Booster', 'amount': response['data']['amount'], 'maximum': 60, 'lastReset': response['data']['lastReset']}
        
        return {'status': '😎', 'status_name': 'Free', 'amount': response['data']['amount'], 'maximum': 5, 'lastReset': response['data']['lastReset']}

    def is_key_valid(self, key):
        response = requests.get(f'{self.host}/api/key', params={'key': key})
        return response
    
    def search_name(self, value):
        response = requests.get(f'{self.host}/api/name', params={'key': self.get_key(), 'value': value})
        return response
    
    def search_ip(self, value):
        response = requests.get(f'{self.host}/api/ip', params={'key': self.get_key(), 'value': value})
        return response
    
    def is_ip_vpn(self, ip):
        response = requests.get(f'http://ip-api.com/json/{ip}?fields=mobile,proxy,hosting')
        return response
    
    def lookup_ip(self, ip):
        response = requests.get(f'http://ip-api.com/json/{ip}')
        response2 = requests.get(f'http://ip-api.com/json/{ip}?fields=mobile,proxy,hosting')
        
        response['proxy'] = response2['proxy']
        response['hosting'] = response2['hosting']
        response['mobile'] = response2['mobile']
        
        return response

    def spy_user(self, user):
        response = requests.get(f'{self.host}/spy/user', params={'key': self.get_key(), 'user': user})
        return response
    
    def spy_channel(self, channel):
        response = requests.get(f'{self.host}/spy/channel', params={'key': self.get_key(), 'channel': channel})
        return response
    
    def spy_guild(self, guild):
        response = requests.get(f'{self.host}/spy/guild', params={'key': self.get_key(), 'guild': guild})
        return response
    
    def spy_message(self, message):
        response = requests.get(f'{self.host}/spy/message', params={'key': self.get_key(), 'value': message})
        return response
    
    def get_guild_list(self):
        response = requests.get(f'{self.host}/spy/list')
        return response

    def get_user_data(self, user_id: int) -> dict:
        response = requests.get(f'{self.host}/data/user', params={'user': user_id})
        return response
    
    def lookup_discord(self, user_id: int) -> dict:
        response = requests.get(f'https://discordlookup.mesavirep.xyz/v1/user/{user_id}')
        return response
    
    def get_guild(self, channel_id: int) -> str:
        response = self.get_guild_list()
        for guild in response['data']:
            for channel in guild['channels']:
                if channel['id'] == channel_id:
                    return guild['name']

        return None
    
    def get_guild_name(self, guild_id: int) -> str:
        response = self.get_guild_list()
        for guild in response['data']:
            if guild['id'] == guild_id:
                return guild['name']

        return None

utils = utilsClass()

api_version = utils.get_info()['data']['version']

class ui:
    def __init__(self):
        self.space = ' '*10

    def base(self):
        system('cls' if name == 'nt' else 'clear')
        
        print('\n' +
            f'\n{self.space}{colors.light_red}┏┓    ┏┓        ┓   ┏┳┓    ┓{colors.reset}',
            f'\n{self.space}{colors.light_red}┣┫┏┓┓┏┗┓┏┓┏┓┏┓┏╸┣┓   ┃ ┏┓┏┓┃{colors.reset}',
            f'\n{self.space}{colors.light_red}┛┗┛┗┗┫┗┛┗ ┗┻┛ ┗━┛┗   ┻ ┗┛┗┛┗{colors.reset}',
            f'\n{self.space}{colors.light_red}     ┛                      {colors.reset}',
            f'\n',
            f'\n{self.space}{colors.light_red}⚡{colors.white}Développé par {colors.light_red}@3d3n.pyc{colors.reset}',
            f'\n{self.space}{colors.light_red}⚡{colors.white}Version: {colors.light_red}{version}{colors.reset}',
            f'\n{self.space}{colors.light_red}⚡{colors.white}GitHub: {colors.light_red}https://github.com/3d3n-pyc{colors.reset}'
        )
        
        if api_version != version:
            print(f'\n{self.space}{colors.light_red}• {colors.white}Une nouvelle version du tool est disponible ({colors.light_red}{api_version}{colors.white}){colors.reset}')
            response = input('\n' + self.space + colors.light_red + '• ' + colors.white + 'Voulez-vous mettre à jour le tool ? (o/n) ' + colors.reset)
            if response.lower() == 'o':
                utils.update()
    
    def menu(self):
        self.base()
        return input(
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}01{colors.white}) Recherche à partir d\'un pseudo'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}02{colors.white}) Recherche à partir d\'une IP'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}03{colors.white}) Lookup une IP'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}04{colors.white}) Logs d\'un utilisateur Discord'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}05{colors.white}) Logs d\'un salon Discord'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}06{colors.white}) Logs d\'un serveur Discord'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}07{colors.white}) Logs des messages Discord contenant ...'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}08{colors.white}) Configuration des logs'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}09{colors.white}) Changer la clé API'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}10{colors.white}) Informations par rapport à l\'API'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}11{colors.white}) Fermer le script'
            f'\n{self.space}{colors.light_red}└─ • {colors.white}'
        )
    
    
    def search(self):
        self.base()
        
        value = input(f'\n{self.space}{colors.light_red}• {colors.white}Entrez le pseudo à rechercher: {colors.light_red}')
        
        if not value:
            return
        
        print(f'\n{self.space}{colors.white}( {colors.tan}⚡{colors.white}) {colors.tan}Recherche du pseudo{colors.reset}')
        try:
            response = utils.search_name(value.replace(' ', '%20'))
        except error.HTTPError:
            cooldown = utils.get_cooldown()
            if cooldown['amount'] >= cooldown['maximum']:
                response = {'code': 429}
            else:
                response = {'code': 404}
        
        if response['code'] == 404:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Pseudo introuvable{colors.reset}')
        elif response['code'] == 429:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Vous faites trop de requêtes !{colors.reset}')
        else:
            print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) {colors.light_green}Pseudo trouvé !{colors.reset}')
            for database in response['data']:
                print(f'\n{self.space}{colors.light_red}• {colors.white}{database} {colors.white}')
                for i, ip in enumerate(response['data'][database]):
                    try: response2 = utils.is_ip_vpn(ip)
                    except: response2 = {'hosting': False, 'proxy': False, 'mobile': False}
                    if response2['hosting'] or response2['proxy'] or response2['mobile']:
                        warn = 'hébergement' if response2['hosting'] else 'proxy' if response2['proxy'] else 'mobile'
                        print(f"{self.space}{colors.light_red}{'┆' if i != len(response['data'][database]) - 1 else '╰'} {colors.orange}{ip} {colors.white}({colors.orange}{warn}{colors.white})")
                    else:
                        print(f"{self.space}{colors.light_red}{'┆' if i != len(response['data'][database]) - 1 else '╰'} {colors.white}{ip}{colors.white}")
        
        input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
    
    
    def linked(self):
        self.base()
        
        value = input(f'\n{self.space}{colors.light_red}• {colors.white}Entrez l\'IP à rechercher: {colors.light_red}')
        
        if not value:
            return
        
        print(f'\n{self.space}{colors.white}( {colors.tan}⚡{colors.white}) {colors.tan}Recherche de l\'IP{colors.reset}')
        try:
            response = utils.search_ip(value)
        except error.HTTPError:
            cooldown = utils.get_cooldown()
            if cooldown['amount'] >= cooldown['maximum']:
                response = {'code': 429}
            else:
                response = {'code': 404}
            
        if response['code'] == 404:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}IP introuvable{colors.reset}')
        elif response['code'] == 429:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Vous faites trop de requêtes !{colors.reset}')
        else:
            print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) {colors.light_green}IP trouvée !{colors.reset} ')
            for database in response['data']:
                print(f'\n{self.space}{colors.light_red}• {colors.white}{database} {colors.white}')
                for i, name in enumerate(response['data'][database]):
                    print(f"{self.space}{colors.light_red}{'┆' if i != len(response['data'][database]) - 1 else '╰'} {colors.white}{name}{colors.white}")
        
        input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
    
    
    def lookup(self):
        self.base()
        
        value = input(f'\n{self.space}{colors.light_red}• {colors.white}Entrez l\'IP à lookup: {colors.light_red}')
        
        if not value:
            return
        
        print(f'\n{self.space}{colors.white}( {colors.tan}⚡{colors.white}) {colors.tan}Lookup de l\'IP en cours...{colors.reset}')
        
        try:
            response = utils.lookup_ip(value)
        except error.HTTPError:
            response = {'status': 'fail'}
        
        if response['status'] == 'fail':
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}IP introuvable{colors.reset}')
        else:
            print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) {colors.light_green}IP trouvée !{colors.reset}')
            print(
                f'\n{self.space}{colors.light_red}• {colors.white}Pays         -> {colors.light_red}{response["country"]}'
                f'\n{self.space}{colors.light_red}• {colors.white}Ville        -> {colors.light_red}{response["city"]}'
                f'\n{self.space}{colors.light_red}• {colors.white}Code Postal  -> {colors.light_red}{response["zip"]}'
                f'\n'
                f'\n{self.space}{colors.light_red}• {colors.white}Fournisseur  -> {colors.light_red}{response["isp"]}'
                f'\n{self.space}{colors.light_red}• {colors.white}Organisation -> {colors.light_red}{response["org"]}'
                f'\n'
                f'\n{self.space}{colors.light_red}• {colors.white}Proxy        -> {colors.light_red}{response["proxy"]}'
                f'\n{self.space}{colors.light_red}• {colors.white}Hébergement  -> {colors.light_red}{response["hosting"]}'
                f'\n{self.space}{colors.light_red}• {colors.white}Mobile       -> {colors.light_red}{response["mobile"]}'
            )
        
        input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
    
    
    def logs_user(self):
        self.base()
        
        value = input(f'\n{self.space}{colors.light_red}• {colors.white}Entrez l\'ID Discord à rechercher: {colors.light_red}')
        
        if not value:
            return
        
        try:
            int(value)
        except ValueError:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Nombre invalide{colors.reset}')
            input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
            return
        
        print(f'\n{self.space}{colors.white}( {colors.tan}⚡{colors.white}) {colors.tan}Recherche de l\'ID Discord{colors.reset}')
        
        try:
            result = utils.spy_user(value)
        except error.HTTPError:
            cooldown = utils.get_cooldown()
            if cooldown['amount'] >= cooldown['maximum']:
                result = {'code': 429}
            else:
                result = {'code': 404}
        
        if result['code'] == 404:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}ID Discord introuvable{colors.reset}')
        elif result['code'] == 429:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Vous faites trop de requêtes !{colors.reset}')
        else:
            contents:list = result['data']['sent_messages'] + result['data']['deleted_messages'] + result['data']['edited_messages'] + result['data']['member_joins'] + result['data']['member_leaves'] + result['data']['member_bans'] + result['data']['member_unbans'] + result['data']['user_updates'] + result['data']['voice_state_updates']
            
            if len(contents) == 0:
                print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Aucun contenu trouvé{colors.reset}')
                input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
                return
            
            print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) {colors.light_green}ID Discord trouvé !{colors.reset}')
            
            response = utils.lookup_discord(value)
            created_at = response['created_at']
            date = datetime.strptime(created_at.replace('T', ' ').replace('+00:00', '').split('.')[0], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M:%S')
            
            print(
                f'\n{self.space}{colors.light_red}• {colors.white}Pseudo   -> {colors.light_red}{response["raw"]["username"] if response["raw"]["discriminator"] == "0" else f"{response["raw"]["username"]}#{response["raw"]["discriminator"]}"}'
                f'\n{self.space}{colors.light_red}• {colors.white}Créé le  -> {colors.light_red}{date}'
                f'\n{self.space}{colors.light_red}• {colors.white}Clan     -> {colors.light_red}{response["raw"]["clan"] if response["raw"]["clan"] != None else "Aucun"}'
            )
            
            for message_type in ['sent_messages', 'deleted_messages', 'edited_messages', 'member_joins', 'member_leaves', 'member_bans', 'member_unbans', 'user_updates', 'voice_state_updates']:
                for item in result['data'][message_type]:
                    item['type'] = message_type

            
            if len(contents) == 0:
                print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Aucun contenu trouvé{colors.reset}')
                input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
                return
            
            for content in contents:
                content['timestamp'] = datetime.strptime(content['timestamp'].replace('T', ' ').replace('+00:00', '').split('.')[0], '%Y-%m-%d %H:%M:%S')
            contents.sort(key=lambda x: x['timestamp'], reverse=True)
            
            for content in contents:
                timestamp = content['timestamp'].strftime('%d/%m/%Y %H:%M:%S')
                config = utils.get_config()
                
                if content['type'] == 'sent_messages' and config['spy']['sent_messages']:
                    event = 'Message envoyé'
                    channel = content['channel_id']
                    guild = utils.get_guild(channel)
                    guild_name = utils.get_guild_name(guild)
                    message = content['content'].split('\n')
                    
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} dans {colors.light_red}#{channel} {colors.white}({colors.light_red}{guild}{colors.white}) le {colors.light_red}{timestamp}{colors.white}')
                    
                    for i, line in enumerate(message):
                        if i != len(message) - 1:
                            print(f'{self.space}{colors.light_red}┆ {colors.white}{line}')
                        else:
                            print(f'{self.space}{colors.light_red}╰ {colors.white}{line}')
                
                elif content['type'] == 'deleted_messages' and config['spy']['deleted_messages']:
                    event = 'Message supprimé'
                    channel = content['channel_id']
                    guild = utils.get_guild(channel)
                    message = content['content'].split('\n')
                    
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} dans {colors.light_red}#{channel} {colors.white}({colors.light_red}{guild}{colors.white}) le {colors.light_red}{timestamp}{colors.white}')
                    
                    for i, line in enumerate(message):
                        if i != len(message) - 1:
                            print(f'{self.space}{colors.light_red}┆ {colors.white}{line}')
                        else:
                            print(f'{self.space}{colors.light_red}╰ {colors.white}{line}')
                
                elif content['type'] == 'edited_messages' and config['spy']['edited_messages']:
                    if content['before_content'] == content['after_content']:
                        continue
                    
                    event = 'Message édité'
                    channel = content['channel_id']
                    guild = utils.get_guild(channel)
                    before = content['before_content'].split('\n')
                    after = content['after_content'].split('\n')
                    
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} dans {colors.light_red}#{channel} {colors.white}({colors.light_red}{guild}{colors.white}) le {colors.light_red}{timestamp}{colors.white}')
                    
                    for line in before:
                        print(f'{self.space}{colors.light_red}┆ {colors.white}{line}')
                    
                    print(f'{self.space}{colors.light_red}├{"─"*3}')
                    
                    for i, line in enumerate(after):
                        if i != len(after) - 1:
                            print(f'{self.space}{colors.light_red}┆ {colors.white}{line}')
                        else:
                            print(f'{self.space}{colors.light_red}╰ {colors.white}{line}')
                
                elif content['type'] == 'member_joins' and config['spy']['member_joins']:
                    event = 'Serveur rejoint'
                    guild = utils.get_guild_name(content['guild_id'])
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} nommé {colors.light_red}{guild}{colors.white} le {colors.light_red}{timestamp}{colors.white}')
                
                elif content['type'] == 'member_leaves' and config['spy']['member_leaves']:
                    event = 'Serveur quitté'
                    guild = utils.get_guild_name(content['guild_id'])
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} nommé {colors.light_red}{guild}{colors.white} le {colors.light_red}{timestamp}{colors.white}')
                
                elif content['type'] == 'member_bans' and config['spy']['member_bans']:
                    event = 'Membre banni'
                    guild = utils.get_guild_name(content['guild_id'])
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} sur {colors.light_red}{guild}{colors.white} le {colors.light_red}{timestamp}{colors.white}')
                
                elif content['type'] == 'member_unbans' and config['spy']['member_unbans']:
                    event = 'Membre débanni'
                    guild = utils.get_guild_name(content['guild_id'])
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} sur {colors.light_red}{guild}{colors.white} le {colors.light_red}{timestamp}{colors.white}')
                
                elif content['type'] == 'user_updates' and config['spy']['user_updates']:
                    before = content['before_data']
                    after = content['after_data']
                    
                    if before['name'] != after['name']:
                        print(f'\n{self.space}{colors.light_red}• {colors.white}Nom changé de {colors.light_red}{before["name"]} {colors.white}à {colors.light_red}{after["name"]}{colors.white} le {colors.light_red}{timestamp}{colors.white}')
                    
                    elif before['display_name'] != after['display_name']:
                        print(f'\n{self.space}{colors.light_red}• {colors.white}Discriminateur changé de {colors.light_red}{before["display_name"]} {colors.white}à {colors.light_red}{after["display_name"]}{colors.white} le {colors.light_red}{timestamp}{colors.white}')
                    
                    else:
                        continue
                
                elif content['type'] == 'voice_state_updates' and config['spy']['voice_state_updates']:
                    if content['before_data']['channel_id'] == None and content['after_data']['channel_id'] != None:
                        guild_name = utils.get_guild_name(content['guild_id'])
                        print(
                            f'\n{self.space}{colors.light_red}• {colors.white}Vocal rejoint dans {colors.light_red}{guild_name}{colors.white} le {colors.light_red}{timestamp}{colors.white}'
                            f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                        )
                    
                    elif content['before_data']['channel_id'] != None and content['after_data']['channel_id'] == None:
                        guild_name = utils.get_guild_name(content['guild_id'])
                        print(
                            f'\n{self.space}{colors.light_red}• {colors.white}Vocal quitté dans {colors.light_red}{guild_name}{colors.white} le {colors.light_red}{timestamp}{colors.white}'
                            f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["before_data"]["channel_id"]}{colors.white}'
                        )
                    
                    elif content['before_data']['channel_id'] != None and content['after_data']['channel_id'] != None:
                        if content['before_data']['channel_id'] == content['after_data']['channel_id']:
                            guild_name = utils.get_guild_name(content['guild_id'])

                            if content['before_data']['self_deaf'] != content['after_data']['self_deaf']:
                                if content['after_data']['self_deaf']:
                                    print(
                                        f'\n{self.space}{colors.light_red}• {colors.white}Sourdine activée dans {colors.light_red}{guild_name}{colors.white} le {colors.light_red}{timestamp}{colors.white}'
                                        f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                                    )
                                else:
                                    print(
                                        f'\n{self.space}{colors.light_red}• {colors.white}Sourdine désactivée dans {colors.light_red}{guild_name}{colors.white} le {colors.light_red}{timestamp}{colors.white}'
                                        f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                                    )

                            elif content['before_data']['self_mute'] != content['after_data']['self_mute']:
                                if content['after_data']['self_mute']:
                                    print(
                                        f'\n{self.space}{colors.light_red}• {colors.white}Muet activé dans {colors.light_red}{guild_name}{colors.white} le {colors.light_red}{timestamp}{colors.white}'
                                        f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                                    )
                                else:
                                    print(
                                        f'\n{self.space}{colors.light_red}• {colors.white}Muet désactivé dans {colors.light_red}{guild_name}{colors.white} le {colors.light_red}{timestamp}{colors.white}'
                                        f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                                    )

                            elif content['before_data']['self_stream'] != content['after_data']['self_stream']:
                                if content['after_data']['self_stream']:
                                    print(
                                        f'\n{self.space}{colors.light_red}• {colors.white}Streaming activé dans {colors.light_red}{guild_name}{colors.white} le {colors.light_red}{timestamp}{colors.white}'
                                        f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                                    )
                                else:
                                    print(
                                        f'\n{self.space}{colors.light_red}• {colors.white}Streaming désactivé dans {colors.light_red}{guild_name}{colors.white} le {colors.light_red}{timestamp}{colors.white}'
                                        f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                                    )

                            else:
                                continue
                        
                        else:
                            print(
                                f'\n{self.space}{colors.light_red}• {colors.white}Salon vocal changé dans {colors.light_red}{guild_name}{colors.white} le {colors.light_red}{timestamp}{colors.white}'
                                f'\n{self.space}{colors.light_red}┆ {colors.white}Ancien salon  {colors.light_gray}-> {colors.light_red}#{content["before_data"]["channel_id"]}{colors.white}'
                                f'\n{self.space}{colors.light_red}╰ {colors.white}Nouveau salon {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                            )
                    
                    else:
                        continue
        
        input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
    
    
    def logs_channel(self):
        self.base()
        
        value = input(f'\n{self.space}{colors.light_red}• {colors.white}Entrez l\'ID Discord du salon à rechercher: {colors.light_red}')
        
        if not value:
            return
        
        print(f'\n{self.space}{colors.white}( {colors.tan}⚡{colors.white}) {colors.tan}Recherche de l\'ID Discord{colors.reset}')
        
        try:
            result = utils.spy_channel(value)
        except error.HTTPError:
            cooldown = utils.get_cooldown()
            if cooldown['amount'] >= cooldown['maximum']:
                result = {'code': 429}
            else:
                result = {'code': 404}
        
        if result['code'] == 404:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}ID Discord introuvable{colors.reset}')
        elif result['code'] == 429:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Vous faites trop de requêtes !{colors.reset}')
        else:
            print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) {colors.light_green}ID Discord trouvé !{colors.reset}')
            for message_type in ['sent_messages', 'deleted_messages', 'edited_messages']:
                for item in result['data'][message_type]:
                    item['type'] = message_type
            
            contents:list = result['data']['sent_messages'] + result['data']['deleted_messages'] + result['data']['edited_messages']
            
            if len(contents) == 0:
                print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Aucun contenu trouvé{colors.reset}')
                input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
                return
            
            for content in contents:
                content['timestamp'] = datetime.strptime(content['timestamp'].replace('T', ' ').replace('+00:00', '').split('.')[0], '%Y-%m-%d %H:%M:%S')
            contents.sort(key=lambda x: x['timestamp'], reverse=True)
            
            for content in contents:
                timestamp = content['timestamp'].strftime('%d/%m/%Y %H:%M:%S')
                config = utils.get_config()
                
                if content['type'] == 'sent_messages' and config['spy']['sent_messages']:
                    event = 'Message envoyé'
                    channel = content['channel_id']
                    guild = utils.get_guild(channel)
                    message = content['content'].split('\n')
                    
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} dans {colors.light_red}#{channel} {colors.white}({colors.light_red}{guild}{colors.white}) le {colors.light_red}{timestamp}{colors.white}')
                    
                    for i, line in enumerate(message):
                        if i != len(message) - 1:
                            print(f'{self.space}{colors.light_red}┆ {colors.white}{line}')
                        else:
                            print(f'{self.space}{colors.light_red}╰ {colors.white}{line}')
                
                elif content['type'] == 'deleted_messages' and config['spy']['deleted_messages']:
                    event = 'Message supprimé'
                    channel = content['channel_id']
                    guild = utils.get_guild(channel)
                    message = content['content'].split('\n')
                    
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} dans {colors.light_red}#{channel} {colors.white}({colors.light_red}{guild}{colors.white}) le {colors.light_red}{timestamp}{colors.white}')
                    
                    for i, line in enumerate(message):
                        if i != len(message) - 1:
                            print(f'{self.space}{colors.light_red}┆ {colors.white}{line}')
                        else:
                            print(f'{self.space}{colors.light_red}╰ {colors.white}{line}')
                
                elif content['type'] == 'edited_messages' and config['spy']['edited_messages']:
                    if content['before_content'] == content['after_content']:
                        continue
                    
                    event = 'Message édité'
                    channel = content['channel_id']
                    guild = utils.get_guild(channel)
                    before = content['before_content'].split('\n')
                    after = content['after_content'].split('\n')
                    
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} dans {colors.light_red}#{channel} {colors.white}({colors.light_red}{guild}{colors.white}) le {colors.light_red}{timestamp}{colors.white}')
                
                    for line in before:
                        print(f'{self.space}{colors.light_red}┆ {colors.white}{line}')
                        
                    print(f'{self.space}{colors.light_red}├{"─"*3}')
                    
                    for i, line in enumerate(after):
                        if i != len(after) - 1:
                            print(f'{self.space}{colors.light_red}┆ {colors.white}{line}')
                        else:
                            print(f'{self.space}{colors.light_red}╰ {colors.white}{line}')
                            
        input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
        
    
    def logs_guild(self):
        self.base()
        
        value = input(f'\n{self.space}{colors.light_red}• {colors.white}Entrez l\'ID Discord du serveur à rechercher: {colors.light_red}')
        
        if not value:
            return
        
        print(f'\n{self.space}{colors.white}( {colors.tan}⚡{colors.white}) {colors.tan}Recherche de l\'ID Discord{colors.reset}')
        
        try:
            result = utils.spy_guild(value)
        except error.HTTPError:
            cooldown = utils.get_cooldown()
            if cooldown['amount'] >= cooldown['maximum']:
                result = {'code': 429}
            else:
                result = {'code': 404}
        
        if result['code'] == 404:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}ID Discord introuvable{colors.reset}')
        elif result['code'] == 429:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Vous faites trop de requêtes !{colors.reset}')
        else:
            print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) {colors.light_green}ID Discord trouvé !{colors.reset}')
            for message_type in ['member_joins', 'member_leaves', 'member_bans', 'member_unbans', 'guild_updates', 'voice_state_updates']:
                for item in result['data'][message_type]:
                    item['type'] = message_type
            
            contents:list = result['data']['member_joins'] + result['data']['member_leaves'] + result['data']['member_bans'] + result['data']['member_unbans'] + result['data']['guild_updates'] + result['data']['voice_state_updates']
            
            if len(contents) == 0:
                print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Aucun contenu trouvé{colors.reset}')
                input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
                return
            
            for content in contents:
                content['timestamp'] = datetime.strptime(content['timestamp'].replace('T', ' ').replace('+00:00', '').split('.')[0], '%Y-%m-%d %H:%M:%S')
            contents.sort(key=lambda x: x['timestamp'], reverse=True)
            
            for content in contents:
                timestamp = content['timestamp'].strftime('%d/%m/%Y %H:%M:%S')
                config = utils.get_config()
                
                if content['type'] == 'member_joins' and config['spy']['member_joins']:
                    try:
                        user = utils.get_user_data(content['user_id'])['data']['name']
                    except error.HTTPError:
                        user = content['user_id']
                    
                    event = 'a rejoint'
                    print(f'\n{self.space}{colors.light_red}• {colors.light_red}{user} {colors.white}{event} le serveur le {colors.light_red}{timestamp}{colors.white}')
                
                elif content['type'] == 'member_leaves' and config['spy']['member_leaves']:
                    try:
                        user = utils.get_user_data(content['user_id'])['data']['name']
                    except error.HTTPError:
                        user = content['user_id']
                    
                    event = 'a quitté'
                    print(f'\n{self.space}{colors.light_red}• {colors.light_red}{user} {colors.white}{event} le serveur le {colors.light_red}{timestamp}{colors.white}')
                
                elif content['type'] == 'member_bans' and config['spy']['member_bans']:
                    try:
                        user = utils.get_user_data(content['user_id'])['data']['name']
                    except error.HTTPError:
                        user = content['user_id']
                    
                    event = 'a été banni'
                    print(f'\n{self.space}{colors.light_red}• {colors.light_red}{user} {colors.white}{event} le serveur le {colors.light_red}{timestamp}{colors.white}')
                
                elif content['type'] == 'member_unbans' and config['spy']['member_unbans']:
                    try:
                        user = utils.get_user_data(content['user_id'])['data']['name']
                    except error.HTTPError:
                        user = content['user_id']
                    
                    event = 'a été débanni'
                    print(f'\n{self.space}{colors.light_red}• {colors.light_red}{user} {colors.white}{event} le serveur le {colors.light_red}{timestamp}{colors.white}')
                
                elif content['type'] == 'guild_updates' and config['spy']['guild_updates']:
                    before = content['before_data']
                    after = content['after_data']
                    
                    if before['name'] != after['name']:
                        print(f'\n{self.space}{colors.light_red}• {colors.white}Le serveur a été renommé le {colors.light_red}{timestamp}{colors.white}')
                        print(f'{self.space}{colors.light_red}┆ {colors.white}Nom avant {colors.light_gray}-> {colors.light_red}{before["name"]}{colors.white}')
                        print(f'{self.space}{colors.light_red}╰ {colors.white}Nom après {colors.light_gray}-> {colors.light_red}{after["name"]}{colors.white}')

                    elif before['icon'] != after['icon']:
                        print(f'\n{self.space}{colors.light_red}• {colors.white}Icône changée le {colors.light_red}{timestamp}{colors.white}')
                    
                    else:
                        continue
                
                elif content['type'] == 'voice_state_updates' and config['spy']['voice_state_updates']:
                    try:
                        user = utils.get_user_data(content['user_id'])['data']['name']
                    except error.HTTPError:
                        user = content['user_id']
                    
                    if content['before_data']['channel_id'] == None and content['after_data']['channel_id'] != None:
                        print(
                            f'\n{self.space}{colors.light_red}• {colors.light_red}{user} {colors.white}a rejoint un vocal le {colors.light_red}{timestamp}{colors.white}'
                            f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                        )
                    
                    elif content['before_data']['channel_id'] != None and content['after_data']['channel_id'] == None:
                        print(
                            f'\n{self.space}{colors.light_red}• {colors.light_red}{user} {colors.white}a quitté un vocal le {colors.light_red}{timestamp}{colors.white}'
                            f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["before_data"]["channel_id"]}{colors.white}'
                        )
                    
                    elif content['before_data']['channel_id'] != None and content['after_data']['channel_id'] != None:
                        if content['before_data']['channel_id'] == content['after_data']['channel_id']:
                            if content['before_data']['self_deaf'] != content['after_data']['self_deaf']:
                                if content['after_data']['self_deaf']:
                                    print(
                                        f'\n{self.space}{colors.light_red}• {colors.light_red}{user} {colors.white}est en sourdine le {colors.light_red}{timestamp}{colors.white}'
                                        f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                                    )
                                else:
                                    print(
                                        f'\n{self.space}{colors.light_red}• {colors.light_red}{user} {colors.white}n\'est plus en sourdine le {colors.light_red}{timestamp}{colors.white}'
                                        f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                                    )

                            elif content['before_data']['self_mute'] != content['after_data']['self_mute']:
                                if content['after_data']['self_mute']:
                                    print(
                                        f'\n{self.space}{colors.light_red}• {colors.light_red}{user} {colors.white}est muet le {colors.light_red}{timestamp}{colors.white}'
                                        f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                                    )
                                else:
                                    print(
                                        f'\n{self.space}{colors.light_red}• {colors.light_red}{user} {colors.white}n\'est plus muet le {colors.light_red}{timestamp}{colors.white}'
                                        f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                                    )

                            elif content['before_data']['self_stream'] != content['after_data']['self_stream']:
                                if content['after_data']['self_stream']:
                                    print(
                                        f'\n{self.space}{colors.light_red}• {colors.light_red}{user} {colors.white}est en stream le {colors.light_red}{timestamp}{colors.white}'
                                        f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                                    )
                                else:
                                    print(
                                        f'\n{self.space}{colors.light_red}• {colors.light_red}{user} {colors.white}n\'est en stream le {colors.light_red}{timestamp}{colors.white}'
                                        f'\n{self.space}{colors.light_red}╰ {colors.white}Salon vocal {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                                    )

                            else:
                                continue
                        
                        else:
                            print(
                                f'\n{self.space}{colors.light_red}• {colors.white}Salon vocal changé le {colors.light_red}{timestamp}{colors.white}'
                                f'\n{self.space}{colors.light_red}┆ {colors.white}Ancien salon  {colors.light_gray}-> {colors.light_red}#{content["before_data"]["channel_id"]}{colors.white}'
                                f'\n{self.space}{colors.light_red}╰ {colors.white}Nouveau salon {colors.light_gray}-> {colors.light_red}#{content["after_data"]["channel_id"]}{colors.white}'
                            )
                    
                    else:
                        continue
                
        input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
    
    
    def logs_messages(self):
        self.base()
        
        value = input(f'\n{self.space}{colors.light_red}• {colors.white}Entrez le message à rechercher: {colors.light_red}')
        
        if not value:
            return
        
        print(f'\n{self.space}{colors.white}( {colors.tan}⚡{colors.white}) {colors.tan}Recherche de messages Discord{colors.reset}')
        
        try:
            result = utils.spy_message(value)
        except error.HTTPError:
            cooldown = utils.get_cooldown()
            if cooldown['amount'] >= cooldown['maximum']:
                result = {'code': 429}
            else:
                result = {'code': 404}
        
        if result['code'] == 404:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Aucun message trouvé...{colors.reset}')
        elif result['code'] == 429:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Vous faites trop de requêtes !{colors.reset}')
        else:
            contents:list = result['data']['sent_messages'] + result['data']['deleted_messages'] + result['data']['edited_messages']
            if len(contents) == 0:
                print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Aucun contenu trouvé{colors.reset}')
                input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
                return
            
            print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) {colors.light_green}Messages trouvés !{colors.reset}')
            for message_type in ['sent_messages', 'deleted_messages', 'edited_messages']:
                for item in result['data'][message_type]:
                    item['type'] = message_type
            
            for content in contents:
                content['timestamp'] = datetime.strptime(content['timestamp'].replace('T', ' ').replace('+00:00', '').split('.')[0], '%Y-%m-%d %H:%M:%S')
            contents.sort(key=lambda x: x['timestamp'], reverse=True)
            
            for content in contents:
                try:
                    username = utils.get_user_data(content["author_id"])['data']['name']
                except error.HTTPError:
                    username = utils.lookup_discord(content["author_id"])['username']
                
                channel = content['channel_id']
                guild = utils.get_guild(channel)
                timestamp = content['timestamp'].strftime('%d/%m/%Y %H:%M:%S')
                config = utils.get_config()
                
                if content['type'] == 'sent_messages' and config['spy']['sent_messages']:
                    event = 'Message envoyé'
                    message = content['content'].split('\n')
                    
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} dans {colors.light_red}#{channel} {colors.white}par {colors.light_red}{username} {colors.white}({colors.light_red}{guild}{colors.white}) le {colors.light_red}{timestamp}{colors.white}')
                    
                    for i, line in enumerate(message):
                        if i != len(message) - 1:
                            print(f'{self.space}{colors.light_red}┆ {colors.white}{line}')
                        else:
                            print(f'{self.space}{colors.light_red}╰ {colors.white}{line}')
                            
                elif content['type'] == 'deleted_messages' and config['spy']['deleted_messages']:
                    event = 'Message supprimé'
                    message = content['content'].split('\n')
                    
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} dans {colors.light_red}#{channel} {colors.white}par {colors.light_red}{username} {colors.white}({colors.light_red}{guild}{colors.white}) le {colors.light_red}{timestamp}{colors.white}')
                    
                    for i, line in enumerate(message):
                        if i != len(message) - 1:
                            print(f'{self.space}{colors.light_red}┆ {colors.white}{line}')
                        else:
                            print(f'{self.space}{colors.light_red}╰ {colors.white}{line}')
                            
                elif content['type'] == 'edited_messages' and config['spy']['edited_messages']:
                    if content['before_content'] == content['after_content']:
                        continue
                    
                    event = 'Message édité'
                    before = content['before_content'].split('\n')
                    after = content['after_content'].split('\n')
                    
                    print(f'\n{self.space}{colors.light_red}• {colors.white}{event} dans {colors.light_red}#{channel} {colors.white}par {colors.light_red}{username} {colors.white}({colors.light_red}{guild}{colors.white}) le {colors.light_red}{timestamp}{colors.white}')
                    
                    for line in before:
                        print(f'{self.space}{colors.light_red}┆ {colors.white}{line}')
                    
                    print(f'{self.space}{colors.light_red}├{"─"*3}')
                    
                    for i, line in enumerate(after):
                        if i != len(after) - 1:
                            print(f'{self.space}{colors.light_red}┆ {colors.white}{line}')
                        else:
                            print(f'{self.space}{colors.light_red}╰ {colors.white}{line}')
                            
        input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
    
    def configuration(self):
        while True:
            self.base()

            config = utils.get_config()

            response = input(
                f"\n{self.space}{colors.light_red}• {colors.white}Configuration actuelle"
                f"\n"
                f"\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}01{colors.white}) Messages envoyés          {colors.light_gray}-> {f'{colors.light_green}✓' if config['spy']['sent_messages'] else f'{colors.light_red}✗'}{colors.white}"
                f"\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}02{colors.white}) Messages supprimés        {colors.light_gray}-> {f'{colors.light_green}✓' if config['spy']['deleted_messages'] else f'{colors.light_red}✗'}{colors.white}"
                f"\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}03{colors.white}) Messages édités           {colors.light_gray}-> {f'{colors.light_green}✓' if config['spy']['edited_messages'] else f'{colors.light_red}✗'}{colors.white}"
                f"\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}04{colors.white}) Serveurs rejoins          {colors.light_gray}-> {f'{colors.light_green}✓' if config['spy']['member_joins'] else f'{colors.light_red}✗'}{colors.white}"
                f"\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}05{colors.white}) Serveurs quittés          {colors.light_gray}-> {f'{colors.light_green}✓' if config['spy']['member_leaves'] else f'{colors.light_red}✗'}{colors.white}"
                f"\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}06{colors.white}) Membres bannis            {colors.light_gray}-> {f'{colors.light_green}✓' if config['spy']['member_bans'] else f'{colors.light_red}✗'}{colors.white}"
                f"\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}07{colors.white}) Membres débannis          {colors.light_gray}-> {f'{colors.light_green}✓' if config['spy']['member_unbans'] else f'{colors.light_red}✗'}{colors.white}"
                f"\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}08{colors.white}) Mises à jour utilisateurs {colors.light_gray}-> {f'{colors.light_green}✓' if config['spy']['user_updates'] else f'{colors.light_red}✗'}{colors.white}"
                f"\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}09{colors.white}) Mises à jour vocal        {colors.light_gray}-> {f'{colors.light_green}✓' if config['spy']['voice_state_updates'] else f'{colors.light_red}✗'}{colors.white}"
                f"\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}10{colors.white}) Mises à jour serveur      {colors.light_gray}-> {f'{colors.light_green}✓' if config['spy']['guild_updates'] else f'{colors.light_red}✗'}{colors.white}"
                f'\n{self.space}{colors.light_red}└─ • {colors.white}'
            )
            
            if response == '':
                break
            
            try:
                response = int(response)
            except:
                continue
            
            if response < 1 or response > 10:
                continue
            
            config['spy']['sent_messages'] = not config['spy']['sent_messages'] if response == 1 else config['spy']['sent_messages']
            config['spy']['deleted_messages'] = not config['spy']['deleted_messages'] if response == 2 else config['spy']['deleted_messages']
            config['spy']['edited_messages'] = not config['spy']['edited_messages'] if response == 3 else config['spy']['edited_messages']
            config['spy']['member_joins'] = not config['spy']['member_joins'] if response == 4 else config['spy']['member_joins']
            config['spy']['member_leaves'] = not config['spy']['member_leaves'] if response == 5 else config['spy']['member_leaves']
            config['spy']['member_bans'] = not config['spy']['member_bans'] if response == 6 else config['spy']['member_bans']
            config['spy']['member_unbans'] = not config['spy']['member_unbans'] if response == 7 else config['spy']['member_unbans']
            config['spy']['user_updates'] = not config['spy']['user_updates'] if response == 8 else config['spy']['user_updates']
            config['spy']['voice_state_updates'] = not config['spy']['voice_state_updates'] if response == 9 else config['spy']['voice_state_updates']
            config['spy']['guild_updates'] = not config['spy']['guild_updates'] if response == 10 else config['spy']['guild_updates']
            
            dump(config, open('config.json', 'w'), indent=4)
    
    
    def info(self):
        self.base()
        
        result = utils.get_cooldown()
        result2 = utils.get_info()
        
        state = f'{colors.light_green}A jour{colors.white}' if version == result2['data']['version'] else f'{colors.red}Mise a jour nécessaire{colors.white}'
        
        print(
            f"\n{self.space}{colors.light_red}• {colors.white}Cooldown {colors.light_gray}-> {colors.white}{colors.light_red}{result['amount']}{colors.white} / {colors.light_red}{result['maximum']}{colors.white} requêtes par heure",
            f"\n{self.space}{colors.light_red}• {colors.white}Status   {colors.light_gray}-> {colors.light_red}{result['status_name']} {colors.white}({result['status']})",
            f"\n{self.space}{colors.light_red}• {colors.white}Reset    {colors.light_gray}-> {colors.white}Il y a {colors.light_red}{round((datetime.now().timestamp() - result['lastReset']) // 60)}{colors.white} minutes et {colors.light_red}{round((datetime.now().timestamp() - result['lastReset']) % 60)}{colors.white} secondes",
            f"\n",
            f"\n{self.space}{colors.light_red}• {colors.white}Version  {colors.light_gray}-> {colors.light_red}{result2['data']['version']} {colors.white}({state}{colors.white})",
            f"\n{self.space}{colors.light_red}• {colors.white}Pseudos  {colors.light_gray}-> {colors.light_red}{result2['data']['count']}{colors.white} pseudos dans la base de données",
            f"\n{self.space}{colors.light_red}• {colors.white}Serveurs {colors.light_gray}-> {colors.light_red}{result2['data']['server']}{colors.white} serveurs espionnés",
        )
        
        input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
    
    
    def new_key(self):
        self.base()
        
        key = input(f'\n{self.space}{colors.light_red}• {colors.white}Entrez votre nouvelle clé API: {colors.light_red}')
        
        if not key:
            return
        
        print(f'\n{self.space}{colors.white}( {colors.tan}⚡{colors.white}) {colors.tan}Vérification de la clé API{colors.reset}')
        try:
            response = utils.is_key_valid(key)
        except error.HTTPError:
            response = {'code': 404}
            
        if response['code'] == 404:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Clé API invalide{colors.reset}')
        else:
            print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) {colors.light_green}Clé API valide{colors.reset}')
            open('KEY', 'w').write(key)
            print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) {colors.light_green}Clé API mise à jour{colors.reset}')
        
        input(f'\n{self.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')




if __name__ == '__main__':
    ui = ui()
    while True:
        try:
            ui.base()
            result = ui.menu()
            
            try:
                result = int(result)
            except:
                continue

            if result == 1:
                ui.search()
                continue
            
            if result == 2:
                ui.linked()
                continue
            
            if result == 3:
                ui.lookup()
                continue
            
            if result == 4:
                ui.logs_user()
                continue
            
            if result == 5:
                ui.logs_channel()
                continue
            
            if result == 6:
                ui.logs_guild()
                continue
                
            if result == 7:
                ui.logs_messages()
                continue
            
            if result == 8:
                ui.configuration()
                continue
            
            if result == 9:
                ui.new_key()
                continue
            
            if result == 10:
                ui.info()
                continue
            
            if result == 11:
                exit()
        
        except KeyboardInterrupt:
            continue
        
        except Exception as e:
            ERROR = [line for line in format_exc().split('\n') if line != '']
            
            print(f'\n{ui.space}{colors.white}( {colors.red}⚡{colors.white}) {colors.red}Une erreur est survenue{colors.reset}')
            for i, line in enumerate(ERROR):
                print(f'  {ui.space}{colors.red}{'┆' if i != len(ERROR) - 1 else '╰'} {colors.white}{line}')
            
            input(f'\n{ui.space}{colors.light_red}• {colors.white}Appuyez sur {colors.light_red}ENTRÉE{colors.white} pour continuer...')
            continue