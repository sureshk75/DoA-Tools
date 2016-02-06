import http.client
import json
import os
from binascii import b2a_hex
from hashlib import sha1
from operator import itemgetter
from time import time, sleep

__version__ = '2.0.2'

########################################################################################################################
#                                             SCRIPT SECTION - Do Not Edit!                                            #
########################################################################################################################
# -------------------------------------------------------------------------------------------------------------------- #
#                                                   GAME DICTIONARIES                                                  #
# -------------------------------------------------------------------------------------------------------------------- #
speed_items_dict = [{'item': 'Blitz', 'exceed': 216000, 'time': 345600},
                    {'item': 'Blast', 'exceed': 86400, 'time': 216000},
                    {'item': 'Bolt', 'exceed': 54000, 'time': 86400},
                    {'item': 'Bore', 'exceed': 28800, 'time': 54000},
                    {'item': 'Bounce', 'exceed': 9000, 'time': 28800},
                    {'item': 'Leap', 'exceed': 3600, 'time': 9000},
                    {'item': 'Jump', 'exceed': 900, 'time': 3600},
                    {'item': 'Skip', 'exceed': 300, 'time': 900},
                    {'item': 'Hop', 'exceed': 60, 'time': 300},
                    {'item': 'Blink', 'exceed': 0, 'time': 60}]

building_dict = {'capital': {'buildings': {'Farm', 'Lumbermill', 'Mine', 'Quarry', 'ScienceCenter', 'Home', 'Rookery',
                                           'DragonKeep', 'Fortress', 'Garrison', 'OfficerQuarter', 'StorageVault',
                                           'Metalsmith', 'MusterPoint', 'Wall', 'Sentinel', 'Theater', 'Factory'},
                             'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 32, 9: 35, 10: 38, 11: 39},
                             'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31,
                                         11: 32}},
                 'cave': {'buildings': {'CaveDragonKeep', 'CaveCathedral', 'CaveDepot', 'CaveForge', 'CaveGreenhouse',
                                        'CaveLibrary', 'CaveTrainingCamp', 'CaveWorkshop'},
                          'f_slots': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
                          'c_slots': {1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8, 9: 8, 10: 8, 11: 8, 12: 8}},
                 'chrono': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                          'Farm', 'Mine', 'Home', 'Silo'},
                            'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                        12: 30},
                            'c_slots': {1: 29, 2: 29, 3: 29, 4: 29, 5: 29, 6: 29, 7: 29, 8: 29, 9: 29, 10: 29, 11: 29,
                                        12: 29}},
                 'colossus': {'buildings': {'ColossusDragonKeep', 'ColossusWall', 'Warehouse', 'TroopQuarters',
                                            'WarpGate', 'WarpPortal'},
                              'f_slots': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
                              'c_slots': {1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10, 10: 10, 11: 10,
                                          12: 10}},
                 'desert': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                          'Farm', 'Mine', 'Home', 'Silo'},
                            'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                        12: 30},
                            'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                        12: 31}},
                 'fire': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                        'Farm', 'Mine', 'Home', 'Silo'},
                          'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                      12: 30},
                          'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                      12: 31}},
                 'forest': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                          'Farm', 'Mine', 'Home', 'Silo'},
                            'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                        12: 30},
                            'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                        12: 31}},
                 'ice': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                       'Farm', 'Mine', 'Home', 'Silo'},
                         'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                     12: 30},
                         'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                     12: 31}},
                 'leviathan': {'buildings': {'LeviathanDragonKeep', 'LeviathanWall', 'LeviathanWarehouse',
                                             'LeviathanMarketplace', 'LeviathanTroopQuarters'},
                               'f_slots': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
                               'c_slots': {1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10, 10: 10,
                                           11: 10, 12: 10}},
                 'luna': {'buildings': {'DragonKeep', 'LunaShrine', 'LunaDepot', 'LunaCathedral', 'LunaForge',
                                        'LunaGreenhouse', 'LunaLibrary', 'LunaWorkshop'},
                          'f_slots': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
                          'c_slots': {1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8, 9: 8, 10: 8, 11: 8, 12: 8}},
                 'skythrone': {
                     'buildings': {'Forge', 'Workshop', 'Cathedral', 'Greenhouse', 'Library', 'KaiserDragonKeep'},
                     'f_slots': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
                     'c_slots': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}},
                 'spectral': {'buildings': {'SpectralDragonKeep', 'DarkPortal', 'Mausoleum', 'EnergyCollector'},
                              'f_slots': {1: 2, 2: 2, 3: 2, 4: 4, 5: 6, 6: 8, 7: 11, 8: 14, 9: 17, 10: 20, 11: 20,
                                          12: 20},
                              'c_slots': {1: 2, 2: 2, 3: 4, 4: 6, 5: 8, 6: 10, 7: 14, 8: 18, 9: 22, 10: 26, 11: 26,
                                          12: 26}},
                 'stone': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                         'Farm', 'Mine', 'Home', 'Silo'},
                           'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                       12: 30},
                           'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                       12: 31}},
                 'swamp': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                         'Farm', 'Mine', 'Home', 'Silo'},
                           'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                       12: 30},
                           'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                       12: 31}},
                 'water': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                         'Farm', 'Mine', 'Home', 'Silo'},
                           'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                       12: 30},
                           'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                       12: 31}},
                 'wind': {'buildings': {'TrainingCamp', 'Wall', 'DragonKeep', 'MusterPoint', 'Lumbermill', 'Quarry',
                                        'Farm', 'Mine', 'Home', 'Silo'},
                          'f_slots': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30,
                                      12: 30},
                          'c_slots': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31,
                                      12: 31}}}


# -------------------------------------------------------------------------------------------------------------------- #
#                                              FUNCTIONAL CLASSES/MODULES                                              #
# -------------------------------------------------------------------------------------------------------------------- #
def div_line(default='_', suffix=True):
    print(' ' + (default * 78))
    if suffix:
        print(' ')


def screen_update(title, subtitle):
    os.system('cls' if os.name == 'nt' else 'clear')
    v_len = len(__version__)
    try:
        a = '{0}({1})'.format(pData['name'], d_rn) if d_rn != 0 else ''
    except (KeyError, NameError):
        a = ''
    print('\n {0:<55}  {1:>21}\n     {2:<{3}}{4}'.format(
            title.capitalize(), a, subtitle.title(), 74 - v_len, __version__))
    div_line()


def web_ops(operation, param_add_on, method='POST', post=True):
    global realm, std_param, cookie, d_conn
    url = 'http://{0}/api/{1}.json'.format(realm, operation)
    params = param_add_on + '{0}&timestamp={1}'.format(std_param, int(time()))
    d_conn.connect()
    if not post:
        d_conn.request(method, url + params)
    else:
        cmd = 'Draoumculiasis' + params + 'LandCrocodile' + url + 'Bevar-Asp'
        headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive', 'Content-Length': len(params), 'Origin': 'http://' + realm,
                   'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': cookie, 'DNT': 1, 'Host': realm,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like'
                                 ' Gecko Chrome/45.0.2454.101 Safari/537.36)',
                   'X-Requested-With': 'ShockwaveFlash/19.0.0.226', 'X-S3-AWS': sha1(cmd.encode('utf-8')).hexdigest()}
        d_conn.request(method, url, params, headers)
    try:
        conn_resp = d_conn.getresponse()
        if conn_resp.status == 200:
            conn_json = conn_resp.read().decode('utf-8')
            return json.loads(conn_json)
        elif conn_resp.status == 429:
            d_conn.close()
            for ban_countdown in range(3660):
                screen_update('{0}'.format(lo['91']), '{0}'.format(lo['92']))
                prog(ban_countdown, 3660, '{0}: {1}'.format(lo['94'], cvt_time(3660 - ban_countdown)))
                sleep(1)
        elif conn_resp.status == 509:
            d_conn.close()
            for ban_countdown in range(60):
                screen_update('{0}'.format(lo['91']), '{0}'.format(lo['93']))
                prog(ban_countdown, 60, '{0}: {1}'.format(lo['95'], cvt_time(60 - ban_countdown)))
                sleep(1)
        elif conn_resp.status == 502:
            sleep(5)
        else:
            div_line('#')
            ctr_it('{0} {1}'.format(lo['96'], conn_resp.status))
            ctr_it('{0}'.format(lo['25']))
            os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
            quit()
    except http.client.CannotSendRequest:
        div_line('#')
        ctr_it('{0}'.format(lo['97']))
        ctr_it('{0}'.format(lo['98']))
        os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
        quit()
    except http.client.HTTPException:
        d_conn.close()
        sleep(2)


def prog(p_count, p_total, prefix, suffix=None):
    filled_len = int(round(50 * p_count / float(p_total)))
    bar = ('▓' * filled_len) + ('░' * (50 - filled_len))
    print(prefix.center(78))
    print(bar.center(78))
    if suffix:
        print(suffix.center(78))


def get_data(title, pl=True, fm=False, pf=False, op=False, w1=False, w2=False, w3=False, unmute=True):
    global pData, mData, fData, pfData, cData, tData, d_conn, fStat
    sub_hdr = lo['16'] if pData or mData or fData or pfData or cData else lo['17']
    w1_data, w2_data = [None, None]
    max_count, count = [0, 0]
    for check in (w1, w2, w3, pl, fm, pf):
        if check:
            max_count += 1
    if unmute:
        screen_update(title, sub_hdr)
        prog(count, max_count, lo['18'])

    # Get Manifest and Translation
    conn = http.client.HTTPConnection('wackoscripts.com', 80)
    req = [{'0': w1, '1': lo['19'], '2': 'manifest'},
           {'0': w2, '1': lo['20'], '2': 'chest'},
           {'0': w3, '1': lo['21'], '2': 'forgestat'}]
    for x in range(len(req)):
        if req[x]['0']:
            name = req[x]['1']
            url = 'http://wackoscripts.com/sanctuary/{0}.json'.format(req[x]['2'])
            if unmute:
                screen_update(title, sub_hdr)
                prog(count, max_count, '{0} {1}'.format(lo['22'], name))
            for web_retry in range(2):
                try:
                    conn.connect()
                    conn.request('GET', url)
                    conn_resp = conn.getresponse()
                    conn_data = json.loads(conn_resp.read().decode('utf-8'))
                    count += 1
                    if req[x]['2'] == 'manifest':
                        mData = conn_data
                    elif req[x]['2'] == 'chest':
                        w1_data = conn_data
                    elif req[x]['2'] == 'forgestat':
                        fStat = conn_data
                    conn.close()
                    break
                except (KeyError, TypeError):
                    if unmute:
                        screen_update(title, sub_hdr)
                        prog(count, max_count, '{0} {1}'.format(lo['22'], name),
                             '{0}: {1}/2'.format(lo['23'], web_retry + 1))
                    sleep(1)
                    continue
            else:
                div_line('#')
                ctr_it('{0} {1}'.format(lo['24'], name))
                ctr_it(lo['25'])
                div_line('#')
                sleep(5)
                quit()
            if w1_data:
                for key, value in w1_data.items():
                    if key not in tData and value != '':
                        tData[key] = value
                    if key not in tData and value == '':
                        tData[key] = key

    # Get Forge and Player
    req = [{'0': pl, '1': lo['26'], '2': 'player', '3': '?', '4': 'GET', '5': False},
           {'0': fm, '1': lo['27'], '2': 'forge/forge', '3': '', '4': 'GET', '5': True},
           {'0': pf, '1': lo['28'], '2': 'forge/player_forge_info', '3': '', '4': 'GET', '5': True}]
    for x in range(len(req)):
        if req[x]['0']:
            name = req[x]['1']
            if unmute:
                screen_update(title, sub_hdr)
                prog(count, max_count, '{0} {1}'.format(lo['22'], name))
            for web_retry in range(2):
                try:
                    conn_data = web_ops(req[x]['2'], req[x]['3'], req[x]['4'], req[x]['5'])
                    count += 1
                    if req[x]['2'] == 'forge/forge':
                        fData = conn_data
                    elif req[x]['2'] == 'player':
                        pData = conn_data
                    elif req[x]['2'] == 'forge/player_forge_info':
                        pfData = conn_data
                    break
                except (KeyError, TypeError):
                    if unmute:
                        screen_update(title, sub_hdr)
                        prog(count, max_count, '{0} {1}'.format(lo['22'], name),
                             '{0}: {1}/2'.format(lo['23'], web_retry + 1))
                    sleep(1)
                    continue
            else:
                div_line('#')
                ctr_it('{0} {1}'.format(lo['24'], name))
                ctr_it(lo['25'])
                div_line('#')
                sleep(5)
                quit()

    # Process City Data
    if op:
        cData = {}
        for loc_key in sorted(pData['cities']):
            if unmute:
                screen_update(title, sub_hdr)
                prog(1, 1, '{0} {1}'.format(lo['29'], t(loc_key)))
            for web_retry in range(5):
                try:
                    current_location = web_ops('cities/{0}'.format(pData['cities'][loc_key]['id']), '')
                    cData[loc_key] = current_location
                    break
                except (KeyError, TypeError):
                    if unmute:
                        screen_update(title, sub_hdr)
                        prog(1, 1, '{0} {1}'.format(lo['29'], t(loc_key)),
                             '{0}: {1}/5'.format(lo['23'], web_retry + 1))
                    sleep(1)
                    continue
            else:
                div_line('#')
                ctr_it(lo['30'])
                ctr_it(lo['25'])
                div_line('#')
                quit()

    # Save Entry If Loading Went Well...
    acct = list()
    verify_record = list()
    unique_id = '{0}-{1}'.format(d_ui, d_rn)
    try:
        with open('DoA-Tools.doa', 'r') as read_file:
            r_file = json.load(read_file)
            for x in range(len(r_file)):
                acct.append(r_file[x])
                if r_file[x]['id'] not in verify_record:
                    verify_record.append(r_file[x]['id'])
            if unique_id not in verify_record:
                my_dict = {'id': unique_id, 'ac': pData['name'], 'ui': d_ui, 'dh': d_dh,
                           'rn': d_rn, 'cn': d_cn}
                acct.append(my_dict)
    except FileNotFoundError:
        my_dict = {'id': unique_id, 'ac': pData['name'], 'ui': d_ui, 'dh': d_dh,
                   'rn': d_rn, 'cn': d_cn}
        acct.append(my_dict)
    finally:
        with open('DoA-Tools.doa', 'w') as create_file:
            json.dump(acct, create_file)


def cvt_time(time_value=0, show_seconds=True):
    m, s = divmod(time_value, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if show_seconds:
        if d > 0:
            return '{0:,}d {1:0>2}h {2:0>2}m {3:0>2}s'.format(int(d), int(h), int(m), int(s))
        elif h > 0:
            return '{0}h {1:0>2}m {2:0>2}s'.format(int(h), int(m), int(s))
        elif m > 0:
            return '{0}m {1:0>2}s'.format(int(m), int(s))
        else:
            return '{0}s'.format(int(s))
    else:
        if d > 0:
            return '{0:,}d {1:0>2}h {2:0>2}m'.format(int(d), int(h), int(m))
        elif h > 0:
            return '{0}h {1:0>2}m'.format(int(h), int(m))
        else:
            return '{0}m'.format(int(m))


def ctr_it(string, prefix=False, suffix=False):
    if prefix:
        print('')
    print(string.center(78))
    if suffix:
        print('')


def choose_language(title='', shut_script=True):
    global lo
    conn = http.client.HTTPConnection('wackoscripts.com', 80)
    url = 'http://wackoscripts.com/sanctuary/locale.json'
    conn_data = None
    for web_retry in range(2):
        try:
            conn.connect()
            conn.request('GET', url)
            conn_resp = conn.getresponse()
            conn_data = json.loads(conn_resp.read().decode('utf-8'))
            conn.close()
            break
        except (KeyError, TypeError) as err:
            print(err)
            sleep(1)
            continue
    else:
        div_line('#')
        ctr_it(lo['99'])
        ctr_it(lo['25'])
        div_line('#')
        sleep(5)
        quit()
    if conn_data:
        d_lang = None
        while d_lang is None:
            if title:
                screen_update(title, ' ')
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
            ctr_it('~~~ Language/Sprog/Sprache/Idioma/Langue/Lingua/Taal/Språk/Dil ~~~', prefix=True)
            for x in range(len(conn_data)):
                ctr_it(conn_data[x]['type'])
            div_line()
            d_select = input('\n Vælge/Auswählen/Seleccionar/Sélectionner/Selezionare/Välj/Seçin\n Select : ')
            if len(d_select) >= 3:
                for x in range(len(conn_data)):
                    if d_select.lower() == conn_data[x]['type'].lower():
                        d_lang = conn_data[x]['type']
                        lo = conn_data[x]['locale']
                        break
                else:
                    for x in range(len(conn_data)):
                        if d_select.lower() in conn_data[x]['type'].lower():
                            d_lang = conn_data[x]['type']
                            lo = conn_data[x]['locale']
                            break
        with open('locale.doa', 'w') as create_file:
            json.dump(lo, create_file)
        if shut_script:
            ctr_it(lo['P1'], prefix=True, suffix=True)
            sleep(5)
            quit()


def check_version():
    if __version__ != fStat['version']:
        screen_update(lo['44'], lo['45'])
        div_line('*')
        ctr_it('DoA-Tools v{0} {1}'.format(fStat['version'], lo['O4']), suffix=True)
        ctr_it(lo['O5'])
        ctr_it(fStat['url'], suffix=True)
        div_line('*')
        sleep(5)


def t(string):
    if string in tData.keys():
        return tData[string]
    else:
        return string


def display_it(my_list, single=True):
    if single:
        max_len = len(max(my_list.values(), key=len))
        max_items = int(76 / (max_len + 2)) if max_len <= 34 else 1
        if len(my_list) < max_items:
            max_items = len(my_list)
        x = ''
        y = 0
        for value in sorted(my_list.values()):
            x += ' {0:{1}} '.format(value, max_len)
            if y == max_items - 1:
                ctr_it(x)
                y = 0
                x = ''
            else:
                y += 1
        if y != 0:
            z = ' ' * ((max_len + 2) * (max_items - y))
            x += z
            ctr_it(x)
    else:
        max_len_key = max_len_value = 0
        for key, value in my_list.items():
            if len(key) > max_len_key:
                max_len_key = len(key)
            if len(str(value)) > max_len_value:
                max_len_value = len(str(value))
        max_len = max_len_key + max_len_value
        max_items = int(76 / (max_len + 4)) if max_len <= 32 else 1
        if len(my_list) < max_items:
            max_items = len(my_list)
        x = ''
        y = 0
        for key, value in sorted(my_list.items()):
            txt = '{0:>{1}}: {2:<{3}}'.format(key, max_len_key, value, max_len_value)
            x += ' {0:<{1}} '.format(txt, max_len)
            if y == max_items - 1:
                ctr_it(x)
                y = 0
                x = ''
            else:
                y += 1
        if y != 0:
            z = ' ' * ((max_len + 4) * (max_items - y))
            x += z
            ctr_it(x)


def set_batch(max_value, exec_string=''):
    div_line('-')
    ctr_it('~~~ {0} ~~~'.format(lo['86']))
    ctr_it('1 - {0}'.format(max_value - 1), suffix=True)
    ctr_it('{0}'.format(exec_string))
    div_line()
    i = input(' {0} : '.format(lo['06']))
    if len(i) >= 1:
        if i.lower() == lo['N1'] or i.lower() == 'exit':
            return 'exit'
        if i.isnumeric():
            if int(i) in range(1, max_value):
                return int(i)


def set_delay():
    div_line('-')
    ctr_it('~~~ {0} ~~~'.format(lo['86']))
    ctr_it('0 - 5', suffix=True)
    ctr_it(lo['87'])
    ctr_it(lo['88'], suffix=True)
    ctr_it(lo['89'])
    div_line()
    i = input(' {0} : '.format(lo['06']))
    if len(i) >= 1:
        if i.lower() == lo['N1'] or i.lower() == 'exit':
            return 'exit'
        if i.isnumeric():
            if int(i) in range(6):
                return int(i)


def proceed_run():
    div_line('-')
    ctr_it('~~~ {0} ~~~'.format(lo['86']))
    ctr_it(lo['90'], suffix=True)
    ctr_it(lo['72'])
    div_line()
    i = input(' {0} : '.format(lo['06']))
    if len(i) >= 1:
        if i.lower() == lo['N1'] or i.lower() == 'exit':
            return 'exit'
        if i.isalpha():
            if i.lower() == lo['D6'].lower() or i.lower() == 'yes':
                return True
            elif i.lower() == lo['D7'].lower() or i.lower() == 'no':
                return 'exit'


def nothing_to_do(title, subtitle, exec_string):
    screen_update(title, subtitle)
    div_line('*')
    ctr_it(exec_string, suffix=True)
    div_line('*')
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')


def smart_truncate(content, length=100, suffix='..'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length + 1].split(' ')[0:-1]) + suffix


def exit_script():
    os.system('cls' if os.name == 'nt' else 'clear')
    ctr_it('{0} DoA Tools v{1}'.format(lo['O6'], __version__), prefix=True, suffix=True)
    ctr_it(lo['O7'])
    ctr_it(fStat['author'])
    ctr_it('{0} {1}'.format(lo['O8'], fStat['contrib']), suffix=True)
    ctr_it(lo['O9'])
    ctr_it(fStat['url'], suffix=True)
    sleep(3)
    quit()


def enter_script(title):
    global d_ui, d_dh, d_rn, d_cn, pData, mData, fData, pfData, cData, tData
    pData, mData, fData, pfData, cData = [{}, {}, {}, {}, {}]
    d_ui, d_dh, d_rn, d_cn = [0, 0, 0, 0]
    selection = {}
    r_file = None
    try:
        with open('DoA-Tools.doa', 'r') as read_file:
            r_file = json.load(read_file)
            for x in range(len(r_file)):
                selection[r_file[x]['id']] = '{0}({1})'.format(r_file[x]['ac'], r_file[x]['rn'])
    except FileNotFoundError:
        pass
    if selection:
        selected = False
        while not selected:
            screen_update(title, '{0}'.format(lo['03']))
            ctr_it('~~~ {0} ~~~'.format(lo['04']), suffix=True)
            display_it(selection)
            print('\n\n {0}'.format(lo['05']))
            div_line()
            i = input(' {0} : '.format(lo['06']))
            if len(i) >= 1:
                if i.lower() == lo['P0'] or i.lower() == 'new':
                    break
                for key, value in selection.items():
                    if i.lower() == value.lower():
                        for x in range(len(r_file)):
                            if r_file[x]['id'] == key:
                                d_ui = r_file[x]['ui']
                                d_dh = r_file[x]['dh']
                                d_rn = r_file[x]['rn']
                                d_cn = r_file[x]['cn']
                                selected = True
                                break
                        break
                else:
                    for key, value in selection.items():
                        if i.lower() in value.lower():
                            for x in range(len(r_file)):
                                if r_file[x]['id'] == key:
                                    d_ui = r_file[x]['ui']
                                    d_dh = r_file[x]['dh']
                                    d_rn = r_file[x]['rn']
                                    d_cn = r_file[x]['cn']
                                    selected = True
                                    break
                            break
    get_account_info(title)
    get_realm_info(title)
    switch_realm(title, d_rn, d_cn)


def check_input(entry, input_list):
    for key, value in input_list.items():
        if entry.lower() == value.lower():
            return key
    else:
        for key, value in input_list.items():
            if entry.lower() in value.lower():
                return key
        else:
            return None


# -------------------------------------------------------------------------------------------------------------------- #
#                                             INTERACTIVE CLASSES/MODULES                                              #
# -------------------------------------------------------------------------------------------------------------------- #
def get_account_info(title):
    global d_ui, d_dh, d_si
    while not d_ui:
        screen_update(title, lo['07'])
        d_select = input(' {0} : '.format(lo['08']))
        if len(d_select) >= 1:
            if d_select.isnumeric():
                d_ui = int(d_select)

    while not d_dh:
        screen_update(title, lo['07'])
        ctr_it('{0}: {1}'.format(lo['09'], d_ui))
        div_line()
        d_select = input(' {0} : '.format(lo['10']))
        if len(d_select) >= 3:
            if d_select.isalnum():
                d_dh = d_select


def get_realm_info(title):
    global d_rn, d_cn
    while not d_rn:
        screen_update(title, lo['11'])
        ctr_it('{0}: {1}   {2}: {3:.15}..'.format(lo['09'], d_ui, lo['12'], d_dh))
        ctr_it(' ')
        div_line()
        d_select = input(' {0} : '.format(lo['13']))
        if len(d_select) >= 1:
            if d_select.isnumeric():
                d_rn = int(d_select)

    while not d_cn:
        screen_update(title, lo['11'])
        ctr_it('{0}: {1}   {2}: {3:.15}..'.format(lo['09'], d_ui, lo['12'], d_dh))
        ctr_it('{0}: {1}'.format(lo['14'], d_rn))
        div_line()
        d_select = input(' {0} : '.format(lo['15']))
        if len(d_select) >= 1:
            if d_select.isnumeric():
                d_cn = int(d_select)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                      FORGE CLASS                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
def create_equipment(title):
    # Initialize Craftable Equipment
    screen_update(title, lo['49'])
    ctr_it(lo['18'])
    d_list = list()
    selection = {}
    d_blacksmith = pfData['result']['blacksmith']['level']
    for key in sorted(fData['forge']['items'].keys()):
        if fData['forge']['items'][key]['troop_slot_number'] in (1, 2):
            try:
                bs_level = fData['forge']['recipes'][key]['requirements']['blacksmith_level']
            except KeyError:
                continue
            if d_blacksmith >= bs_level:
                try:
                    ingredients = pData['forge']['items']['ingredients']
                    recipe = fData['forge']['recipes'][key]['requirements']
                except KeyError:
                    continue
                d_max_queue = 9999
                met_req = (len(recipe['items']))
                for r_key, r_value in recipe['items'].items():
                    for r_item in range(len(ingredients)):
                        if r_key == ingredients[r_item]['name']:
                            if r_value < ingredients[r_item]['quantity']:
                                met_req -= 1
                                if d_max_queue > int(ingredients[r_item]['quantity'] / r_value):
                                    d_max_queue = int(ingredients[r_item]['quantity'] / r_value)
                            else:
                                break
                if met_req == 0:
                    f_multiply = fStat[key] if key in fStat else 1
                    for x in range(len(mData['units'])):
                        if mData['units'][x]['type'] == fData['forge']['items'][key]['troop_type']:
                            my_dict = {'troop': mData['units'][x]['type'],
                                       'item': key, 'craftable': d_max_queue,
                                       'defense': int(mData['units'][x]['stats']['defense'] * f_multiply),
                                       'life': int(mData['units'][x]['stats']['life'] * f_multiply),
                                       'melee': int(mData['units'][x]['stats']['melee'] * f_multiply),
                                       'range': int(mData['units'][x]['stats']['range'] * f_multiply),
                                       'ranged': int(mData['units'][x]['stats']['ranged'] * f_multiply),
                                       'speed': int(mData['units'][x]['stats']['speed'] * f_multiply)}
                            d_list.append(my_dict)
    if not d_list:
        nothing_to_do(title, lo['49'], lo['50'])
        return
    else:
        for x in range(len(d_list)):
            if d_list[x]['troop'] not in selection.keys():
                selection[d_list[x]['troop']] = t(d_list[x]['troop'])

    # Select Troop For Equipment Crafting
    d_troop = None
    while d_troop is None:
        screen_update(title, lo['49'])
        ctr_it('~~~ {0} ~~~'.format(lo['51']))
        display_it(selection)
        div_line()
        d_select = input(' {0} : '.format(lo['06']))
        if len(d_select) >= 1:
            if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                return
            else:
                d_troop = check_input(d_select, selection)
    d_list[:] = [d for d in d_list if d.get('troop') == d_troop]
    selection.clear()
    for x in range(len(d_list)):
        if d_list[x]['item'] not in selection.keys():
            selection[d_list[x]['item']] = t(d_list[x]['item'])

    # Select Equipment To Craft
    a, b, c, d, e, f, g, h = [lo['52'], lo['53'], lo['54'].title(), lo['55'].title(), lo['56'].title(),
                              lo['57'].title(), lo['58'].title(), lo['59'].title()]
    a1, b1, c1, d1, e1, f1, g1, h1 = [len(a), len(b), len(c), len(d), len(e), len(f), len(g), len(h)]
    for x in range(len(d_list)):
        if len(t(d_list[x]['item'])) > a1:
            a1 = len(t(d_list[x]['item']))
        if len('{0:,}'.format(d_list[x]['craftable'])) > b1:
            b1 = len('{0:,}'.format(d_list[x]['craftable']))
        if len('{0:,}'.format(d_list[x]['defense'])) > c1:
            c1 = len('{0:,}'.format(d_list[x]['defense']))
        if len('{0:,}'.format(d_list[x]['life'])) > d1:
            d1 = len('{0:,}'.format(d_list[x]['life']))
        if len('{0:,}'.format(d_list[x]['melee'])) > e1:
            e1 = len('{0:,}'.format(d_list[x]['melee']))
        if len('{0:,}'.format(d_list[x]['range'])) > f1:
            f1 = len('{0:,}'.format(d_list[x]['range']))
        if len('{0:,}'.format(d_list[x]['ranged'])) > g1:
            g1 = len('{0:,}'.format(d_list[x]['ranged']))
        if len('{0:,}'.format(d_list[x]['speed'])) > h1:
            h1 = len('{0:,}'.format(d_list[x]['speed']))
    d_item = None
    while d_item is None:
        screen_update(title, lo['60'])
        ctr_it('{0}: {1}'.format(lo['61'], t(d_troop)))
        ctr_it(' ')
        div_line('-')
        ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}} {6:^{7}} {8:^{9}} {10:^{11}} {12:^{13}} {14:^{15}}'.format(
            a, a1, b, b1, c, c1, d, d1, e, e1, f, f1, g, g1, h, h1))
        ctr_it('{0}  {1}  {2} {3} {4} {5} {6} {7}'.format(
            '~' * a1, '~' * b1, '~' * c1, '~' * d1, '~' * e1, '~' * f1, '~' * g1, '~' * h1))
        for x in range(len(d_list)):
            ctr_it('{0:<{1}}  {2:^{3},}  {4:>{5},} {6:>{7},} {8:>{9},} {10:>{11},} {12:>{13},} {14:>{15},}'.format(
                t(d_list[x]['item']), a1, d_list[x]['craftable'], b1, d_list[x]['defense'], c1, d_list[x]['life'],
                d1,
                d_list[x]['melee'], e1, d_list[x]['range'], f1, d_list[x]['range'], g1, d_list[x]['speed'], h1))
        div_line()
        d_select = input(' {0} : '.format(lo['06']))
        if len(d_select) >= 1:
            if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                return
            else:
                d_item = check_input(d_select, selection)
    d_list[:] = [d for d in d_list if d.get('item') == d_item]

    # Set Minimum Equipment Stat
    d_attrib, d_stat = [None, None]
    while d_attrib is None:
        screen_update(title, lo['62'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['61'], t(d_troop), lo['63'], t(d_item)))
        ctr_it(' ')
        div_line('-')
        ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}  {8:^{9}}  {10:^{11}}'.format(
            c, c1, d, d1, e, e1, f, f1, g, g1, h, h1))
        ctr_it('{0}  {1}  {2}  {3}  {4}  {5}'.format('~' * c1, '~' * d1, '~' * e1, '~' * f1, '~' * g1, '~' * h1))
        for x in range(len(d_list)):
            ctr_it('{0:^{1},}  {2:^{3},}  {4:^{5},}  {6:^{7},}  {8:^{9},}  {10:^{11},}'.format(
                d_list[x]['defense'], c1, d_list[x]['life'], d1, d_list[x]['melee'], e1, d_list[x]['range'], f1,
                d_list[x]['range'], g1, d_list[x]['speed'], h1))
        print('\n {0}'.format(lo['64']))
        div_line()
        d_select = input(' {0} : '.format(lo['06']))
        if len(d_select) >= 4:
            if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                return
            else:
                try:
                    i_attrib, i_stat = d_select.split('@')
                    if i_stat.isnumeric():
                        if i_attrib.lower() == lo['54'] or i_attrib.lower() == 'defense':
                            d_attrib = 'defense'
                        elif i_attrib.lower() == lo['55'] or i_attrib.lower() == 'life':
                            d_attrib = 'life'
                        elif i_attrib.lower() == lo['56'] or i_attrib.lower() == 'melee':
                            d_attrib = 'melee'
                        elif i_attrib.lower() == lo['57'] or i_attrib.lower() == 'range':
                            d_attrib = 'range'
                        elif i_attrib.lower() == lo['58'] or i_attrib.lower() == 'ranged':
                            d_attrib = 'ranged'
                        elif i_attrib.lower() == lo['59'] or i_attrib.lower() == 'speed':
                            d_attrib = 'speed'
                        d_stat = int(i_stat)
                        break
                except(TypeError, ValueError):
                    sleep(1)

    # Set Number Of Batches
    d_batch = None
    while d_batch is None:
        screen_update(title, lo['67'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['61'], t(d_troop), lo['63'], t(d_item)))
        ctr_it('{0}: {1:,} {2}'.format(lo['65'], d_stat, d_attrib.title()))
        d_batch = set_batch(d_list[0]['craftable'] + 1, '{0}'.format(lo['68']))
        if d_batch == lo['N1'] or d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, lo['69'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['61'], t(d_troop), lo['63'], t(d_item)))
        ctr_it('{0}: {1:,} {2}   {3}: {4:,}'.format(lo['65'], d_stat, d_attrib.title(), lo['66'], d_batch))
        d_delay = set_delay()
        if d_delay == lo['N1'] or d_delay == 'exit':
            return

    # Proceed Forging
    d_proceed = False
    while not d_proceed:
        screen_update(title, lo['70'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['61'], t(d_troop), lo['63'], t(d_item)))
        ctr_it('{0}: {1:,} {2}   {3}: {4:,}   {5}: {6}s'.format(
            lo['65'], d_stat, d_attrib.title(), lo['66'], d_batch, lo['71'], d_delay))
        d_proceed = proceed_run()
        if d_proceed == lo['N1'] or d_proceed == 'exit':
            return

    # Forge Equipment
    d_start = time()
    f_succ, f_fail, len_item = [0, 0, 0]
    kept_items = list()
    crushed_items = {}
    for x in range(1, d_batch + 1):
        screen_update(title, lo['73'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['61'], t(d_troop), lo['63'], t(d_item)))
        ctr_it('{0}: {1:,} {2}   {3}: {4:,}   {5}: {6}s   {7}: {8}'.format(
            lo['65'], d_stat, d_attrib.title(), lo['66'], d_batch, lo['71'], d_delay, lo['74'],
            cvt_time(time() - d_start)))
        div_line('-')
        prog(x, d_batch, '{0}: {1}/{2}'.format(lo['66'], x, d_batch),
             '{0}: {1:,}  {2}: {3:,}  {4}: {5:,}  {6}: {7:,}'.format(
                 lo['75'], f_succ, lo['76'], f_fail, lo['77'], len(kept_items), lo['78'], f_succ - len(kept_items)))
        if kept_items:
            ctr_it('~~~ {0} ~~~'.format(lo['79']), prefix=True)
            for y in range(len(kept_items)):
                k_item = '{0} {1}: '.format(lo['80'], y + 1) + ', '.join('{0} {1}'.format(
                    k_i.title(), v_i) for k_i, v_i in kept_items[y].items())
                if len(k_item) > len_item:
                    len_item = len(k_item)
                ctr_it('{0:<{1}}'.format(k_item, len_item))
        if crushed_items:
            ctr_it('~~~ {0} ~~~'.format(lo['81']), prefix=True)
            display_it(crushed_items, single=False)
        crush_it = False
        x_param = 'output%5Fname={0}&'.format(d_item)
        for web_retry in range(5):
            sleep(d_delay)
            try:
                main_json = web_ops('forge/forge_item', x_param)
                result = main_json['result']['success']
                if result:
                    forge_equip = main_json['result']['forge_result']
                    if forge_equip != 'failure':
                        f_succ += 1
                        if d_attrib in forge_equip['stats'].keys() and d_stat <= forge_equip['stats'][d_attrib]:
                            kept_items.append(forge_equip['stats'])
                        else:
                            x_param = 'player%5Fforge%5Fequipment%5Fid={0}&'.format(forge_equip['id'])
                            crush_it = True
                    else:
                        f_fail += 1
                    break
            except (KeyError, TypeError):
                sleep(1)
                continue
        if crush_it:
            for web_retry in range(5):
                sleep(d_delay)
                try:
                    crush_json = web_ops('forge/disenchant_equipment', x_param)
                    result = crush_json['result']['success']
                    if result:
                        for y in range(len(crush_json['result']['disenchanted_ingredients'])):
                            if t(crush_json['result']['disenchanted_ingredients'][y]) in crushed_items:
                                crushed_items[t(crush_json['result']['disenchanted_ingredients'][y])] += 1
                            else:
                                crushed_items[t(crush_json['result']['disenchanted_ingredients'][y])] = 1
                        break
                except (KeyError, TypeError):
                    sleep(1)
                    continue
    screen_update(title, lo['82'])
    ctr_it('{0}: {1}   {2}: {3}'.format(lo['61'], t(d_troop), lo['63'], t(d_item)))
    ctr_it('{0}: {1:,} {2}   {3}: {4:,}   {5}: {6}s'.format(
        lo['65'], d_stat, d_attrib.title(), lo['83'], d_batch, lo['71'], d_delay))
    div_line('-')
    prog(1, 1, '{0} {1}'.format(lo['84'], cvt_time(time() - d_start)),
         '{0}: {1:,}  {2}: {3:,}  {4}: {5:,}  {6}: {7:,}'.format(
             lo['75'], f_succ, lo['76'], f_fail, lo['77'], len(kept_items), lo['78'],
             f_succ - len(kept_items)))
    if kept_items:
        ctr_it('~~~ {0} ~~~'.format(lo['79']), prefix=True)
        for y in range(len(kept_items)):
            k_item = '{0} {1}: '.format(lo['80'], y + 1) + ', '.join('{0} {1}'.format(
                k_i.title(), v_i) for k_i, v_i in kept_items[y].items())
            ctr_it('{0:<{1}}'.format(k_item, len_item))
    if crushed_items:
        ctr_it('~~~ {0} ~~~'.format(lo['81']), prefix=True)
        display_it(crushed_items, single=False)
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
    print(lo['85'])
    get_data(title, pf=True, op=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def forge_ingredient(title):
    # Initialize Craftable Ingredient
    screen_update(title, lo['A0'])
    ctr_it(lo['18'])
    d_list = list()
    selection = {}
    d_blacksmith = pfData['result']['blacksmith']['level']
    x = 0
    for forge_key in reversed(sorted(fData['forge']['items'].keys())):
        if fData['forge']['items'][forge_key]['type'] == 'ingredient':
            try:
                bs_level = fData['forge']['recipes'][forge_key]['requirements']['blacksmith_level']
            except KeyError:
                continue
            if d_blacksmith >= bs_level:
                try:
                    ingredients = pData['forge']['items']['ingredients']
                    recipe = fData['forge']['recipes'][forge_key]['requirements']
                except KeyError:
                    continue
                d_max_queue = 1024
                d_avail = 0
                for r_item in range(len(ingredients)):
                    if forge_key == ingredients[r_item]['name']:
                        d_avail = ingredients[r_item]['quantity']
                        d_max_queue = 1024 - d_avail
                if d_max_queue != 0:
                    count = (len(recipe['items']))
                    for r_key, r_qty in recipe['items'].items():
                        for r_item in range(len(ingredients)):
                            if r_key == ingredients[r_item]['name']:
                                if r_qty < ingredients[r_item]['quantity']:
                                    count -= 1
                                    if d_max_queue > int(ingredients[r_item]['quantity'] / r_qty):
                                        d_max_queue = int(ingredients[r_item]['quantity'] / r_qty)
                                else:
                                    break
                    if count == 0:
                        my_dict = {'item': forge_key, 'available': d_avail, 'craftable': d_max_queue}
                        d_list.insert(x, my_dict)
    if not d_list:
        nothing_to_do(title, lo['A0'], lo['A1'])
        return

    # Select Ingredient for Crafting
    a, b, c = [lo['A2'], lo['A3'], lo['A4']]
    a1, b1, c1 = [len(a), len(b), len(c)]
    for x in range(len(d_list)):
        if d_list[x]['item'] not in selection.keys():
            selection[d_list[x]['item']] = t(d_list[x]['item'])
        if len(t(d_list[x]['item'])) > a1:
            a1 = len(t(d_list[x]['item']))
        if len('{0:,}'.format(d_list[x]['available'])) > b1:
            b1 = len('{0:,}'.format(d_list[x]['available']))
        if len('{0:,}'.format(d_list[x]['craftable'])) > c1:
            c1 = len('{0:,}'.format(d_list[x]['craftable']))
    d_item = None
    while d_item is None:
        screen_update(title, lo['A5'])
        ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
        ctr_it('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
        for x in range(len(d_list)):
            ctr_it('{0:<{1}}  {2:>{3},}  {4:>{5},}'.format(
                t(d_list[x]['item']), a1, d_list[x]['available'], b1, d_list[x]['craftable'], c1))
        div_line()
        d_select = input(' {0} : '.format(lo['06']))
        if len(d_select) >= 1:
            if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                return
            else:
                d_item = check_input(d_select, selection)
    d_list[:] = [d for d in d_list if d.get('item') == d_item]

    # Set Number Of Batches
    d_batch = None
    while d_batch is None:
        screen_update(title, lo['69'])
        ctr_it('{0}: {1}'.format(lo['A2'], t(d_item)))
        ctr_it(' ')
        d_batch = set_batch(d_list[0]['craftable'] + 1, '{0}'.format(lo['N2']))
        if d_batch == lo['N1'] or d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, lo['69'])
        ctr_it('{0}: {1}   {2}: {3:,}'.format(lo['A2'], t(d_item), lo['66'], d_batch))
        ctr_it(' ')
        d_delay = set_delay()
        if d_delay == lo['N1'] or d_delay == 'exit':
            return

    # Proceed Forging
    d_proceed = False
    while not d_proceed:
        screen_update(title, lo['70'])
        ctr_it('{0}: {1}   {2}: {3:,}'.format(lo['A2'], t(d_item), lo['66'], d_batch))
        ctr_it('{0}: {1}s'.format(lo['71'], d_delay))
        d_proceed = proceed_run()
        if d_proceed == lo['N1'] or d_proceed == 'exit':
            return

    # Forge Ingredients
    selection.clear()
    base_list = {}
    d_start = time()
    for x in range(len(pData['forge']['items']['ingredients'])):
        if t(pData['forge']['items']['ingredients'][x]['name']) not in base_list:
            base_list[t(pData['forge']['items']['ingredients'][x]['name'])] = pData[
                'forge']['items']['ingredients'][x]['quantity']
    for x in range(1, d_batch + 1):
        screen_update(title, lo['73'])
        ctr_it('{0}: {1}   {2}: {3:,}'.format(lo['A2'], t(d_item), lo['66'], d_batch))
        ctr_it('{0}: {1}s   {2}: {3}'.format(lo['71'], d_delay, lo['74'], cvt_time(time() - d_start)))
        div_line('-')
        prog(x, d_batch, '{0}: {1}/{2}'.format(lo['B0'], x, d_batch))
        if selection:
            ctr_it('~~~ {0} ~~~'.format(lo['B1']), prefix=True)
            display_it(selection, single=False)
        for web_retry in range(5):
            sleep(d_delay)
            try:
                x_param = 'output%5Fname={0}&'.format(d_item)
                main_json = web_ops('forge/forge_item', x_param)
                result = main_json['result']['success']
                if result:
                    check_use = main_json['result']['forge_items']['ingredients']
                    for y in range(len(check_use)):
                        item_name = t(check_use[y]['name'])
                        if item_name in base_list.keys() and check_use[y]['quantity'] < base_list[item_name]:
                            selection[item_name] = base_list[item_name] - check_use[y]['quantity']
                    break
            except (KeyError, TypeError):
                sleep(1)
                continue
    screen_update(title, lo['82'])
    ctr_it('{0}: {1}   {2}: {3:,}'.format(lo['A2'], t(d_item), lo['83'], d_batch))
    ctr_it('{0}: {1}s'.format(lo['71'], d_delay))
    div_line('-')
    prog(1, 1, '{0} {1}'.format(lo['84'], cvt_time(time() - d_start)))
    if selection:
        ctr_it('~~~ {0} ~~~'.format(lo['B1']), prefix=True)
        display_it(selection, single=False)
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
    print(lo['85'])
    get_data(title, pf=True, op=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #


def farm_mission(title):
    # Initialize Player Missions
    screen_update(title, lo['B2'])
    ctr_it(lo['18'])
    d_list = list()
    selection = {}
    adventurers = pData['forge']['adventurers']
    missions = fData['forge']['missions']
    claimed = False
    for x in range(len(adventurers)):
        if adventurers[x]['current_mission'] is not None:
            x_param = 'adventurer_id={0}&mission_type={1}&'.format(
                adventurers[x]['adventurer_id'], adventurers[x]['current_mission'])
            item_json = web_ops('player_missions/claim_mission', x_param)
            if item_json['result']['success']:
                claimed = True
            else:
                selection[adventurers[x]['current_mission']] = adventurers[x]['current_mission']
    if claimed:
        get_data(title, pf=True, unmute=False)
        adventurers = pData['forge']['adventurers']
    ingredients = {}
    for x in range(len(pData['forge']['items']['ingredients'])):
        ingredients[pData['forge']['items']['ingredients'][x]['name']] = pData['forge']['items']['ingredients'][x][
            'quantity']
    for x in range(len(adventurers)):
        if adventurers[x]['current_mission'] is None:
            d_level = 0
            for key, value in reversed(
                    sorted(fData['forge']['adventurers'][adventurers[x]['type']]['level_exp'].items())):
                if adventurers[x]['experience'] >= value:
                    d_level = int(key) + 1
                    break
            for mission in sorted(missions.keys()):
                checked = False
                d_max_queue = 9999999
                if mission in selection.keys():
                    continue
                if d_level < missions[mission]['requirements']['adventurer_level']:
                    continue
                if missions[mission]['ends_at'] != 0 and missions[mission]['ends_at'] < time():
                    continue
                if 'any' not in missions[mission]['adventurers'][0] and adventurers[x]['type'] not in \
                        missions[mission]['adventurers'][0]:
                    continue
                if len(missions[mission]['requirements']['items']) > 0:
                    for r_key, r_value in (missions[mission]['requirements']['items']).items():
                        if r_key not in ingredients.keys():
                            break
                        else:
                            if r_value > ingredients[r_key]:
                                break
                            else:
                                checked = True
                                if int(ingredients[r_key] / r_value) < d_max_queue:
                                    d_max_queue = int(ingredients[r_key] / r_value)
                else:
                    checked = True
                if checked:
                    my_dict = {'adventurer': adventurers[x]['type'], 'id': adventurers[x]['adventurer_id'],
                               'mission': mission, 'desc': t(mission), 'time': missions[mission]['cooldown'],
                               'batch': d_max_queue}
                    d_list.append(my_dict)

    if not d_list:
        nothing_to_do(title, lo['B2'], lo['B3'])
        return
    selection.clear()

    # Select Mission
    a, b, c = [lo['B4'], lo['B5'], lo['B6']]
    a1, b1, c1 = [len(a), len(b), len(c)]
    for x in range(len(d_list)):
        if len(t(d_list[x]['mission'])) > a1:
            a1 = len(t(d_list[x]['mission']))
        if len(cvt_time(d_list[x]['time'], show_seconds=False)) > b1:
            b1 = len(cvt_time(d_list[x]['time'], show_seconds=False))
        if len('{0:,}'.format(d_list[x]['batch'])) > c1:
            c1 = len('{0:,}'.format(d_list[x]['batch']))
    d_list = sorted(d_list, key=itemgetter('desc'))
    d_mission = None
    while d_mission is None:
        screen_update(title, lo['B2'])
        ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
        ctr_it('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
        for x in range(len(d_list)):
            if d_list[x]['mission'] not in selection.keys():
                selection[d_list[x]['mission']] = d_list[x]['desc']
                c = '{0}'.format(lo['B7']) if d_list[x]['batch'] == 9999999 else '{0:,}'.format(d_list[x]['batch'])
                ctr_it('{0:<{1}}  {2:>{3}}  {4:>{5}}'.format(
                    d_list[x]['desc'], a1, cvt_time(d_list[x]['time'], show_seconds=False), b1, c, c1))
        div_line()
        d_select = input(' {0} : '.format(lo['06']))
        if len(d_select) >= 3:
            if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                return
            else:
                d_mission = check_input(d_select, selection)
    d_list[:] = [d for d in d_list if d.get('mission') == d_mission]
    selection.clear()
    for x in range(len(d_list)):
        if d_list[x]['adventurer'] not in selection.keys():
            selection[d_list[x]['adventurer']] = t(d_list[x]['adventurer'])

    # Select Adventurer
    d_adventurer = None
    while d_adventurer is None:
        screen_update(title, lo['B8'])
        ctr_it('{0}: {1} ({2})'.format(lo['B4'], t(d_mission), cvt_time(d_list[0]['time'], show_seconds=False)))
        ctr_it(' ')
        div_line('-')
        ctr_it('~~~ {0} ~~~'.format(lo['C0']))
        display_it(selection)
        div_line()
        d_select = input(' {0} : '.format(lo['06']))
        if len(d_select) >= 3:
            if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                return
            else:
                d_adventurer = check_input(d_select, selection)
    d_list[:] = [d for d in d_list if d.get('adventurer') == d_adventurer]

    # Select Speed Items
    d_speed = list()
    a, b, c, d = [lo['80'], lo['C1'], lo['A3'], lo['C2']]
    a1, b1, c1, d1 = [len(a), len(b), len(c), len(d)]
    for key in range(len(speed_items_dict)):
        look_up = speed_items_dict[key]
        if look_up['item'] in pData['items'] and pData['items'][look_up['item']] > 0:
            if len(look_up['item']) > a1:
                a1 = len(look_up['item'])
            if len(cvt_time(look_up['time'], show_seconds=False)) > b1:
                b1 = len(cvt_time(look_up['time'], show_seconds=False))
            if len('{0:,}'.format(pData['items'][look_up['item']])) > c1:
                c1 = len('{0:,}'.format(pData['items'][look_up['item']]))
            my_dict = {'item': look_up['item'], 'time': look_up['time'],
                       'qty': pData['items'][look_up['item']], 'use': 0}
            d_speed.append(my_dict)
    if not d_speed:
        nothing_to_do(title, lo['B2'], lo['C3'])
        return

    while True:
        screen_update(title, lo['L1'])
        ctr_it('{0}: {1} ({2})   {3}: {4}'.format(
            lo['B4'], t(d_mission), cvt_time(d_list[0]['time'], show_seconds=False), lo['C5'], t(d_adventurer)))
        ctr_it(' ')
        div_line('-')
        ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}'.format(a, a1, b, b1, c, c1, d, d1))
        ctr_it('{0}  {1}  {2}  {3}'.format('~' * a1, '~' * b1, '~' * c1, '~' * d1))
        reduced_time = d_list[0]['time']
        for key in range(len(d_speed)):
            ctr_it('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}'.format(
                d_speed[key]['item'], a1, cvt_time(d_speed[key]['time'], show_seconds=False), b1,
                d_speed[key]['qty'], c1, d_speed[key]['use'], d1))
            if d_speed[key]['use']:
                reduced_time -= d_speed[key]['time'] * d_speed[key]['use']
                reduced_time = 0 if reduced_time <= 0 else reduced_time
        ctr_it('{0}: {1}'.format(lo['A7'], cvt_time(reduced_time, show_seconds=False)), prefix=True, suffix=True)
        if reduced_time != 0:
            print(' {0}'.format(lo['C6']))
        else:
            print(' {0}'.format(lo['C7']))
        div_line()
        d_select = input(' {0} '.format(lo['06']))
        if len(d_select) >= 2:
            if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                return
            elif reduced_time == 0 and d_select.lower() == lo['N4']:
                break
            else:
                try:
                    i_item, i_qty = d_select.split('@')
                    if i_qty.isnumeric():
                        for x in range(len(d_speed)):
                            if i_item.lower() == t(d_speed[x]['item']).lower() and int(i_qty) < d_speed[x]['qty']:
                                d_speed[x]['use'] = int(i_qty)
                                break
                        else:
                            for x in range(len(d_speed)):
                                if i_item.lower() in t(d_speed[x]['item']).lower() and int(i_qty) < d_speed[x]['qty']:
                                    d_speed[x]['use'] = int(i_qty)
                                    break
                except(TypeError, ValueError):
                    sleep(1)
    d_speed[:] = [d for d in d_speed if d.get('use') != 0]
    d_max_queue = d_list[0]['batch']
    for x in range(len(d_speed)):
        if d_max_queue > int(d_speed[x]['qty'] / d_speed[x]['use']):
            d_max_queue = int(d_speed[x]['qty'] / d_speed[x]['use'])
    d_batch = 1 if d_max_queue == 1 else None

    # Set Number Of Batches
    while d_batch is None:
        screen_update(title, lo['C8'])
        ctr_it('{0}: {1} ({2})   {3}: {4}'.format(
            lo['B4'], t(d_mission), cvt_time(d_list[0]['time'], show_seconds=False), lo['C5'], t(d_adventurer)))
        ctr_it(' ')
        d_batch = set_batch(d_max_queue + 1, '{0}'.format(lo['C9']))
        if d_batch == lo['N1'] or d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, lo['69'])
        ctr_it('{0}: {1} ({2})   {3}: {4}'.format(
            lo['B4'], t(d_mission), cvt_time(d_list[0]['time'], show_seconds=False), lo['C5'], t(d_adventurer)))
        ctr_it('{0}: {1:,}'.format(lo['A8'], d_batch))
        d_delay = set_delay()
        if d_delay == lo['N1'] or d_delay == 'exit':
            return

    # Proceed With Farming
    d_proceed = False
    while not d_proceed:
        screen_update(title, lo['70'])
        ctr_it('{0}: {1} ({2})   {3}: {4}'.format(
            lo['B4'], t(d_mission), cvt_time(d_list[0]['time'], show_seconds=False), lo['C5'], t(d_adventurer)))
        ctr_it('{0}: {1:,}   {2}: {3}s'.format(lo['A8'], d_batch, lo['71'], d_delay))
        d_proceed = proceed_run()
        if d_proceed == lo['N1'] or d_proceed == 'exit':
            return

    # Farm Mission
    d_start = time()
    speeds_used, items_gained = [{}, {}]
    for x in range(d_batch):
        job_id = 0
        dur = -1
        for item in d_speed:
            for y in range(item['use']):
                if dur == 0 and y < item['use'] - 1:
                    break
                screen_update(title, lo['73'])
                ctr_it('{0}: {1} ({2})   {3}: {4}'.format(
                    lo['B4'], t(d_mission), cvt_time(d_list[0]['time'], show_seconds=False), lo['C5'], t(d_adventurer)))
                ctr_it('{0}: {1:,}   {2}: {3}s   {4}: {5}'.format(
                    lo['A8'], d_batch, lo['71'], d_delay, lo['74'], cvt_time(time() - d_start)))
                div_line('-')
                if dur == -1:
                    prog(x, d_batch, '{0}: {1}/{2}'.format(lo['A9'], x, d_batch), '{0}'.format(lo['18']))
                else:
                    prog(x + 1, d_batch, '{0}: {1}/{2}'.format(lo['A9'], x + 1, d_batch))
                if speeds_used:
                    ctr_it('~~~ {0} ~~~'.format(lo['D0']), prefix=True)
                    display_it(speeds_used, single=False)
                if items_gained:
                    ctr_it('~~~ {0} ~~~'.format(lo['D1']), prefix=True)
                    display_it(items_gained, single=False)
                if dur == -1:
                    for web_retry in range(5):
                        sleep(d_delay)
                        x_param = 'adventurer_id={0}&mission_type={1}&'.format(d_list[0]['id'], d_mission)
                        try:
                            main_json = web_ops('player_missions', x_param)
                            result = main_json['result']['success']
                            if result:
                                dur = int(main_json['result']['job']['duration'])
                                job_id = main_json['result']['job']['id']
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
                if dur > 1:
                    for web_retry in range(5):
                        sleep(d_delay)
                        x_param = '%5Fmethod=delete&job%5Fid={0}&'.format(job_id)
                        try:
                            item_json = web_ops('player_items/{0}'.format(item['item']), x_param)
                            result = item_json['result']['success']
                            if result:
                                dur = int(item_json['result']['item_response']['run_at'] - item_json['timestamp'])
                                if dur < 0:
                                    dur = 0
                                if t(item['item']) in speeds_used:
                                    speeds_used[t(item['item'])] += 1
                                else:
                                    speeds_used[t(item['item'])] = 1
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
                if dur == 0:
                    for web_retry in range(5):
                        sleep(d_delay)
                        x_param = 'adventurer_id={0}&mission_type={1}&'.format(d_list[0]['id'], d_mission)
                        try:
                            claim_json = web_ops('player_missions/claim_mission', x_param)
                            result = claim_json['result']['success']
                            if result:
                                for z in range(len(claim_json['result']['items'])):
                                    if t(claim_json['result']['items'][z]) in items_gained:
                                        items_gained[t(claim_json['result']['items'][z])] += 1
                                    else:
                                        items_gained[t(claim_json['result']['items'][z])] = 1
                                break
                        except (KeyError, TypeError) as err:
                            print(err)
                            sleep(1)
                            continue
    screen_update(title, lo['82'])
    ctr_it('{0}: {1} ({2})   {3}: {4}'.format(
        lo['B4'], t(d_mission), cvt_time(d_list[0]['time'], show_seconds=False), lo['C5'], t(d_adventurer)))
    ctr_it('{0}: {1:,}   {2}: {3}s'.format(lo['A8'], d_batch, lo['71'], d_delay))
    div_line('-')
    prog(1, 1, '{0} {1}'.format(lo['84'], cvt_time(time() - d_start)))
    if speeds_used:
        ctr_it('~~~ {0} ~~~'.format(lo['D0']), prefix=True)
        display_it(speeds_used, single=False)
    if items_gained:
        ctr_it('~~~ {0} ~~~'.format(lo['D1']), prefix=True)
        display_it(items_gained, single=False)
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue . . ."')
    print(lo['85'])
    get_data(title, pf=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                      CHEST CLASS                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
def open_chest(title):
    # Initialize Chest Opener
    screen_update(title, lo['D2'])
    ctr_it(lo['18'])
    d_list = list()
    selection = {}
    max_len = 0
    for key, value in pData['items'].items():
        if 'ConfigurableChest' in key and value != 0:
            max_use_quantity = 0
            for manifest in range(len(mData['store']['chest'])):
                if key in mData['store']['chest'][manifest]['type']:
                    max_use_quantity = mData['store']['chest'][manifest]['max_use_quantity']
                    break
            max_len = len(str(value)) if max_len < len(str(value)) else max_len
            my_dict = {'chest': key, 'desc': t(key), 'qty': value, 'max_use': max_use_quantity, 'open': False}
            d_list.append(my_dict)

    if not d_list:
        nothing_to_do(title, lo['D2'], lo['D3'])
        return
    else:
        d_list = sorted(d_list, key=itemgetter('desc'))
        # Select Chests
        if len(d_list) == 1:
            d_list[0]['open'] = True
        else:
            a, b, c = [lo['D4'], lo['B6'], lo['D5']]
            a1, b1, c1 = [len(a), len(b), len(c)]
            for x in range(len(d_list)):
                if len(d_list[x]['desc']) > a1:
                    a1 = len(d_list[x]['desc'])
                if len('{0:,}'.format(d_list[x]['qty'])) > b1:
                    b1 = len('{0:,}'.format(d_list[x]['qty']))
                if len('{0}'.format('D6')) > c1:
                    c1 = len('{0}'.format('D6'))
                if len('{0}'.format('D7')) > c1:
                    c1 = len('{0}'.format('D7'))
            while True:
                screen_update(title, '{0}'.format(lo['D2']))
                ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
                ctr_it('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
                selected = False
                for x in range(len(d_list)):
                    d = '{0}'.format(lo['D6']) if d_list[x]['open'] else '{0}'.format(lo['D7'])
                    if d_list[x]['open']:
                        selected = True
                    ctr_it('{0:<{1}}  {2:>{3},}  {4:>{5}}'.format(d_list[x]['desc'], a1, d_list[x]['qty'], b1, d, c1))
                if not selected:
                    print('\n {0}'.format(lo['D8']))
                    print('       {0}'.format(lo['D9']))
                else:
                    print('\n {0}\n'.format(lo['C7']))
                div_line()
                d_select = input(' {0} : '.format(lo['06']))
                if len(d_select) >= 3:
                    if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                        return
                    elif selected and (d_select.lower() == lo['N4'] or d_select.lower() == 'next'):
                        break
                    elif d_select.lower() == lo['N5'] or d_select.lower() == 'all':
                        for x in range(len(d_list)):
                            d_list[x]['open'] = True
                    elif d_select.lower() == lo['N6'] or d_select.lower() == 'none':
                        for x in range(len(d_list)):
                            d_list[x]['open'] = False
                    else:
                        for x in range(len(d_list)):
                            if d_select.lower() == t(d_list[x]['chest']).lower():
                                d_list[x]['open'] = False if d_list[x]['open'] else True
                                break
                        else:
                            for x in range(len(d_list)):
                                if d_select.lower() in t(d_list[x]['chest']).lower():
                                    d_list[x]['open'] = False if d_list[x]['open'] else True
    d_list[:] = [d for d in d_list if d.get('open') == True]
    d_chest = '{0}: {1}'.format(lo['D4'], t(d_list[0]['chest'])) if len(d_list) == 1 else '{0}: {1}'.format(
        lo['E0'], len(d_list))
    d_total, max_chest = [0, 0]
    for x in range(len(d_list)):
        d_total += d_list[x]['qty']
        if max_chest < d_list[x]['qty']:
            max_chest = d_list[x]['qty']
        if max_chest > d_list[x]['max_use']:
            max_chest = d_list[x]['max_use']

    # Set Number Of Batches
    d_batch = None
    while d_batch is None:
        screen_update(title, lo['E1'])
        ctr_it('{0}   {1}: {2:,}'.format(d_chest, lo['E2'], d_total))
        ctr_it(' ')
        d_batch = set_batch(max_chest + 1, '{0}'.format(lo['E3']))
        if d_batch == lo['N1'] or d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, lo['69'])
        ctr_it('{0}   {1}: {2:,}'.format(d_chest, lo['E2'], d_total))
        ctr_it('{0}: {1}'.format(lo['E4'], d_batch))
        d_delay = set_delay()
        if d_delay == lo['N1'] or d_delay == 'exit':
            return

    # Proceed With Run
    d_proceed = False
    while not d_proceed:
        screen_update(title, lo['70'])
        ctr_it('{0}   {1}: {2:,}'.format(d_chest, lo['E2'], d_total))
        ctr_it('{0}: {1}   {2}: {3}s'.format(lo['E4'], d_batch, lo['71'], d_delay))
        d_proceed = proceed_run()
        if d_proceed == lo['N1'] or d_proceed == 'exit':
            return

    # Open Chests
    screen_update(title, lo['73'])
    ctr_it('{0}   {1}: {2:,}'.format(d_chest, lo['E2'], d_total))
    ctr_it('{0}: {1}   {2}: {3}s'.format(lo['E4'], d_batch, lo['71'], d_delay))
    div_line('-')
    prog(0, 1, lo['18'])
    selection.clear()
    d_start = time()
    look_up = pData['items']
    o_received = {'{0}'.format(lo['D4']): {}, '{0}'.format(lo['E5']): {}, '{0}'.format(lo['E6']): {},
                  '{0}'.format(lo['E7']): {}, '{0}'.format(lo['E8']): {}, '{0}'.format(lo['E9']): {}}
    speed_items = ('Hop', 'TranceMarchDrops', 'ForcedMarchDrops', 'TranceMarchElixir', 'Godspeed', 'Bounce', 'Skip',
                   'Jump', 'Leap', 'Bore', 'Bolt', 'Blast', 'Blitz', 'Blink')
    ttl_open = 0
    for x in range(len(d_list)):
        i_received = {'{0}'.format(lo['D4']): {}, '{0}'.format(lo['E5']): {}, '{0}'.format(lo['E6']): {},
                      '{0}'.format(lo['E7']): {}, '{0}'.format(lo['E8']): {}, '{0}'.format(lo['E9']): {}}
        opened = d_list[x]['qty']
        count = 0
        open_qty = d_batch if d_list[x]['max_use'] >= d_batch else d_list[x]['max_use']
        open_qty = d_list[x]['qty'] if d_list[x]['qty'] <= open_qty else open_qty
        while opened != 0:
            if opened < open_qty:
                open_qty = opened
            for web_retry in range(5):
                sleep(d_delay)
                try:
                    x_param = '%5Fmethod=delete&quantity={0}&'.format(open_qty)
                    main_data = web_ops('player_items/{0}'.format(d_list[x]['chest']), x_param)
                    result = main_data['result']['success']
                    if result:
                        opened -= open_qty
                        count += open_qty
                        ttl_open += open_qty
                        for r_key, r_value in main_data['result']['items'].items():
                            if 'Chest' in r_key:
                                if r_key in look_up.keys() and r_value > look_up[r_key]:
                                    i_received['{0}'.format(lo['D4'])][t(r_key)] = r_value - look_up[r_key]
                                if r_key not in look_up.keys():
                                    i_received['{0}'.format(lo['D4'])][t(r_key)] = r_value
                            elif 'TroopPrize' in r_key:
                                if r_key in look_up.keys() and r_value > look_up[r_key]:
                                    i_received['{0}'.format(lo['E5'])][t(r_key)] = r_value - look_up[r_key]
                                if r_key not in look_up.keys():
                                    i_received['{0}'.format(lo['E5'])][t(r_key)] = r_value
                            elif 'Seal' in r_key or 'Grant' in r_key:
                                if r_key in look_up.keys() and r_value > look_up[r_key]:
                                    i_received['{0}'.format(lo['E8'])][t(r_key)] = r_value - look_up[r_key]
                                if r_key not in look_up.keys():
                                    i_received['{0}'.format(lo['E8'])][t(r_key)] = r_value
                            elif 'Testronius' in r_key:
                                if r_key in look_up.keys() and r_value > look_up[r_key]:
                                    i_received['{0}'.format(lo['E7'])][t(r_key)] = r_value - look_up[r_key]
                                if r_key not in look_up.keys():
                                    i_received['{0}'.format(lo['E7'])][t(r_key)] = r_value
                            elif r_key in speed_items:
                                if r_key in look_up.keys() and r_value > look_up[r_key]:
                                    i_received['{0}'.format(lo['E6'])][t(r_key)] = r_value - look_up[r_key]
                                if r_key not in look_up.keys():
                                    i_received['{0}'.format(lo['E6'])][t(r_key)] = r_value
                            else:
                                if r_key in look_up.keys() and r_value > look_up[r_key]:
                                    i_received['{0}'.format(lo['E9'])][t(r_key)] = r_value - look_up[r_key]
                                if r_key not in look_up.keys():
                                    i_received['{0}'.format(lo['E9'])][t(r_key)] = r_value
                        screen_update(title, lo['73'])
                        ctr_it('{0}   {1}: {2:,}'.format(d_chest, lo['E2'], d_total))
                        ctr_it('{0}: {1}   {2}: {3}s   {4}: {5}'.format(
                            lo['E4'], d_batch, lo['71'], d_delay, lo['74'], cvt_time(time() - d_start)))
                        div_line('-')
                        if len(d_list) > 1:
                            prog(ttl_open, d_total, '{0}: {1:,}/{2:,}'.format(lo['F0'], ttl_open, d_total))
                            prog(count, d_list[x]['qty'], '{0}: {1}'.format(lo['F1'], t(d_list[x]['chest'])),
                                 '{0}: {1:,}/{2:,}'.format(lo['F2'], count, d_list[x]['qty']))
                        else:
                            prog(count, d_list[x]['qty'], '{0} {1:,}/{2:,}'.format(lo['F2'], count, d_list[x]['qty']))
                        for category in ('{0}'.format(lo['D4']), '{0}'.format(lo['E5']), '{0}'.format(lo['E6']),
                                         '{0}'.format(lo['E7']), '{0}'.format(lo['E8']), '{0}'.format(lo['E9'])):
                            if len(i_received[category]) > 0:
                                selection = i_received[category]
                                ctr_it('~~~ {0} ~~~'.format(category), prefix=True)
                                display_it(selection, single=False)
                        if count == d_list[x]['qty']:
                            look_up = main_data['result']['items']
                        break
                except (KeyError, TypeError):
                    sleep(1)
                    continue
        for category in ('{0}'.format(lo['D4']), '{0}'.format(lo['E5']), '{0}'.format(lo['E6']), '{0}'.format(lo['E7']),
                         '{0}'.format(lo['E8']), '{0}'.format(lo['E9'])):
            for r_key, r_value in i_received[category].items():
                if r_key in o_received[category].keys():
                    o_received[category][r_key] += r_value
                else:
                    o_received[category][r_key] = r_value
    screen_update(title, lo['82'])
    ctr_it('{0}   {1}: {2:,}'.format(d_chest, lo['E2'], d_total))
    ctr_it('{0}: {1}   {2}: {3}s'.format(lo['E4'], d_batch, lo['71'], d_delay))
    div_line('-')
    prog(1, 1, '{0} {1}'.format(lo['84'], cvt_time(time() - d_start)))
    for category in ('{0}'.format(lo['D4']), '{0}'.format(lo['E5']), '{0}'.format(lo['E6']), '{0}'.format(lo['E7']),
                     '{0}'.format(lo['E8']), '{0}'.format(lo['E9'])):
        if len(o_received[category]) > 0:
            selection = o_received[category]
            ctr_it('~~~ {0} ~~~'.format(category), prefix=True)
            display_it(selection, single=False)
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue . . ."')
    print(lo['85'])
    get_data(title, pf=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def unpack_arsenal(title):
    # Initialize Open Arsenal
    screen_update(title, lo['F3'])
    ctr_it(lo['18'])
    d_list = list()
    selection = {}
    max_use_quantity = 0
    for key, value in sorted(pData['items'].items()):
        for manifest in range(len(mData['store']['arsenal'])):
            if key in mData['store']['arsenal'][manifest]['type']:
                max_use_quantity = mData['store']['arsenal'][manifest]['max_use_quantity']
                break
        if 'TroopPrizeItem' in key and value > 0:
            for x in range(len(mData['units'])):
                if mData['units'][x]['type'] in key:
                    if '50TroopPrizeItem' in key:
                        bin_desc, bin_type = [lo['N7'], 50]
                    elif '500TroopPrizeItem' in key:
                        bin_desc, bin_type = [lo['N8'], 500]
                    elif '1000TroopPrizeItem' in key:
                        bin_desc, bin_type = [lo['N9'], 1000]
                    elif '10kTroopPrizeItem' in key:
                        bin_desc, bin_type = [lo['O0'], 10000]
                    elif '50kTroopPrizeItem' in key:
                        bin_desc, bin_type = [lo['O1'], 50000]
                    else:
                        continue
                    my_dict = {'troop': mData['units'][x]['type'], 'bin': key, 'quantity': value,
                               'power': mData['units'][x]['stats']['power'], 'bin_desc': bin_desc,
                               'bin_type': bin_type, 'max_use': max_use_quantity, 'use': False}
                    d_list.append(my_dict)
    if not d_list:
        nothing_to_do(title, lo['F3'], lo['F4'])
        return
    if len(d_list) == 1:
        d_troop = d_list[0]['troop']
    else:
        d_troop = None
        for x in range(len(d_list)):
            if d_list[x]['troop'] not in selection.keys():
                selection[d_list[x]['troop']] = t(d_list[x]['troop'])
        # Select Troop Type
        while not d_troop:
            screen_update(title, lo['F3'])
            ctr_it('~~~ {0} ~~~'.format(lo['F5']))
            display_it(selection)
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 1:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                else:
                    d_troop = check_input(d_select, selection)
    d_list[:] = [d for d in d_list if d.get('troop') == d_troop]
    if len(d_list) == 1:
        d_list[0]['use'] = True
    else:
        # Select Bins To Open
        a, b, c, d = [lo['63'], lo['B6'], lo['F6'], lo['D5']]
        a1, b1, c1, d1 = [len(a), len(b), len(c), len(d)]
        for x in range(len(d_list)):
            if len('{0}'.format(d_list[x]['bin_desc'])) > a1:
                a1 = len('{0}'.format(d_list[x]['bin_desc']))
            if len('{0:,}'.format(d_list[x]['quantity'])) > b1:
                b1 = len('{0:,}'.format(d_list[x]['quantity']))
            if len('{0:,}'.format(d_list[x]['bin_type'] * d_list[x]['quantity'] * d_list[x]['power'])) > c1:
                c1 = len('{0:,}'.format(d_list[x]['bin_type'] * d_list[x]['quantity'] * d_list[x]['power']))
        selected = False
        while not selected:
            screen_update(title, '{0}'.format(lo['F7']))
            ctr_it('{0}: {1}'.format(lo['F8'], t(d_troop)))
            ctr_it(' ')
            div_line('-')
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}'.format(a, a1, b, b1, c, c1, d, d1))
            ctr_it('{0}  {1}  {2}  {3}'.format('~' * a1, '~' * b1, '~' * c1, '~' * d1))
            gtg = False
            for x in range(len(d_list)):
                e = '{0:,}'.format(d_list[x]['bin_type'] * d_list[x]['quantity'] * d_list[x]['power'])
                if d_list[x]['use']:
                    f = lo['D6']
                    gtg = True
                else:
                    f = lo['D7']
                ctr_it('{0:<{1}}  {2:>{3},}  {4:>{5}}  {6:>{7}}'.format(
                    d_list[x]['bin_desc'], a1, d_list[x]['quantity'], b1, e, c1, f, d1))
            if not gtg:
                print('\n {0}'.format(lo['G0']))
            else:
                print('\n {0}'.format(lo['C7']))
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 3:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                elif d_select.lower() == lo['N5'] or d_select.lower() == 'all':
                    for x in range(len(d_list)):
                        d_list[x]['use'] = True
                elif (d_select.lower() == lo['N4'] or d_select.lower() == 'next') and gtg is True:
                    selected = True
                else:
                    for x in range(len(d_list)):
                        if d_select.lower() == d_list[x]['bin_desc'].lower():
                            d_list[x]['use'] = True if d_list[x]['use'] else False
                    else:
                        for x in range(len(d_list)):
                            if d_select.lower() in d_list[x]['bin_desc'].lower():
                                d_list[x]['use'] = True if d_list[x]['use'] else False
    d_list[:] = [d for d in d_list if d.get('use') == True]
    d_batch = None
    if len(d_list) > 1:
        d_bin_type = '{0} {1}'.format(len(d_list), lo['G1'])
        d_batch = 0
        for x in range(len(d_list)):
            d_batch += d_list[x]['quantity']
    else:
        d_bin_type = '{0:,} {1}'.format(d_list[0]['bin_type'], lo['G1'])

    # Set Number Of Batches
    while d_batch is None:
        screen_update(title, lo['G3'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['F8'], t(d_troop), lo['G4'], d_bin_type))
        ctr_it(' ')
        d_batch = set_batch(d_list[0]['quantity'] + 1, '{0}'.format(lo['G5']))
        if d_batch == lo['N1'] or d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, lo['69'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['F8'], t(d_troop), lo['G4'], d_bin_type))
        ctr_it('{0}: {1:,}'.format(lo['G6'], d_batch))
        d_delay = set_delay()
        if d_delay == lo['N1'] or d_delay == 'exit':
            return

    # Proceed With Run
    d_proceed = False
    while not d_proceed:
        screen_update(title, lo['70'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['F8'], t(d_troop), lo['G4'], d_bin_type))
        ctr_it('{0}: {1:,}   {2}: {3}s'.format(lo['G6'], d_batch, lo['71'], d_delay))
        d_proceed = proceed_run()
        if d_proceed == lo['N1'] or d_proceed == 'exit':
            return

    # Unpack Troop Bins
    screen_update(title, lo['73'])
    ctr_it('{0}: {1}   {2}: {3}'.format(lo['F8'], t(d_troop), lo['G4'], d_bin_type))
    ctr_it('{0}: {1:,}   {2}: {3}s'.format(lo['G6'], d_batch, lo['71'], d_delay))
    div_line('-')
    prog(0, 1, lo['18'])
    d_start = time()
    total_opened = 0
    d_power = 0
    for x in range(len(d_list)):
        current_opened = 0
        if len(d_list) > 1:
            d_quantity = d_list[x]['quantity']
        else:
            d_quantity = d_batch
        open_quantity = d_list[x]['max_use']
        while d_quantity != 0:
            screen_update(title, lo['73'])
            ctr_it('{0}: {1}   {2}: {3}'.format(lo['F8'], t(d_troop), lo['G4'], d_bin_type))
            ctr_it('{0}: {1:,}   {2}: {3}s   {4}: {5}'.format(
                lo['G6'], d_batch, lo['71'], d_delay, lo['74'], cvt_time(time() - d_start)))
            div_line('-')
            prog(total_opened, d_batch, '{0}: {1:,}/{2:,}'.format(lo['G7'], total_opened, d_batch))
            if len(d_list) > 1:
                prog(current_opened, d_list[x]['quantity'], '{0} {1}'.format(lo['G7'], t(d_list[x]['bin'])))
            ctr_it('~~~ {0} ~~~'.format(lo['G8']), prefix=True)
            ctr_it('{0:,}'.format(d_power))
            if d_quantity < open_quantity:
                open_quantity = d_quantity
            for web_retry in range(5):
                sleep(d_delay)
                try:
                    x_param = '%5Fmethod=delete&quantity={0}&'.format(open_quantity)
                    main_json = web_ops('player_items/{0}'.format(d_list[x]['bin']), x_param)
                    result = main_json['result']['success']
                    if result:
                        total_opened += open_quantity
                        current_opened += open_quantity
                        d_quantity -= open_quantity
                        d_power += (open_quantity * d_list[x]['bin_type']) * d_list[x]['power']
                        break
                except (KeyError, TypeError):
                    sleep(1)
                    continue
    screen_update(title, lo['82'])
    ctr_it('{0}: {1}   {2}: {3}'.format(lo['F8'], t(d_troop), lo['G4'], d_bin_type))
    ctr_it('{0}: {1:,}   {2}: {3}s'.format(lo['G6'], d_batch, lo['71'], d_delay))
    div_line('-')
    prog(1, 1, '{0} {1}'.format(lo['84'], cvt_time(time() - d_start)))
    ctr_it('~~~ {0} ~~~'.format(lo['G8']), prefix=True)
    ctr_it('{0:,}'.format(d_power))
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue . . ."')
    print(lo['85'])
    get_data(title, pf=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #


def fill_building(title):
    # Initialize
    screen_update(title, lo['G9'])
    ctr_it(lo['18'])
    d_list, built = [list(), list()]
    selection, capital_buildings = [{}, {}]
    for x in range(len(cData['capital']['city']['buildings'])):
        building = cData['capital']['city']['buildings'][x]
        if building['type'] not in capital_buildings:
            capital_buildings[building['type']] = building['level']
    for key in cData.keys():
        city_busy = False
        built.clear()
        if len(cData[key]['city']['jobs']) != 0:
            for check_jobs in range(len(cData[key]['city']['jobs'])):
                if cData[key]['city']['jobs'][check_jobs]['queue'] == 'building':
                    city_busy = True
                    break
        city_slot, field_slot, c_slot, f_slot = [list(), list(), 0, 0]
        for c_key in range(len(cData[key]['city']['buildings'])):
            city = cData[key]['city']['buildings'][c_key]
            built.append(city['type'])
            if city['location'] in 'city':
                city_slot.append(city['slot'])
            if city['location'] in 'field':
                field_slot.append(city['slot'])
            if key == 'capital' and city['type'] == 'Fortress':
                c_slot = building_dict[key]['c_slots'][city['level']]
                f_slot = building_dict[key]['f_slots'][city['level']]
            if key != 'capital' and 'DragonKeep' in city['type']:
                c_slot = building_dict[key]['c_slots'][city['level']]
                f_slot = building_dict[key]['f_slots'][city['level']]
        if not city_busy:
            for x in range(len(mData['buildings'])):
                manifest = mData['buildings'][x]
                if (manifest['location'] in 'city' and len(city_slot) < c_slot) or (
                                manifest['location'] in 'field' and len(field_slot) < f_slot):
                    if manifest['buildable'] is True and manifest['city_max'][key] != 0:
                        if manifest['per_city'] == 0 or (manifest['per_city'] == 1 and manifest['type'] not in built):
                            for z in range(len(manifest['levels'])):
                                if manifest['levels'][z]['level'] == 1:
                                    level = manifest['levels'][z]
                                    my_dict = {'city': key, 'location': manifest['location'], 'f_slot': field_slot,
                                               'type': t(manifest['type']), 'f_slot_max': f_slot, 'c_slot_max': c_slot,
                                               'levels': level, 'per_city': manifest['per_city'], 'c_slot': city_slot,
                                               'location_id': cData[key]['city']['id'], 'desc': t(key),
                                               'time': manifest['levels'][z]['time']}
                                    d_list.append(my_dict)
    if not d_list:
        nothing_to_do(title, lo['G9'], lo['H0'])
        return
    elif len(d_list) == 1:
        d_location = d_list[0]['city']
    else:
        d_list = sorted(d_list, key=itemgetter('desc'))
        d_location = None
        # Select Location
        a, b, c = [lo['H1'], lo['H2'], lo['H3']]
        a1, b1, c1 = [len(a), len(b), len(c)]
        for x in range(len(d_list)):
            if len(d_list[x]['desc']) > a1:
                a1 = len(d_list[x]['desc'])
        while d_location is None:
            screen_update(title, lo['H4'])
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
            ctr_it('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
            for x in range(len(d_list)):
                d1, d2 = [d_list[x]['c_slot_max'] - len(d_list[x]['c_slot']),
                          d_list[x]['f_slot_max'] - len(d_list[x]['f_slot'])]
                if d_list[x]['city'] not in selection:
                    selection[d_list[x]['city']] = d_list[x]['city']
                    ctr_it('{0:<{1}}  {2:^{3}}  {4:^{5}}'.format(d_list[x]['desc'], a1, d1, b1, d2, c1))
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 2:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                else:
                    for x in range(len(d_list)):
                        if d_select.lower() == d_list[x]['desc'].lower():
                            d_location = d_list[x]['city']
                            break
                    else:
                        for x in range(len(d_list)):
                            if d_select.lower() in d_list[x]['desc'].lower():
                                d_location = d_list[x]['city']
                                break
    d_list[:] = [d for d in d_list if d.get('city') == d_location]
    d_list = sorted(d_list, key=itemgetter('type'))
    if len(d_list) == 1:
        d_building = d_list[0]['type']
    else:
        d_building = None
        # Select Building
        a, b, c = [lo['H5'], lo['B5'], lo['H6']]
        a1, b1, c1 = [len(a), len(b), len(c)]
        for x in range(len(d_list)):
            if len(d_list[x]['type']) > a1:
                a1 = len(d_list[x]['type'])
            if len('{0}'.format(cvt_time(d_list[x]['time']))) > b1:
                b1 = len('{0}'.format(cvt_time(d_list[x]['time'])))
        while d_building is None:
            screen_update(title, lo['H7'])
            ctr_it('{0}: {1}'.format(lo['H1'], t(d_location)))
            ctr_it(' ')
            div_line('-')
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
            ctr_it('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
            for x in range(len(d_list)):
                if d_list[x]['location'] == 'city':
                    d = d_list[x]['c_slot_max'] - len(d_list[x]['c_slot'])
                else:
                    d = d_list[x]['f_slot_max'] - len(d_list[x]['f_slot'])
                ctr_it('{0:<{1}}  {2:>{3}}  {4:^{5}}'.format(
                    d_list[x]['type'], a1, cvt_time(d_list[x]['time']), b1, d, c1))
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 3:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                else:
                    for x in range(len(d_list)):
                        if d_select.lower() == t(d_list[x]['type'].lower()):
                            d_building = d_list[x]['type']
                            break
                    else:
                        for x in range(len(d_list)):
                            if d_select.lower() in t(d_list[x]['type'].lower()):
                                d_building = d_list[x]['type']
                                break
    d_list[:] = [d for d in d_list if d.get('type') == d_building]
    if d_list[0]['location'] == 'city':
        max_slot = d_list[0]['c_slot_max'] - len(d_list[0]['c_slot'])
    else:
        max_slot = d_list[0]['f_slot_max'] - len(d_list[0]['f_slot'])

    # Set Slots If Applicable
    gtg = False
    requirements = {}
    if d_list[0]['per_city'] == 1:
        d_slots = 1
    else:
        d_slots = 0
        while d_slots is 0:
            screen_update(title, lo['H8'])
            ctr_it('{0}: {1}   {2}: {3}'.format(lo['H1'], t(d_location), lo['H5'], t(d_building)))
            ctr_it(' ')
            div_line('-')
            ctr_it('~~~ {0} ~~~'.format(lo['86']))
            ctr_it('1 - {0}'.format(max_slot))
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 1:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                if d_select.isnumeric():
                    if int(d_select) in range(max_slot + 1):
                        d_slots = int(d_select)
        while gtg is False:
            requirements = {'items': {}, 'buildings': {}, 'resources': {}}
            req_check = list()
            req = d_list[0]['levels']['requirements']
            for key in req.keys():
                for c_key, c_value in req[key].items():
                    if c_key in requirements[key]:
                        if key == 'buildings':
                            if requirements[key][c_key] < c_value:
                                requirements[key][c_key] = c_value
                        else:
                            requirements[key][c_key] += c_value * d_slots
                    else:
                        requirements[key][c_key] = c_value * d_slots
            if len(requirements['items']) + len(requirements['buildings']) + len(requirements['resources']) > 0:
                for key in requirements:
                    if key == 'buildings':
                        for c_key, c_value in requirements[key].items():
                            if c_key in capital_buildings.keys():
                                if c_value > capital_buildings[c_key]:
                                    req = '{0} {1} {2} {3}'.format(c_key, c_value, lo['I0'], capital_buildings[c_key])
                                    req_check.append(req)
                            else:
                                req = '{0} {1} {2}'.format(c_key, c_value, lo['I1'])
                                req_check.append(req)
                    if key == 'items':
                        for c_key, c_value in requirements[key].items():
                            if c_key in pData['items']:
                                if pData['items'][c_key] < c_value:
                                    req = '{0:,} {1} {2} {3:,}'.format(c_value, c_key, lo['I2'], pData['items'][c_key])
                                    req_check.append(req)
                            else:
                                req = '{0:,} {1} {2}'.format(c_value, c_key, lo['I3'])
                                req_check.append(req)
                    if key == 'resources':
                        for c_key, c_value in requirements[key].items():
                            if c_key in cData['capital']['city']['resources']:
                                if cData['capital']['city']['resources'][c_key] < c_value:
                                    req = '{0:,} {1} {2} {3:,}'.format(
                                        c_value, c_key, lo['I2'], cData['capital']['city']['resources'][c_key])
                                    req_check.append(req)
                            else:
                                req = '{0:,} {1} {2}'.format(c_value, c_key, lo['I3'])
                                req_check.append(req)
            screen_update(title, lo['H8'])
            ctr_it('{0}: {1}   {2}: {3}'.format(lo['H1'], t(d_location), lo['H5'], t(d_building)))
            ctr_it(' ')
            div_line('-')
            ctr_it('~~~ {0} ~~~'.format(lo['86']))
            ctr_it('1 - {0}'.format(max_slot), suffix=True)
            if len(req_check) != 0:
                for x in range(len(req_check)):
                    ctr_it(req_check[x])
                ctr_it('{0}'.format(lo['H9']), prefix=True, suffix=True)
                div_line()
            if len(req_check) == 0 and d_slots != 0:
                gtg = True
            else:
                d_select = input(' {0} : '.format(lo['06']))
                if len(d_select) >= 1:
                    if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                        return
                    if d_select.isnumeric():
                        if int(d_select) in range(max_slot + 1):
                            d_slots = int(d_select)
                            req_check.clear()

    # Select Speed Items
    selection = list()
    a, b, c, d, e = [lo['80'], lo['C1'], lo['A3'], lo['I4'], lo['C2']]
    a1, b1, c1, d1, e1 = [len(a), len(b), len(c), len(d), len(e)]
    for key in range(len(speed_items_dict)):
        look_up = speed_items_dict[key]
        if look_up['item'] in pData['items'] and pData['items'][look_up['item']] > 0:
            if len(look_up['item']) > a1:
                a1 = len(look_up['item'])
            if len(cvt_time(look_up['time'], show_seconds=False)) > b1:
                b1 = len(cvt_time(look_up['time'], show_seconds=False))
            if len('{0:,}'.format(pData['items'][look_up['item']])) > c1:
                c1 = len('{0:,}'.format(pData['items'][look_up['item']]))
            if len(cvt_time(look_up['exceed'], show_seconds=False)) > d1:
                d1 = len(cvt_time(look_up['exceed'], show_seconds=False))
            my_dict = {'item': look_up['item'], 'exceed': look_up['exceed'], 'time': look_up['time'],
                       'quantity': pData['items'][look_up['item']], 'use': False}
            selection.append(my_dict)
    if selection:
        while True:
            screen_update(title, lo['C4'])
            ctr_it('{0}: {1}   {2}: {3}'.format(lo['H1'], t(d_location), lo['H5'], t(d_building)))
            ctr_it('{0}: {1}'.format(lo['I8'], d_slots))
            div_line('-')
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}  {8:^{9}}'.format(a, a1, b, b1, c, c1, d, d1, e, e1))
            ctr_it('{0}  {1}  {2}  {3}  {4}'.format('~' * a1, '~' * b1, '~' * c1, '~' * d1, '~' * e1))
            for key in range(len(selection)):
                use_item = 'Yes' if selection[key]['use'] is True else 'No'
                ctr_it('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}  {8:>{9}}'.format(
                    selection[key]['item'], a1, cvt_time(selection[key]['time'], show_seconds=False), b1,
                    selection[key]['quantity'], c1, cvt_time(selection[key]['exceed'], show_seconds=False),
                    d1, use_item, e1))
            print('\n {0}'.format(lo['I5']))
            div_line('-')
            print(' {0}:'.format(lo['86']))
            print(' {0}'.format(lo['I6']))
            print(' {0}'.format(lo['I7']))
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 2:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                elif d_select.lower() == lo['N4'] or d_select.lower() == 'next':
                    break
                elif d_select.lower() == lo['N5'] or d_select.lower() == 'all':
                    for key in range(len(selection)):
                        selection[key]['use'] = True
                elif d_select.lower() == lo['N6'] or d_select.lower() == 'none':
                    for key in range(len(selection)):
                        selection[key]['use'] = False
                else:
                    for key in range(len(selection)):
                        if d_select.lower() == selection[key]['item'].lower():
                            selection[key]['use'] = True if selection[key]['use'] is False else False
                            break
                    else:
                        for key in range(len(selection)):
                            if d_select.lower() in selection[key]['item'].lower():
                                selection[key]['use'] = True if selection[key]['use'] is False else False
    d_speed = list()
    for x in range(len(selection)):
        if selection[x]['use'] is True:
            d_speed.append(selection[x])

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, lo['69'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['H1'], t(d_location), lo['H5'], t(d_building)))
        ctr_it('{0}: {1}'.format(lo['I8'], d_slots))
        d_delay = set_delay()
        if d_delay == lo['N1'] or d_delay == 'exit':
            return

    # Proceed With Run
    d_proceed = False
    while not d_proceed:
        screen_update(title, lo['70'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['H1'], t(d_location), lo['H5'], t(d_building)))
        ctr_it('{0}: {1}   {2}: {3}s'.format(lo['I8'], d_slots, lo['71'], d_delay))
        d_proceed = proceed_run()
        if d_proceed == lo['N1'] or d_proceed == 'exit':
            return

    # Run Auto Fill
    screen_update(title, lo['73'])
    ctr_it('{0}: {1}   {2}: {3}'.format(lo['H1'], t(d_location), lo['H5'], t(d_building)))
    ctr_it('{0}: {1}   {2}: {3}s'.format(lo['I8'], d_slots, lo['71'], d_delay))
    div_line('-')
    prog(0, 1, lo['18'])
    d_start = time()
    speeds_used = {}
    slots = list()
    count = 0
    if d_list[0]['location'] == 'city':
        for x in range(d_list[0]['c_slot_max']):
            if x not in d_list[0]['c_slot']:
                slots.append(x)
    else:
        for x in range(d_list[0]['f_slot_max']):
            if x not in d_list[0]['f_slot']:
                slots.append(x)
    for x in range(d_slots):
        jobid = 0
        duration = -1
        while duration != 0:
            screen_update(title, lo['73'])
            ctr_it('{0}: {1}   {2}: {3}'.format(lo['H1'], t(d_location), lo['H5'], t(d_building)))
            ctr_it('{0}: {1}   {2}: {3}s   {4}: {5}'.format(
                lo['I8'], d_slots, lo['71'], d_delay, lo['74'], cvt_time(time() - d_start)))
            div_line('-')
            if speeds_used:
                prog(count, d_slots, '{0}: {1}/{2}'.format(lo['I9'], count, d_slots))
                ctr_it(' ')
                ctr_it('~~~ {0} ~~~'.format(lo['D0']))
                display_it(speeds_used, single=False)
            elif duration != -1:
                prog(count, d_slots, '{0}: {1}/{2}'.format(lo['I9'], count, d_slots),
                     '{0}: {1}'.format(lo['J0'], cvt_time(duration)))
            else:
                prog(count, d_slots, '{0}: {1}/{2}'.format(lo['I9'], count, d_slots), '{0}'.format(lo['18']))
            if duration == -1:
                x_param = 'city%5F{0}%5B{0}%5Ftype%5D={1}&%5Fmethod=post&city%5F{0}%5Bslot%5D={2}&'.format(
                    'building', d_building, slots[x])
                for web_retry in range(5):
                    try:
                        sleep(d_delay)
                        json_data = web_ops('cities/{0}/buildings'.format(
                            d_list[0]['location_id']), x_param)
                        result = json_data['result']['success']
                        if result:
                            duration = json_data['result']['job']['duration']
                            jobid = json_data['result']['job']['id']
                            count += 1
                            break
                    except (KeyError, TypeError):
                        sleep(1)
                        continue
            elif duration != 0 and len(d_speed) > 0:
                speed_item = None
                for y in range(len(d_speed)):
                    if duration > d_speed[y]['exceed']:
                        speed_item = d_speed[y]['item']
                        break
                if speed_item is None:
                    if len(d_speed) == 1:
                        speed_item = d_speed[0]['item']
                    else:
                        for y in range(len(d_speed) + 1, -1, -1):
                            if duration <= d_speed[y]['time']:
                                speed_item = d_speed[y]['item']
                                break
                x_param = '%5Fmethod=delete&job%5Fid={0}&'.format(jobid)
                for web_retry in range(5):
                    try:
                        sleep(d_delay)
                        json_data = web_ops('player_items/{0}'.format(speed_item), x_param)
                        result = json_data['result']['success']
                        if result:
                            if speed_item in speeds_used:
                                speeds_used[speed_item] += 1
                            else:
                                speeds_used[speed_item] = 1
                            duration = int(json_data['result']['item_response']['run_at'] - json_data['timestamp'])
                            if duration < 1:
                                duration = 0
                            break
                    except TypeError:
                        sleep(1)
                        continue
            else:
                duration -= 1
                if duration < 1:
                    duration = 0
                sleep(1)
    screen_update(title, lo['82'])
    ctr_it('{0}: {1}   {2}: {3}'.format(lo['H1'], t(d_location), lo['H5'], t(d_building)))
    ctr_it('{0}: {1}   {2}: {3}s'.format(lo['I8'], d_slots, lo['71'], d_delay))
    div_line('-')
    prog(1, 1, '{0} {1}'.format(lo['84'], cvt_time(time() - d_start)))
    if speeds_used:
        ctr_it('~~~ {0} ~~~'.format(lo['D0']), prefix=True)
        display_it(speeds_used, single=False)
    if len(requirements['items']) >= 1:
        ctr_it('~~~ {0} ~~~'.format(lo['J1']), prefix=True)
        for key, value in requirements['items'].items():
            ctr_it('{0:>}: {1:,}'.format(t(key), value))
    if len(requirements['resources']) >= 1:
        ctr_it('~~~ {0} ~~~'.format(lo['J2']), prefix=True)
        for key, value in requirements['resources'].items():
            ctr_it('{0:>5}: {1:,}'.format(key.title(), value))
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
    print(lo['85'])
    get_data(title, op=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def upgrade_building(title):
    # Initialize
    screen_update(title, lo['H4'])
    ctr_it(lo['18'])
    d_list = list()
    selection, c_bldg = [{}, {}]
    for x in range(len(cData['capital']['city']['buildings'])):
        if cData['capital']['city']['buildings'][x]['type'] not in c_bldg:
            c_bldg[cData['capital']['city']['buildings'][x]['type']] = cData['capital']['city']['buildings'][x]['level']
    for key in cData.keys():
        city_busy = False
        if len(cData[key]['city']['jobs']) != 0:
            for check_jobs in range(len(cData[key]['city']['jobs'])):
                if cData[key]['city']['jobs'][check_jobs]['queue'] == 'building':
                    city_busy = True
                    break
        if not city_busy:
            for x in range(len(cData[key]['city']['buildings'])):
                city = cData[key]['city']['buildings'][x]
                for y in range(len(mData['buildings'])):
                    manifest = mData['buildings'][y]
                    levels = list()
                    if city['type'] == manifest['type'] and city['level'] < manifest['city_max'][key]:
                        for z in range(city['level'] + 1, manifest['city_max'][key] + 1):
                            for lvl in range(len(manifest['levels'])):
                                if z == manifest['levels'][lvl]['level']:
                                    levels.append(manifest['levels'][lvl])
                        my_dict = {'city': key, 'max_level': manifest['city_max'][key], 'building_id': city['id'],
                                   'type': city['type'], 'level': city['level'], 'levels': levels,
                                   'location_id': cData[key]['city']['id'], 'desc': t(key)}
                        d_list.append(my_dict)
                        break
    if not d_list:
        nothing_to_do(title, lo['H4'], lo['J4'])
        return
    if len(d_list) == 1:
        d_lct = d_list[0]['city']
    else:
        d_lct = None
        for x in range(len(d_list)):
            if d_list[x]['city'] not in selection.keys():
                selection[d_list[x]['city']] = t(d_list[x]['city'])
        # Select Location
        while d_lct is None:
            screen_update(title, lo['J4'])
            ctr_it('~~~ {0} ~~~'.format(lo['J3']))
            display_it(selection)
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 3:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                else:
                    d_lct = check_input(d_select, selection)
    d_list[:] = [d for d in d_list if d.get('city') == d_lct]
    selection.clear()
    if len(d_list) == 1:
        d_bldg = d_list[0]['type']
    else:
        for x in range(len(d_list)):
            if d_list[x]['type'] not in selection:
                selection[d_list[x]['type']] = t(d_list[x]['type'])
        # Select Building
        d_bldg = None
        while d_bldg is None:
            screen_update(title, lo['H7'])
            ctr_it('{0}: {1}'.format(lo['H1'], t(d_lct)))
            ctr_it(' ')
            div_line('-')
            ctr_it('~~~ {0} ~~~'.format(lo['J5']))
            display_it(selection)
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 3:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                else:
                    d_bldg = check_input(d_select, selection)
    d_list[:] = [d for d in d_list if d.get('type') == d_bldg]
    max_level = d_list[0]['max_level']
    min_lvl = max_level
    for x in range(len(d_list)):
        if d_list[x]['level'] < min_lvl:
            min_lvl = d_list[x]['level']
    # Select Level
    gtg = False
    d_lvl = 0
    requirements = {}
    while d_lvl is 0:
        screen_update(title, lo['J6'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['H1'], t(d_lct), lo['H5'], t(d_bldg)))
        ctr_it(' ')
        div_line('-')
        ctr_it('{0}'.format(lo['J7']), prefix=True)
        ctr_it('{0} - {1}'.format(min_lvl + 1, max_level), suffix=True)
        div_line()
        d_select = input(' {0} : '.format(lo['06']))
        if len(d_select) >= 1:
            if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                return
            if d_select.isnumeric():
                if int(d_select) in range(min_lvl + 1, max_level + 1):
                    d_lvl = int(d_select)
    while gtg is False:
        requirements = {'items': {}, 'buildings': {}, 'research': {}, 'resources': {}}
        req_check = list()
        for x in range(len(d_list)):
            for y in range(len(d_list[x]['levels'])):
                if d_list[x]['levels'][y]['level'] <= d_lvl:
                    req = d_list[x]['levels'][y]['requirements']
                    for key in req.keys():
                        for c_key, c_value in req[key].items():
                            if c_key in requirements[key]:
                                if key == 'buildings':
                                    if requirements[key][c_key] < c_value:
                                        requirements[key][c_key] = c_value
                                else:
                                    requirements[key][c_key] += c_value
                            else:
                                requirements[key][c_key] = c_value
        if len(requirements['items']) + len(requirements['buildings']) + len(requirements['resources']) > 0:
            for key in requirements:
                if key == 'buildings':
                    for c_key, c_value in requirements[key].items():
                        for x in range(len(cData[d_lct]['city']['buildings'])):
                            if c_key == cData[d_lct]['city']['buildings'][x]['type']:
                                if c_value > cData[d_lct]['city']['buildings'][x]['level']:
                                    req = '{0} {1} {2} {3}'.format(
                                            t(c_key), c_value, lo['I0'], cData[d_lct]['city']['buildings'][x]['level'])
                                    req_check.append(req)
                                break
                        else:
                            if c_key in c_bldg.keys():
                                if c_value > c_bldg[c_key]:
                                    req = '{0} {1} {2} {3}'.format(t(c_key), c_value, lo['I0'], c_bldg[c_key])
                                    req_check.append(req)
                            else:
                                req = '{0} {1} {2}'.format(t(c_key), c_value, lo['I1'])
                                req_check.append(req)
                if key == 'items':
                    for c_key, c_value in requirements[key].items():
                        if c_key in pData['items']:
                            if pData['items'][c_key] < c_value:
                                req = '{0:,} {1} {2} {3:,}'.format(
                                    c_value, c_key, lo['I2'], pData['items'][c_key])
                                req_check.append(req)
                        else:
                            req = '{0:,} {1} {2}'.format(c_value, c_key, lo['I3'])
                            req_check.append(req)
                if key == 'research':
                    for c_key, c_value in requirements[key].items():
                        if c_key in pData['research']:
                            if pData['research'][c_key] < c_value:
                                req = '{1} {0} {2} {3}'.format(c_value, c_key, lo['I0'], pData['research'][c_key])
                                req_check.append(req)
                        else:
                            req = '{1} {0} {2} {1}'.format(c_value, c_key, lo['J8'])
                            req_check.append(req)
                if key == 'resources':
                    for c_key, c_value in requirements[key].items():
                        if c_key in cData['capital']['city']['resources']:
                            if cData['capital']['city']['resources'][c_key] < c_value:
                                req = '{0:,} {1} {2} {3:,}'.format(
                                    c_value, c_key, lo['I2'], cData['capital']['city']['resources'][c_key])
                                req_check.append(req)
        screen_update(title, lo['J6'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['H1'], t(d_lct), lo['H5'], t(d_bldg)))
        ctr_it(' ')
        div_line('-')
        ctr_it(lo['J7'], prefix=True)
        ctr_it('{0} - {1}'.format(min_lvl + 1, max_level), suffix=True)
        if len(req_check) != 0:
            div_line('#')
            ctr_it(lo['H9'], suffix=True)
            for x in range(len(req_check)):
                ctr_it(req_check[x])
            div_line('#')
        if len(req_check) == 0 and d_lvl != 0:
            gtg = True
        else:
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 1:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                if d_select.isnumeric():
                    if int(d_select) in range(min_lvl + 1, max_level + 1):
                        d_lvl = int(d_select)
                        max_level = int(d_select) - 1
                        req_check.clear()
    # Select Speed Items
    selection = list()
    a, b, c, d, e = [lo['80'], lo['C1'], lo['A3'], lo['I4'], lo['C2']]
    a1, b1, c1, d1, e1 = [len(a), len(b), len(c), len(d), len(e)]
    for key in range(len(speed_items_dict)):
        look_up = speed_items_dict[key]
        if look_up['item'] in pData['items'] and pData['items'][look_up['item']] > 0:
            if len(look_up['item']) > a1:
                a1 = len(look_up['item'])
            if len(cvt_time(look_up['time'], show_seconds=False)) > b1:
                b1 = len(cvt_time(look_up['time'], show_seconds=False))
            if len('{0:,}'.format(pData['items'][look_up['item']])) > c1:
                c1 = len('{0:,}'.format(pData['items'][look_up['item']]))
            if len(cvt_time(look_up['exceed'], show_seconds=False)) > d1:
                d1 = len(cvt_time(look_up['exceed'], show_seconds=False))
            my_dict = {'item': look_up['item'], 'exceed': look_up['exceed'], 'time': look_up['time'],
                       'quantity': pData['items'][look_up['item']], 'use': False}
            selection.append(my_dict)
    if selection:
        while True:
            screen_update(title, lo['C4'])
            ctr_it('{0}: {1}   {2}: {3}   {4}: {5}'.format(
                lo['H1'], t(d_lct), lo['H5'], t(d_bldg), lo['J9'], d_lvl))
            ctr_it(' ')
            div_line('-')
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}  {8:^{9}}'.format(a, a1, b, b1, c, c1, d, d1, e, e1))
            ctr_it('{0}  {1}  {2}  {3}  {4}'.format('~' * a1, '~' * b1, '~' * c1, '~' * d1, '~' * e1))
            for x in range(len(selection)):
                use_item = lo['D6'] if selection[x]['use'] is True else lo['D7']
                ctr_it('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}  {8:>3}'.format(
                        selection[x]['item'], a1, cvt_time(selection[x]['time'], show_seconds=False), b1,
                        selection[x]['quantity'], c1, cvt_time(selection[x]['exceed'], show_seconds=False),
                    d1, use_item))
            print('\n {0}'.format(lo['I5']))
            div_line('-')
            print(' {0}:'.format(lo['86']))
            print(' {0}'.format(lo['I6']))
            print(' {0}'.format(lo['I7']))
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 2:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                elif d_select.lower() == lo['N4'] or d_select.lower() == 'next':
                    break
                elif d_select.lower() == lo['N5'] or d_select.lower() == 'all':
                    for x in range(len(selection)):
                        selection[x]['use'] = True
                elif d_select.lower() == lo['N6'] or d_select.lower() == 'none':
                    for x in range(len(selection)):
                        selection[x]['use'] = False
                else:
                    for x in range(len(selection)):
                        if d_select.lower() == selection[x]['item'].lower():
                            selection[x]['use'] = True if not selection[x]['use'] else False
                            break
                    else:
                        for x in range(len(selection)):
                            if d_select.lower() in selection[x]['item'].lower():
                                selection[x]['use'] = True if not selection[x]['use'] else False
    d_speed = list()
    for x in range(len(selection)):
        if selection[x]['use'] is True:
            d_speed.append(selection[x])
    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, lo['69'])
        ctr_it('{0}: {1}   {2}: {3}   {4}: {5}'.format(lo['H1'], t(d_lct), lo['H5'], t(d_bldg), lo['J9'], d_lvl))
        ctr_it(' ')
        d_delay = set_delay()
        if d_delay == lo['N1'] or d_delay == 'exit':
            return

    # Proceed With Run
    d_proceed = False
    while not d_proceed:
        screen_update(title, lo['70'])
        ctr_it('{0}: {1}   {2}: {3}   {4}: {5}'.format(lo['H1'], t(d_lct), lo['H5'], t(d_bldg), lo['J9'], d_lvl))
        ctr_it('{0}: {1}s'.format(lo['71'], d_delay))
        d_proceed = proceed_run()
        if d_proceed == lo['N1'] or d_proceed == 'exit':
            return

    # Run Auto Upgrade
    screen_update(title, lo['73'])
    ctr_it('{0}: {1}   {2}: {3}   {4}: {5}'.format(lo['H1'], t(d_lct), lo['H5'], t(d_bldg), lo['J9'], d_lvl))
    ctr_it('{0}: {1}s'.format(lo['71'], d_delay))
    div_line('-')
    prog(0, 1, lo['18'])
    d_start = time()
    speeds_used = {}
    d_list_len = len(d_list)
    for y in range(min_lvl, d_lvl):
        total = len([d for d in d_list if d.get('level') == y])
        count = 0
        for x in range(d_list_len):
            if d_list[x]['level'] == y:
                jobid = 0
                duration = -1
                speed_item = None
                while duration != 0:
                    screen_update(title, lo['73'])
                    ctr_it('{0}: {1}   {2}: {3}   {4}: {5}'.format(
                        lo['H1'], t(d_lct), lo['H5'], t(d_bldg), lo['J9'], d_lvl))
                    ctr_it('{0}: {1}s   {2}: {3}'.format(lo['71'], d_delay, lo['74'], cvt_time(time() - d_start)))
                    div_line('-')
                    if (d_lvl - min_lvl) > 1:
                        prog((d_lvl - min_lvl) - (d_lvl - y) + 1, d_lvl - min_lvl, '{0} {1}'.format(lo['K0'], y))
                    if total > 1:
                        prog(count, total, '{0}: {1}/{2}'.format(lo['K1'], count, total))
                    elif speed_item:
                        prog(prog_dur - duration, prog_dur, '{0} {1}'.format(lo['K2'], speed_item))
                    else:
                        pass
                    if speeds_used:
                        ctr_it('~~~ {0} ~~~'.format(lo['D0']), prefix=True)
                        display_it(speeds_used, single=False)
                    if duration == -1:
                        x_param = '%5Fmethod=put&'
                        for server_retry in range(5):
                            sleep(d_delay + 1)
                            try:
                                main_json = web_ops('cities/{0}/buildings/{1}'.format(
                                    d_list[x]['location_id'], d_list[x]['building_id']), x_param)
                                result = main_json['result']['success']
                                if result:
                                    duration = int(main_json['result']['job']['duration'])
                                    prog_dur = duration
                                    jobid = main_json['result']['job']['id']
                                    count += 1
                                    break
                            except (KeyError, TypeError):
                                sleep(1)
                                continue
                    elif duration > 0 and len(d_speed) > 0:
                        speed_item = None
                        for z in range(len(d_speed)):
                            if duration > d_speed[z]['exceed'] and d_speed[z]['quantity'] != 0:
                                speed_item = d_speed[z]['item']
                                break
                        if speed_item is None:
                            if len(d_speed) == 1 and d_speed[0]['quantity'] != 0:
                                speed_item = d_speed[0]['item']
                            else:
                                for z in range(len(d_speed) - 1, -1, -1):
                                    if duration <= d_speed[z]['time'] and d_speed[z]['quantity'] != 0:
                                        speed_item = d_speed[z]['item']
                                        break
                        x_param = '%5Fmethod=delete&job%5Fid={0}&'.format(jobid)
                        for server_retry in range(5):
                            sleep(d_delay + 1)
                            try:
                                item_json = web_ops('player_items/{0}'.format(speed_item), x_param)
                                result = item_json['result']['success']
                                if result:
                                    for z in range(len(d_speed)):
                                        if speed_item == d_speed[z]['item']:
                                            d_speed[z]['quantity'] -= 1
                                    if speed_item in speeds_used:
                                        speeds_used[speed_item] += 1
                                    else:
                                        speeds_used[speed_item] = 1
                                    duration = int(
                                        item_json['result']['item_response']['run_at'] - item_json['timestamp'])
                                    if duration < 1:
                                        duration = 0
                                        d_list[x]['level'] = item_json['result']['item_response']['level']
                                    break
                            except (KeyError, TypeError):
                                sleep(1)
                                continue
                    else:
                        duration -= 1
                        if duration < 1:
                            duration = 0
                            d_list[x]['level'] += 1
                        sleep(1)
    screen_update(title, lo['82'])
    ctr_it('{0}: {1}   {2}: {3}   {4}: {5}'.format(lo['H1'], t(d_lct), lo['H5'], t(d_bldg), lo['J9'], d_lvl))
    ctr_it('{0}: {1}s'.format(lo['71'], d_delay))
    div_line('-')
    prog(1, 1, '{0} {1}'.format(lo['84'], cvt_time(time() - d_start)))
    if speeds_used:
        ctr_it('~~~ {0} ~~~'.format(lo['D0']), prefix=True)
        display_it(speeds_used, single=False)
    if len(requirements['items']) >= 1:
        ctr_it('~~~ {0} ~~~'.format(lo['J1']), prefix=True)
        for key, value in requirements['items'].items():
            ctr_it('{0:>}: {1:,}'.format(t(key), value))
    if len(requirements['resources']) >= 1:
        ctr_it('~~~ {0} ~~~'.format(lo['J2']), prefix=True)
        for key, value in requirements['resources'].items():
            ctr_it('{0:>5}: {1:,}'.format(key.title(), value))
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
    print(lo['85'])
    get_data(title, op=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def train_troop(title):
    # Initialize
    low_req = None
    while low_req is None:
        screen_update(title, lo['K3'])
        ctr_it(lo['P2'], prefix=True, suffix=True)
        ctr_it('~~~ {0} ~~~'.format(lo['86']))
        ctr_it(lo['90'])
        div_line()
        d_select = input(' {0} : '.format(lo['06']))
        if len(d_select) >= 1:
            if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                break
            if d_select.isalpha():
                if d_select.lower() == lo['D6'].lower() or d_select.lower() == 'yes':
                    low_req = True
                elif d_select.lower() == lo['D7'].lower() or d_select.lower() == 'no':
                    low_req = False
    screen_update(title, lo['K3'])
    ctr_it(lo['18'])
    d_list = list()
    selection = {}
    pseudo_tc = ('Garrison', 'TrainingCamp', 'CaveTrainingCamp')
    for x in cData:
        tc_level, tc_total, tc_combo = [0, 0, 0]
        for y in range(len(cData[x]['city']['buildings'])):
            if cData[x]['city']['buildings'][y]['type'] in pseudo_tc:
                tc_level = cData[x]['city']['buildings'][y]['level'] if tc_level < cData[x]['city']['buildings'][y][
                    'level'] else tc_level
                tc_total += 1
                tc_combo += cData[x]['city']['buildings'][y]['level']
        my_dict = {'tc_level': tc_level, 'tc_combo': tc_combo, 'tc_total': tc_total}
        selection[x] = my_dict
    d_rookery = 0
    for x in range(len(mData['units'])):
        if mData['units'][x]['trainable_in']:
            d_max_queue, d_pop = [-1, -1]
            met_rsch, met_rsc, met_item, met_unit, met_idle, met_bldg = [True, True, True, True, True, True]
            d_unit = mData['units'][x]
            d_req = d_unit['requirements']['capital']
            if 'research' in d_req.keys():
                met_req = len(d_req['research'])
                for key, value in d_req['research'].items():
                    if key in pData['research']:
                        if value <= pData['research'][key]:
                            met_req -= 1
                met_rsch = True if met_req == 0 else False
            if 'resources' in d_req.keys():
                met_req = len(d_req['resources'])
                lookup = cData['capital']['city']['resources']
                for key, value in d_req['resources'].items():
                    if key == 'blue_energy' and low_req:
                        value = 1
                    if key in lookup:
                        if value <= lookup[key]:
                            met_req -= 1
                            if value != 0:
                                if d_max_queue > int(lookup[key] / value) or d_max_queue == -1:
                                    d_max_queue = int(lookup[key] / value)
                met_rsc = True if met_req == 0 else False
            if 'items' in d_req.keys():
                if low_req:
                    met_item = True
                else:
                    met_req = len(d_req['items'])
                    lookup = pData['items']
                    for key, value in d_req['items'].items():
                        if key in lookup:
                            if value <= lookup[key]:
                                met_req -= 1
                                if value != 0:
                                    if d_max_queue > int(lookup[key] / value) or d_max_queue == -1:
                                        d_max_queue = int(lookup[key] / value)
                    met_item = True if met_req == 0 else False
            if 'units' in d_req.keys():
                met_req = len(d_req['units'])
                lookup = cData['capital']['city']['units']
                for key, value in d_req['units'].items():
                    if key in lookup:
                        if value <= lookup[key]:
                            met_req -= 1
                            if value != 0:
                                if d_max_queue > int(lookup[key] / value) or d_max_queue == -1:
                                    d_max_queue = int(lookup[key] / value)
                met_unit = True if met_req == 0 else False
            if 'population' in d_req.keys():
                lookup = cData['capital']['city']['figures']['population']
                if d_req['population']['idle'] <= lookup['current'] - (lookup['laborers'] + lookup['armed_forces']) - 1:
                    met_idle = True
                    d_pop = int((lookup['current'] - (lookup['laborers'] + lookup['armed_forces']) - 1) /
                                d_req['population']['idle'])
                else:
                    met_idle = False
            if 'buildings' in d_req.keys():
                met_req = len(d_req['buildings'])
                lookup = cData['capital']['city']['buildings']
                for key, value in d_req['buildings'].items():
                    if key in pseudo_tc:
                        met_req -= 1
                    else:
                        for y in range(len(lookup)):
                            if key == lookup[y]['type'] and value <= lookup[y]['level']:
                                met_req -= 1
                                d_rookery = lookup[y]['level'] if key == 'Rookery' else 0
                                break
                met_bldg = True if met_req == 0 else False
            if met_rsch and met_rsc and met_item and met_unit and met_idle and met_bldg:
                for d_loc in mData['units'][x]['trainable_in']:
                    if 'buildings' in d_req.keys():
                        for key, value in d_req['buildings'].items():
                            if key in pseudo_tc and value <= selection[d_loc]['tc_level']:
                                multiplier = selection[d_loc]['tc_total'] + \
                                             ((selection[d_loc]['tc_combo'] - selection[d_loc]['tc_total']) / 10)
                                if mData['units'][x]['type'] in ('BattleDragon', 'SwiftStrikeDragon') \
                                        and d_loc == 'capital':
                                    multiplier += (multiplier / 100) * d_rookery
                                if d_pop > d_max_queue:
                                    d_pop = d_max_queue
                                my_dict = {'troop': mData['units'][x]['type'], 'id': cData[d_loc]['city']['id'],
                                           'tc_level': selection[d_loc]['tc_level'], 'quantity': d_pop,
                                           'tc_total': selection[d_loc]['tc_total'], 'trainable': d_max_queue,
                                           'time': mData['units'][x]['time'], 'multiplier': multiplier,
                                           'power': mData['units'][x]['stats']['power'], 'location': d_loc,
                                           'desc': t(mData['units'][x]['type']), 'loc_desc': t(d_loc)}
                                d_list.append(my_dict)
                                break
    d_list = sorted(d_list, key=itemgetter('desc'))
    selection.clear()
    if not d_list:
        nothing_to_do(title, lo['K3'], lo['K4'])
        return
    elif len(d_list) == 1:
        d_troop = d_list[0]['troop']
    else:
        a, b, c = [lo['61'], lo['K5'], lo['F6']]
        a1, b1, c1 = [len(a), len(b), len(c)]
        for x in range(len(d_list)):
            if len(d_list[x]['desc']) > a1:
                a1 = len(d_list[x]['desc'])
            if len('{0:,}'.format(d_list[x]['trainable'])) > b1:
                b1 = len('{0:,}'.format(d_list[x]['trainable']))
            if len('{0:,}'.format(d_list[x]['trainable'] * d_list[x]['power'])) > c1:
                c1 = len('{0:,}'.format(d_list[x]['trainable'] * d_list[x]['power']))
        # Select Troop To Train
        d_troop = None
        while d_troop is None:
            screen_update(title, lo['K3'])
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
            ctr_it('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
            for x in range(len(d_list)):
                if d_list[x]['troop'] not in selection:
                    selection[d_list[x]['troop']] = d_list[x]['desc']
                    ctr_it('{0:<{1}}  {2:>{3},}  {4:>{5},}'.format(
                        d_list[x]['desc'], a1, d_list[x]['trainable'], b1,
                        d_list[x]['trainable'] * d_list[x]['power'],
                        c1))
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 3:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                else:
                    d_troop = check_input(d_select, selection)
    d_list[:] = [d for d in d_list if d.get('troop') == d_troop]
    selection.clear()
    if len(d_list) == 1:
        d_location = d_list[0]['location']
    else:
        d_location = None
        d_list = sorted(d_list, key=itemgetter('loc_desc'))
        # Select Location To Train
        a, b, c, d = [lo['H1'], lo['K6'], lo['K7'], lo['B5']]
        a1, b1, c1, d1 = [len(a), len(b), len(c), len(d)]
        for x in range(len(d_list)):
            if len(d_list[x]['loc_desc']) > a1:
                a1 = len(d_list[x]['loc_desc'])
            if len('{0}'.format(d_list[x]['tc_level'])) > b1:
                b1 = len('{0}'.format(d_list[x]['tc_level']))
            if len('{0}'.format(d_list[x]['tc_total'])) > c1:
                c1 = len('{0}'.format(d_list[x]['tc_total']))
            if len(cvt_time(d_list[x]['time'] / d_list[x]['multiplier'])) > d1:
                d1 = len(cvt_time(d_list[x]['time'] / d_list[x]['multiplier']))
        while d_location is None:
            screen_update(title, lo['H4'])
            ctr_it('{0}: {1}'.format(lo['61'], t(d_troop)))
            ctr_it(' ')
            div_line('-')
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}'.format(a, a1, b, b1, c, c1, d, d1))
            ctr_it('{0}  {1}  {2}  {3}'.format('~' * a1, '~' * b1, '~' * c1, '~' * d1))
            for x in range(len(d_list)):
                ctr_it('{0:<{1}}  {2:^{3}}  {4:^{5}}  {6:>{7}}'.format(
                    d_list[x]['loc_desc'], a1, d_list[x]['tc_level'], b1, d_list[x]['tc_total'], c1,
                    cvt_time(d_list[x]['time'] / d_list[x]['multiplier']), d1))
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 3:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                else:
                    for x in range(len(d_list)):
                        if d_select.lower() == d_list[x]['loc_desc'].lower():
                            d_location = d_list[x]['location']
                            break
                    else:
                        for x in range(len(d_list)):
                            if d_select.lower() in d_list[x]['loc_desc'].lower():
                                d_location = d_list[x]['location']
                                break
    d_list[:] = [d for d in d_list if d.get('location') == d_location]
    d_max_queue = 1 if d_list[0]['quantity'] == 1 else 0
    # Set Training Queue Size
    while d_max_queue is 0:
        screen_update(title, lo['K8'])
        ctr_it('{0}: {1}   {2}: {3}'.format(lo['61'], t(d_troop), lo['H1'], t(d_location)))
        ctr_it(' ')
        div_line('-')
        ctr_it('~~~ {0} ~~~'.format(lo['86']))
        ctr_it('1 - {0}'.format(d_list[0]['quantity']), suffix=True)
        print(' {0}'.format(lo['K9']))
        div_line()
        d_select = input(' {0} : '.format(lo['06']))
        if len(d_select) >= 1:
            if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                return
            elif d_select.lower() == lo['O3'] or d_select.lower() == 'max':
                d_max_queue = d_list[0]['quantity']
            elif d_select.isnumeric():
                if int(d_select) in range(1, d_list[0]['quantity'] + 1):
                    d_max_queue = int(d_select)
    d_list[0]['quantity'] = d_max_queue
    selection.clear()

    # Set Speed Items
    a, b, c, d = [lo['L0'], lo['C1'], lo['A3'], lo['C2']]
    a1, b1, c1, d1 = [len(a), len(b), len(c), len(d)]
    selection = [{'item': 'TestroniusInfusion', 'time': 0.99}, {'item': 'TestroniusDeluxe', 'time': 0.5},
                 {'item': 'TestroniusPowder', 'time': 0.3}, {'item': 'Blitz', 'time': 345600},
                 {'item': 'Blast', 'time': 216000}, {'item': 'Bolt', 'time': 86400}, {'item': 'Bore', 'time': 54000},
                 {'item': 'Bounce', 'time': 28800}, {'item': 'Leap', 'time': 9000}, {'item': 'Jump', 'time': 3600},
                 {'item': 'Skip', 'time': 900}, {'item': 'Hop', 'time': 300}, {'item': 'Blink', 'time': 60}]
    d_speed = list()
    for x in range(len(selection)):
        if selection[x]['item'] in pData['items']:
            if pData['items'][selection[x]['item']] > 0:
                if selection[x]['time'] < 1:
                    y = '{0}% {1}'.format(int(selection[x]['time'] * 100), lo['O2'])
                else:
                    y = '{0}'.format(cvt_time(selection[x]['time'], show_seconds=False))
                my_dict = {'item': selection[x]['item'], 'qty': pData['items'][selection[x]['item']],
                           'time': selection[x]['time'], 'desc': y, 'use': 0}
                d_speed.append(my_dict)
                if len(t(selection[x]['item'])) > a1:
                    a1 = len(t(selection[x]['item']))
                if len(y) > b1:
                    b1 = len(y)
                z = '{0:,}'.format(pData['items'][selection[x]['item']])
                if len(z) > c1:
                    c1 = len(str(pData['items'][selection[x]['item']]))
    while True:
        screen_update(title, lo['L1'])
        ctr_it('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
            lo['61'], t(d_troop), lo['H1'], t(d_location), lo['L2'], d_list[0]['quantity']))
        ctr_it(' ')
        div_line('-')
        ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}'.format(a, a1, b, b1, c, c1, d, d1))
        ctr_it('{0}  {1}  {2}  {3}'.format('-' * a1, '-' * b1, '-' * c1, '-' * d1))
        reduced_time = (d_list[0]['time'] / d_list[0]['multiplier']) * d_list[0]['quantity']
        for x in range(len(d_speed)):
            ctr_it('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}'.format(
                t(d_speed[x]['item']), a1, d_speed[x]['desc'], b1, d_speed[x]['qty'], c1,
                d_speed[x]['use'], d1))
            if d_speed[x]['use'] != 0:
                if d_speed[x]['time'] < 1:
                    for y in range(d_speed[x]['use']):
                        reduced_time *= (1 - d_speed[x]['time'])
                else:
                    for y in range(d_speed[x]['use']):
                        reduced_time -= d_speed[x]['time']
        else:
            reduced_time = 0 if reduced_time < 1 else cvt_time(reduced_time)
            ctr_it('{0}: {1}'.format(lo['L3'], reduced_time), prefix=True, suffix=True)
        if reduced_time != 0:
            print(' {0}'.format(lo['C6']))
        else:
            print(' {0}'.format(lo['C7']))
        div_line()
        d_select = input(' {0} : '.format(lo['06']))
        if len(d_select) >= 3:
            if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                return
            elif (d_select.lower() == lo['N4'] or d_select.lower() == 'next') and reduced_time == 0:
                break
            else:
                try:
                    i_item, i_qty = d_select.split('@')
                    if i_qty.isnumeric():
                        for x in range(len(d_speed)):
                            if i_item.lower() == t(d_speed[x]['item']).lower() and int(i_qty) <= d_speed[x]['qty']:
                                d_speed[x]['use'] = int(i_qty)
                                break
                        else:
                            for x in range(len(d_speed)):
                                if i_item.lower() in t(d_speed[x]['item']).lower() and int(i_qty) <= d_speed[x]['qty']:
                                    d_speed[x]['use'] = int(i_qty)
                                    break
                except(TypeError, ValueError):
                    pass
    d_speed[:] = [d for d in d_speed if d.get('use') != 0]
    d_max_queue = int(d_list[0]['trainable'] / d_list[0]['quantity'])
    speed_cut_off = 0
    for x in range(len(d_speed)):
        if d_max_queue > (d_speed[x]['qty'] / d_speed[x]['use']):
            d_max_queue = int(d_speed[x]['qty'] / d_speed[x]['use'])
        if 'Testronius' not in d_speed[x]['item']:
            speed_cut_off += d_speed[x]['time']
    d_batch = 1 if d_max_queue == 1 else None

    # Set Number Of Batches
    while d_batch is None:
        screen_update(title, lo['L4'])
        ctr_it('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
            lo['61'], t(d_troop), lo['H1'], t(d_location), lo['L2'], d_list[0]['quantity']))
        ctr_it(' ')
        d_batch = set_batch(d_max_queue + 1, '{0}'.format(lo['L5']))
        if d_batch == lo['N1'] or d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, lo['69'])
        ctr_it('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
            lo['61'], t(d_troop), lo['H1'], t(d_location), lo['L2'], d_list[0]['quantity']))
        ctr_it('{0}: {1:,}'.format(lo['L6'], d_batch))
        d_delay = set_delay()
        if d_delay == lo['N1'] or d_delay == 'exit':
            return

    # Proceed With Run
    d_proceed = False
    while not d_proceed:
        screen_update(title, lo['70'])
        ctr_it('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
            lo['61'], t(d_troop), lo['H1'], t(d_location), lo['L2'], d_list[0]['quantity']))
        ctr_it('{0}: {1:,}   {2}: {3}s'.format(lo['L6'], d_batch, lo['71'], d_delay))
        d_proceed = proceed_run()
        if d_proceed == lo['N1'] or d_proceed == 'exit':
            return

    # Train Troops
    speeds_used, powders_used = [{}, {}]
    d_start = time()
    for x in range(d_batch):
        dur = -1
        job_id = 0
        for item in d_speed:
            for y in range(item['use']):
                if 'Testronius' in item['item'] and speed_cut_off >= dur != -1 or dur == 0:
                    break
                screen_update(title, lo['73'])
                ctr_it('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
                    lo['61'], t(d_troop), lo['H1'], t(d_location), lo['L2'], d_list[0]['quantity']))
                ctr_it('{0}: {1:,}   {2}: {3}s   {4}: {5}'.format(
                    lo['L6'], d_batch, lo['71'], d_delay, lo['74'], cvt_time(time() - d_start)))
                div_line('-')
                prog(x + 1, d_batch, '{0}: {1:,}/{2:,}'.format(lo['L7'], x + 1, d_batch))
                if speeds_used or powders_used:
                    init = '{0}'.format(lo['18']) if dur == -1 else '{0}: {1}'.format(lo['L8'], cvt_time(dur))
                    prog(y + 1, item['use'], 'Using {0}'.format(t(item['item'])), init)
                    if powders_used:
                        ctr_it('~~~ {0} ~~~'.format(lo['L9']), prefix=True)
                        display_it(powders_used, single=False)
                    if speeds_used:
                        ctr_it('~~~ {0} ~~~'.format(lo['D0']), prefix=True)
                        display_it(speeds_used, single=False)
                    if x > 0:
                        ctr_it('~~~ {0} ~~~'.format(lo['M0']), prefix=True)
                        ctr_it('{0:,}'.format(d_list[0]['quantity'] * x))
                        ctr_it('~~~ {0} ~~~'.format(lo['G8']), prefix=True)
                        ctr_it('{0:,}'.format(d_list[0]['quantity'] * x * d_list[0]['power']))
                else:
                    prog(0, 1, lo['18'])
                if dur == -1:
                    x_param = 'units%5Bquantity%5D={0}&units%5Bunit%5Ftype%5D={1}&%5Fmethod=post&'.format(
                        d_list[0]['quantity'], d_troop)
                    for server_retry in range(5):
                        sleep(d_delay)
                        try:
                            main_json = web_ops('cities/{0}/units'.format(d_list[0]['id']), x_param)
                            result = main_json['result']['success']
                            if result:
                                job_id = main_json['result']['job']['id']
                                dur = int(main_json['result']['job']['duration'])
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
                if dur > 1:
                    x_param = 'job%5Fid={0}&%5Fmethod=delete&'.format(job_id)
                    for server_retry in range(5):
                        sleep(d_delay)
                        try:
                            item_json = web_ops('player_items/{0}'.format(item['item']), x_param)
                            result = item_json['result']['success']
                            if result:
                                dur = int(item_json['result']['item_response']['run_at'] - item_json['timestamp'])
                                if dur < 0:
                                    dur = 0
                                if 'Testronius' not in item['item']:
                                    if t(item['item']) in speeds_used:
                                        speeds_used[t(item['item'])] += 1
                                    else:
                                        speeds_used[t(item['item'])] = 1
                                else:
                                    if t(item['item']) in powders_used:
                                        powders_used[t(item['item'])] += 1
                                    else:
                                        powders_used[t(item['item'])] = 1
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
    screen_update(title, lo['82'])
    ctr_it('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
        lo['61'], t(d_troop), lo['H1'], t(d_location), lo['L2'], d_list[0]['quantity']))
    ctr_it('{0}: {1:,}   {2}: {3}s'.format(lo['L6'], d_batch, lo['71'], d_delay))
    div_line('-')
    prog(1, 1, '{0} {1}'.format(lo['84'], cvt_time(time() - d_start)))
    if powders_used:
        ctr_it('~~~ {0} ~~~'.format(lo['L9']), prefix=True)
        display_it(powders_used, single=False)
    if speeds_used:
        ctr_it('~~~ {0} ~~~'.format(lo['D0']), prefix=True)
        display_it(speeds_used, single=False)
    ctr_it('~~~ {0} ~~~'.format(lo['M0']), prefix=True)
    ctr_it('{0:,}'.format(d_list[0]['quantity'] * d_batch))
    ctr_it('~~~ {0} ~~~'.format(lo['G8']), prefix=True)
    ctr_it('{0:,}'.format(d_list[0]['quantity'] * d_batch * d_list[0]['power']))
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
    print(lo['85'])
    get_data(title, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #


def revive_soul(title):
    # Initialize
    screen_update(title, lo['M1'])
    ctr_it(lo['18'])
    d_list = list()
    d_location = 'spectral'
    dp_level, dp_total, dp_combo = [0, 0, 0]
    try:
        spec = cData[d_location]['city']['buildings']
    except KeyError:
        spec = None
    if spec:
        be = cData['capital']['city']['resources']['blue_energy']
        for x in range(len(spec)):
            if spec[x]['type'] == 'DarkPortal':
                if dp_level < spec[x]['level']:
                    dp_level = spec[x]['level']
                dp_total += 1
                dp_combo += spec[x]['level']
        for key, value in cData['capital']['city']['souls'].items():
            for x in range(len(mData['units'])):
                if key == mData['units'][x]['type']:
                    if dp_level >= mData['units'][x]['requirements'][d_location]['buildings']['DarkPortal'] and be >= \
                            mData['units'][x]['requirements'][d_location]['resources']['blue_energy']:
                        y = int(be / mData['units'][x]['requirements'][d_location]['resources']['blue_energy'])
                        if y > value:
                            y = value
                        multiplier = dp_total + ((dp_combo - dp_total) / 10)
                        my_dict = {'troop': key, 'total': value, 'quantity': y, 'time': mData['units'][x]['time'],
                                   'multiplier': multiplier, 'desc': t(key), 'id': cData[d_location]['city']['id'],
                                   'power': mData['units'][x]['stats']['power']}
                        d_list.append(my_dict)
    if not d_list:
        nothing_to_do(title, lo['M1'], lo['M2'])
        return
    if len(d_list) == 1:
        d_troop = d_list[0]['troop']
    else:
        d_list = sorted(d_list, key=itemgetter('desc'))
        d_troop = None
        a, b, c = [lo['M3'], lo['K7'], lo['M4']]
        a1, b1, c1 = [len(a), len(b), len(c)]
        for x in range(len(d_list)):
            if len(d_list[x]['desc']) > a1:
                a1 = len(d_list[x]['desc'])
            if len('{0:,}'.format(d_list[x]['total'])) > b1:
                b1 = len('{0:,}'.format(d_list[x]['total']))
            if len('{0:,}'.format(d_list[x]['quantity'])) > c1:
                c1 = len('{0:,}'.format(d_list[x]['quantity']))
        while d_troop is None:
            screen_update(title, lo['M1'])
            ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
            ctr_it('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
            for x in range(len(d_list)):
                ctr_it('{0:<{1}}  {2:>{3},}  {4:>{5},}'.format(
                    d_list[x]['desc'], a1, d_list[x]['total'], b1, d_list[x]['quantity'], c1))
            div_line()
            d_select = input(' {0}: '.format(lo['06']))
            if len(d_select) >= 3:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                else:
                    for x in range(len(d_list)):
                        if d_select.lower() == d_list[x]['desc'].lower():
                            d_troop = d_list[x]['troop']
                            break
                    else:
                        for x in range(len(d_list)):
                            if d_select.lower() in d_list[x]['desc'].lower():
                                d_troop = d_list[x]['troop']
                                break
    d_list[:] = [d for d in d_list if d.get('troop') == d_troop]
    if d_list[0]['total'] > 1:
        d_max_queue = 0
        # Set Training Queue Size
        while d_max_queue is 0:
            screen_update(title, lo['M5'])
            ctr_it('{0}: {1}   {2}: {3}'.format(lo['61'], t(d_troop), lo['H1'], t(d_location)))
            ctr_it(' ')
            div_line('-')
            ctr_it('~~~ {0} ~~~'.format(lo['86']))
            ctr_it('1 - {0}'.format(d_list[0]['quantity']), suffix=True)
            print(' {0}'.format(lo['K9']))
            div_line()
            d_select = input(' {0} : '.format(lo['06']))
            if len(d_select) >= 1:
                if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                    return
                elif d_select.lower() == lo['O3'] or d_select.lower() == 'max':
                    d_max_queue = d_list[0]['quantity']
                elif d_select.isnumeric():
                    if int(d_select) in range(1, d_list[0]['quantity'] + 1):
                        d_max_queue = int(d_select)
        d_list[0]['quantity'] = d_max_queue
    # Set Speed Items
    a, b, c, d = [lo['L0'], lo['C1'], lo['A3'], lo['C2']]
    a1, b1, c1, d1 = [len(a), len(b), len(c), len(d)]
    selection = [{'item': 'DarkTestroniusInfusion', 'time': 0.99}, {'item': 'DarkTestroniusDeluxe', 'time': 0.5},
                 {'item': 'DarkTestroniusPowder', 'time': 0.3}, {'item': 'Blitz', 'time': 345600},
                 {'item': 'Blast', 'time': 216000}, {'item': 'Bolt', 'time': 86400}, {'item': 'Bore', 'time': 54000},
                 {'item': 'Bounce', 'time': 28800}, {'item': 'Leap', 'time': 9000}, {'item': 'Jump', 'time': 3600},
                 {'item': 'Skip', 'time': 900}, {'item': 'Hop', 'time': 300}, {'item': 'Blink', 'time': 60}]
    d_speed = list()
    for x in range(len(selection)):
        if selection[x]['item'] in pData['items']:
            if pData['items'][selection[x]['item']] > 0:
                if selection[x]['time'] < 1:
                    y = '{0}% {1}'.format(int(selection[x]['time'] * 100), lo['O2'])
                else:
                    y = '{0}'.format(cvt_time(selection[x]['time'], show_seconds=False))
                my_dict = {'item': selection[x]['item'], 'qty': pData['items'][selection[x]['item']],
                           'time': selection[x]['time'], 'desc': y, 'use': 0}
                d_speed.append(my_dict)
                if len(t(selection[x]['item'])) > a1:
                    a1 = len(t(selection[x]['item']))
                if len(y) > b1:
                    b1 = len(y)
                if len('{0:,}'.format(pData['items'][selection[x]['item']])) > c1:
                    c1 = len(str(pData['items'][selection[x]['item']]))
    while True:
        screen_update(title, lo['L1'])
        ctr_it('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
            lo['61'], t(d_troop), lo['H1'], t(d_location), lo['L2'], d_list[0]['quantity']))
        ctr_it(' ')
        div_line('-')
        ctr_it('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}'.format(a, a1, b, b1, c, c1, d, d1))
        ctr_it('{0}  {1}  {2}  {3}'.format('-' * a1, '-' * b1, '-' * c1, '-' * d1))
        reduced_time = (d_list[0]['time'] * d_list[0]['quantity'] * 0.15 / d_list[0]['multiplier'])
        for x in range(len(d_speed)):
            ctr_it('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}'.format(
                t(d_speed[x]['item']), a1, d_speed[x]['desc'], b1, d_speed[x]['qty'], c1,
                d_speed[x]['use'], d1))
            if d_speed[x]['use'] != 0:
                if d_speed[x]['time'] < 1:
                    for y in range(d_speed[x]['use']):
                        reduced_time *= (1 - d_speed[x]['time'])
                else:
                    for y in range(d_speed[x]['use']):
                        reduced_time -= d_speed[x]['time']
        else:
            reduced_time = 0 if reduced_time < 0 else cvt_time(reduced_time)
            ctr_it('{0}: {1}'.format(lo['L3'], reduced_time), prefix=True, suffix=True)
        if reduced_time != 0:
            print(' {0}'.format(lo['C6']))
        else:
            print(' {0}'.format(lo['C7']))
        div_line()
        d_select = input(' {0} : '.format(lo['06']))
        if len(d_select) >= 3:
            if d_select.lower() == lo['N1'] or d_select.lower() == 'exit':
                return
            elif (d_select.lower() == lo['N4'] or d_select.lower() == 'next') and reduced_time == 0:
                break
            else:
                try:
                    i_item, i_qty = d_select.split('@')
                    if i_qty.isnumeric():
                        for x in range(len(d_speed)):
                            if i_item.lower() == t(d_speed[x]['item']).lower() and int(i_qty) < d_speed[x]['qty']:
                                d_speed[x]['use'] = int(i_qty)
                                break
                        else:
                            for x in range(len(d_speed)):
                                if i_item.lower() in t(d_speed[x]['item']).lower() and int(i_qty) < d_speed[x]['qty']:
                                    d_speed[x]['use'] = int(i_qty)
                                    break
                except(TypeError, ValueError):
                    pass
    d_speed[:] = [d for d in d_speed if d.get('use') != 0]
    d_max_queue = int(d_list[0]['total'] / d_list[0]['quantity'])
    speed_cut_off = 0
    for x in range(len(d_speed)):
        if d_max_queue > (d_speed[x]['qty'] / d_speed[x]['use']):
            d_max_queue = int(d_speed[x]['qty'] / d_speed[x]['use'])
        if 'Testronius' not in d_speed[x]['item']:
            speed_cut_off += d_speed[x]['time']
    d_batch = 1 if d_max_queue == 1 else None

    # Set Number Of Batches
    while d_batch is None:
        screen_update(title, lo['M6'])
        ctr_it('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
            lo['61'], t(d_troop), lo['H1'], t(d_location), lo['L2'], d_list[0]['quantity']))
        ctr_it(' ')
        d_batch = set_batch(d_max_queue + 1, '{0}'.format(lo['M7']))
        if d_batch == lo['N1'] or d_batch == 'exit':
            return

    # Set Delay
    d_delay = None
    while d_delay is None:
        screen_update(title, lo['69'])
        ctr_it('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
            lo['61'], t(d_troop), lo['H1'], t(d_location), lo['L2'], d_list[0]['quantity']))
        ctr_it('{0}: {1:,}'.format(lo['L6'], d_batch))
        d_delay = set_delay()
        if d_delay == lo['N1'] or d_delay == 'exit':
            return

    # Proceed With Run
    d_proceed = False
    while not d_proceed:
        screen_update(title, lo['70'])
        ctr_it('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
            lo['61'], t(d_troop), lo['H1'], t(d_location), lo['L2'], d_list[0]['quantity']))
        ctr_it('{0}: {1:,}   {2}: {3}s'.format(lo['L6'], d_batch, lo['71'], d_delay))
        d_proceed = proceed_run()
        if d_proceed == lo['N1'] or d_proceed == 'exit':
            return

    # Revive Troops
    speeds_used, powders_used = [{}, {}]
    d_start = time()
    for x in range(d_batch):
        dur = -1
        job_id = 0
        for item in d_speed:
            for y in range(item['use']):
                if 'Testronius' in item['item'] and speed_cut_off >= dur != -1 or dur == 0:
                    break
                screen_update(title, lo['73'])
                ctr_it('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
                    lo['61'], t(d_troop), lo['H1'], t(d_location), lo['L2'], d_list[0]['quantity']))
                ctr_it('{0}: {1:,}   {2}: {3}s   {4}: {5}'.format(
                    lo['L6'], d_batch, lo['71'], d_delay, lo['74'], cvt_time(time() - d_start)))
                div_line('-')
                prog(x + 1, d_batch, '{0}: {1:,}/{2:,}'.format(lo['L7'], x + 1, d_batch))
                if speeds_used or powders_used:
                    init = '{0}'.format(lo['18']) if dur == -1 else '{0}: {1}'.format(lo['L8'], cvt_time(dur))
                    prog(y + 1, item['use'], '{0} {1}'.format(lo['M8'], t(item['item'])), init)
                    if powders_used:
                        ctr_it('~~~ {0} ~~~'.format(lo['M9']), prefix=True)
                        display_it(powders_used, single=False)
                    if speeds_used:
                        ctr_it('~~~ {0} ~~~'.format(lo['D0']), prefix=True)
                        display_it(speeds_used, single=False)
                    if x > 0:
                        ctr_it('~~~ {0} ~~~'.format(lo['M0']), prefix=True)
                        ctr_it('{0:,}'.format(d_list[0]['quantity'] * x))
                        ctr_it('~~~ {0} ~~~'.format(lo['G8']), prefix=True)
                        ctr_it('{0:,}'.format(d_list[0]['quantity'] * x * d_list[0]['power']))
                else:
                    prog(0, 1, lo['18'])
                if dur == -1:
                    x_param = 'units%5Bquantity%5D={0}&units%5Bunit%5Ftype%5D={1}&%5Fmethod=post&'.format(
                        d_list[0]['quantity'], d_troop)
                    for server_retry in range(5):
                        sleep(d_delay)
                        try:
                            main_json = web_ops('cities/{0}/units/resurrect'.format(d_list[0]['id']), x_param)
                            result = main_json['result']['success']
                            if result:
                                job_id = main_json['result']['job']['id']
                                dur = int(main_json['result']['job']['duration'])
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
                if dur > 1:
                    x_param = 'job%5Fid={0}&%5Fmethod=delete&'.format(job_id)
                    for server_retry in range(5):
                        sleep(d_delay)
                        try:
                            item_json = web_ops('player_items/{0}'.format(item['item']), x_param)
                            result = item_json['result']['success']
                            if result:
                                dur = int(item_json['result']['item_response']['run_at'] - item_json['timestamp'])
                                if dur < 0:
                                    dur = 0
                                if 'Testronius' not in item['item']:
                                    if t(item['item']) in speeds_used:
                                        speeds_used[t(item['item'])] += 1
                                    else:
                                        speeds_used[t(item['item'])] = 1
                                else:
                                    if t(item['item']) in powders_used:
                                        powders_used[t(item['item'])] += 1
                                    else:
                                        powders_used[t(item['item'])] = 1
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
    screen_update(title, lo['82'])
    ctr_it('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
        lo['61'], t(d_troop), lo['H1'], t(d_location), lo['L2'], d_list[0]['quantity']))
    ctr_it('{0}: {1:,}   {2}: {3}s'.format(lo['L6'], d_batch, lo['71'], d_delay))
    div_line('-')
    prog(1, 1, '{0} {1}'.format(lo['84'], cvt_time(time() - d_start)))
    if powders_used:
        ctr_it('~~~ {0} ~~~'.format(lo['M9']), prefix=True)
        display_it(powders_used, single=False)
    if speeds_used:
        ctr_it('~~~ {0} ~~~'.format(lo['D0']), prefix=True)
        display_it(speeds_used, single=False)
    ctr_it('~~~ {0} ~~~'.format(lo['N0']), prefix=True)
    ctr_it('{0:,}'.format(d_list[0]['quantity'] * d_batch))
    ctr_it('~~~ {0} ~~~'.format(lo['G8']), prefix=True)
    ctr_it('{0:,}'.format(d_list[0]['quantity'] * d_batch * d_list[0]['power']))
    div_line()
    os.system('pause' if os.name == 'nt' else 'read -s -n 1 -p "Press any key to continue..."')
    print(lo['85'])
    get_data(title, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def switch_realm(title, realm_no=0, c_no=0):
    global d_rn, d_cn, realm, cookie, std_param, d_si, d_conn
    d_rn = realm_no
    d_cn = c_no
    get_realm_info(title)

    # Fixed Variables
    d_si = b2a_hex(os.urandom(16))
    realm = 'realm{0}.c{1}.castle.rykaiju.com'.format(d_rn, d_cn)
    d_conn = http.client.HTTPConnection(realm, 80)
    cookie = 'dragons={0}'.format(d_si)
    std_param = 'dragon%5Fheart={0}&user%5Fid={1}&version=overarch&%5Fsession%5Fid={2}'.format(d_dh, d_ui, d_si)

    # Refresh Data Files
    refresh_data(title)


# -------------------------------------------------------------------------------------------------------------------- #

def refresh_data(title):
    global pData, mData, fData, pfData, cData, tData
    get_data(title, pl=True, fm=True, pf=True, op=True, w1=True, w2=True, w3=True, unmute=True)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                      MENU CLASS                                                      #
# -------------------------------------------------------------------------------------------------------------------- #
def menu():
    module_dict = {create_equipment: lo['31'], forge_ingredient: lo['32'], farm_mission: lo['33'], open_chest: lo['34'],
                   unpack_arsenal: lo['35'], upgrade_building: lo['36'], fill_building: lo['37'], train_troop: lo['38'],
                   revive_soul: lo['39']}
    system_dict = {switch_realm: lo['40'], refresh_data: lo['41'], enter_script: lo['42'], choose_language: lo['43']}
    while True:
        screen_update(lo['44'], lo['45'])
        ctr_it('~~~ {0} ~~~'.format(lo['46']))
        display_it(module_dict)
        ctr_it('~~~ {0} ~~~'.format(lo['47']), prefix=True)
        display_it(system_dict)
        print('\n {0}'.format(lo['48']))
        div_line()
        d_select = input(' {0} : '.format(lo['06']))
        if len(d_select) >= 2:
            if d_select.lower() == lo['N3'] or d_select.lower() == 'quit':
                exit_script()
            else:
                for key, value in module_dict.items():
                    if d_select.lower() in value.lower() or d_select.lower() == value.lower():
                        key(value.upper())
                for key, value in system_dict.items():
                    if d_select.lower() in value.lower() or d_select.lower() == value.lower():
                        key(value.upper())


# -------------------------------------------------------------------------------------------------------------------- #
#                                                         MAIN                                                         #
# -------------------------------------------------------------------------------------------------------------------- #

# Initialize Global Variables
d_ui, d_rn, d_cn = [0, 0, 0]
d_dh, d_si, realm, cookie, std_param, d_conn = ['', '', '', '', '', '']
pData, mData, fData, pfData, cData, fStat = ['', '', '', '', '', '']
tData, lo = [{}, {}]
try:
    with open('locale.doa', 'r') as load_file:
        lo = json.load(load_file)
except FileNotFoundError:
    choose_language(shut_script=False)
# Load Translations
for tlookup in ('dict_f_eqp', 'dict_build', 'dict_troop', 'dict_f_adv', 'dict_f_mis', 'dict_f_itm'):
    for tkey, tvalue in lo[tlookup].items():
        if tkey not in tData:
            tData[tkey] = tvalue

# Launch Menu
if __name__ == '__main__':
    enter_script(lo['01'])
    check_version()
    menu()
