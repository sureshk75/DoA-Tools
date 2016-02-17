# -*- coding: utf-8 -*-
import http.client
import json
import os
from binascii import b2a_hex
from hashlib import sha1
from operator import itemgetter
from time import time, sleep

__version__ = '2.0.4'


########################################################################################################################
#                                             SCRIPT SECTION - Do Not Edit!                                            #
########################################################################################################################
# -------------------------------------------------------------------------------------------------------------------- #
#                                              FUNCTIONAL CLASSES/MODULES                                              #
# -------------------------------------------------------------------------------------------------------------------- #
def dvsn(default='_', suffix=True):
    print(' ' + (default * 78))
    if suffix:
        print(' ')


def scrn(title, subtitle):
    os.system('cls' if os.name == 'nt' else 'clear')
    v_len = len(__version__)
    try:
        a = '{0}({1})'.format(pData['name'], d_rn) if d_rn != 0 else ''
    except (KeyError, NameError, TypeError):
        a = ''
    print('\n {0:<55}  {1:>21}\n     {2:<{3}}{4}'.format(
            title.upper(), a, subtitle.title(), 74 - v_len, __version__))
    dvsn()


def web_op(operation, param_add_on, method='POST', post=True):
    global realm, std_param, cookie, d_conn
    dl = {'00': lo['c55'], '01': lo['c86'], '02': lo['a14'], '03': lo['c87'], '04': lo['b92'], '05': lo['c13'],
          '06': lo['c12']}
    url = 'http://{0}/api/{1}'.format(realm, operation)
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
            for cd_ban in range(3660):
                scrn(dl['00'], dl['01'])
                prg(cd_ban, 3660, '{0}: {1}'.format(dl['02'], cvttm(3660 - cd_ban)))
                sleep(1)
        elif conn_resp.status == 509:
            d_conn.close()
            for cd_ban in range(60):
                scrn(dl['00'], dl['03'])
                prg(cd_ban, 60, '{0}: {1}'.format(dl['04'], cvttm(60 - cd_ban)))
                sleep(1)
        elif conn_resp.status in (500, 502):
            sleep(5)
        else:
            errmsg('{0} {1}'.format(dl['05'], conn_resp.status))
    except http.client.CannotSendRequest:
        errmsg(dl['06'])
    except http.client.HTTPException:
        d_conn.close()
        sleep(2)


def prg(p_count, p_total, prefix, suffix=None):
    filled_len = int(round(50 * p_count / float(p_total)))
    bar = ('▓' * filled_len) + ('░' * (50 - filled_len))
    print(prefix.center(78))
    print(bar.center(78))
    if suffix:
        print(suffix.center(78))


def errmsg(string):
    dl = {'00': lo['b43'], '01': lo['b46']}
    dvsn('#')
    ctrt(string)
    ctrt(dl['00'], suffix=True)
    dvsn('#')
    input(dl['01'])
    quit()


def gtdt(pl=True, fm=False, pf=False, op=False, w1=False, w2=False, w3=False, unmute=True):
    global pData, mData, fData, pfData, cData, tData, d_conn, fStat
    dl = {'00': lo['a92'].upper(), '01': lo['b61'], '02': lo['b72'], '03': lo['b62'], '04': lo['b73'], '05': lo['a92'],
          '06': lo['a79'], '07': lo['a28'], '08': lo['a75'], '09': lo['b74'], '10': lo['c11'], '11': lo['b42'],
          '12': lo['a74'], '13': lo['a72'], '14': lo['b50'], '15': lo['c09']}
    prg_hdr, sub_hdr = [dl['03'], dl['01']] if pData or mData or fData or pfData or cData else [dl['04'], dl['02']]
    w1_data, w2_data, m_count, count = [None, None, 0, 0]
    for check in (w1, w2, w3, pl, fm, pf):
        if check:
            m_count += 1
    if unmute:
        scrn(dl['00'], sub_hdr)
        prg(count, m_count, dl['05'])
    conn = http.client.HTTPConnection('wackoscripts.com', 80)
    req = [{'0': w1, '1': dl['06'], '2': 'manifest'},
           {'0': w2, '1': dl['07'], '2': 'chest'},
           {'0': w3, '1': dl['08'], '2': 'forgestat'}]
    for x in range(len(req)):
        if req[x]['0']:
            name = req[x]['1']
            url = 'http://wackoscripts.com/sanctuary/{0}.json'.format(req[x]['2'])
            if unmute:
                scrn(dl['00'], sub_hdr)
                prg(count, m_count, '{0} {1}'.format(prg_hdr, name))
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
                        scrn(dl['00'], sub_hdr)
                        prg(count, m_count, '{0} {1}'.format(prg_hdr, name),
                            '{0}: {1}/2'.format(dl['09'], web_retry + 1))
                    sleep(1)
                    continue
            else:
                errmsg('{0} {1}'.format(dl['10'], name))
            if w1_data:
                for key, value in w1_data.items():
                    if key not in tData and value != '':
                        tData[key] = value
                    if key not in tData and value == '':
                        tData[key] = key
    req = [{'0': pl, '1': dl['11'], '2': 'player.json', '3': '?', '4': 'GET', '5': False},
           {'0': fm, '1': dl['12'], '2': 'forge/forge.json', '3': '', '4': 'GET', '5': True},
           {'0': pf, '1': dl['13'], '2': 'forge/player_forge_info.json', '3': '', '4': 'GET', '5': True}]
    for x in range(len(req)):
        if req[x]['0']:
            name = req[x]['1']
            if unmute:
                scrn(dl['00'], sub_hdr)
                prg(count, m_count, '{0} {1}'.format(prg_hdr, name))
            for web_retry in range(2):
                try:
                    conn_data = web_op(req[x]['2'], req[x]['3'], req[x]['4'], req[x]['5'])
                    count += 1
                    if req[x]['2'] == 'forge/forge.json':
                        fData = conn_data
                    elif req[x]['2'] == 'player.json':
                        pData = conn_data
                    elif req[x]['2'] == 'forge/player_forge_info.json':
                        pfData = conn_data
                    break
                except (KeyError, TypeError):
                    if unmute:
                        scrn(dl['00'], sub_hdr)
                        prg(count, m_count, '{0} {1}'.format(prg_hdr, name),
                            '{0}: {1}/2'.format(dl['09'], web_retry + 1))
                    sleep(1)
                    continue
            else:
                errmsg('{0} {1}'.format(dl['10'], name))
    if op:
        cData = {}
        for loc_key in sorted(pData['cities']):
            if unmute:
                scrn(dl['00'], sub_hdr)
                prg(1, 1, '{0} {1}'.format(dl['14'], t(loc_key)))
            for web_retry in range(5):
                try:
                    current_location = web_op('cities/{0}.json'.format(pData['cities'][loc_key]['id']), '')
                    cData[loc_key] = current_location
                    break
                except (KeyError, TypeError):
                    if unmute:
                        scrn(dl['00'], sub_hdr)
                        prg(1, 1, '{0} {1}'.format(dl['14'], t(loc_key)), '{0}: {1}/5'.format(dl['09'], web_retry + 1))
                    sleep(1)
                    continue
            else:
                errmsg(dl['15'])
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


def cvttm(time_value=0, ss=True):
    m, s = divmod(time_value, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if ss:
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


def ctrt(string, prefix=False, suffix=False):
    if prefix:
        print('')
    print(string.center(78))
    if suffix:
        print('')


def chslng(title=True, shut_script=True):
    global lo
    if title:
        dl = {'00': lo['a29'], '01': lo['c01'], '02': lo['a52'], '03': lo['b93'], '04': lo['c10']}
        x = dl['04']
    else:
        x = 'ERROR ACCESSING LANGUAGE FILE'
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
        except (KeyError, TypeError):
            sleep(1)
            continue
    else:
        errmsg(x)
    if conn_data:
        d_lang = None
        while d_lang is None:
            if title:
                scrn(dl['00'], dl['01'])
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                ctrt('~~~ Language/Sprog/Sprache/Idioma/Langue/Lingua/Taal/Språk/Dil ~~~', prefix=True)
            for x in range(len(conn_data)):
                ctrt(conn_data[x]['type'])
            dvsn()
            if title:
                d_select = input(' {0} : '.format(dl['02']))
            else:
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
            ctrt(dl['03'], prefix=True, suffix=True)
            sleep(5)
            quit()


def chkver():
    dl = {'00': lo['b08'], '01': lo['c82'], '02': lo['a93'], '03': lo['a81'], '04': lo['b92']}
    if __version__ != fStat['version']:
        for x in range(5):
            scrn(dl['00'], dl['01'])
            dvsn('*')
            ctrt('DoA-Tools v{0} {1}'.format(fStat['version'], dl['02']), suffix=True)
            ctrt(dl['03'])
            ctrt(fStat['url'], suffix=True)
            ctrt('{0} {1}'.format(dl['04'], cvttm(5 - x)), prefix=True, suffix=True)
            dvsn('*')
            sleep(1)


def t(string):
    for key, value in tData.items():
        if string == key:
            return value
    else:
        return string


def dsply(my_list, single=True):
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
                ctrt(x)
                y = 0
                x = ''
            else:
                y += 1
        if y != 0:
            z = ' ' * ((max_len + 2) * (max_items - y))
            x += z
            ctrt(x)
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
                ctrt(x)
                y = 0
                x = ''
            else:
                y += 1
        if y != 0:
            z = ' ' * ((max_len + 4) * (max_items - y))
            x += z
            ctrt(x)


def stbtch(max_value, exec_string):
    dl = {'00': lo['a11'], '01': lo['a52'], '02': lo['a59']}
    dvsn('-')
    ctrt('~~~ {0} ~~~'.format(dl['00']))
    ctrt('1 - {0}'.format(max_value - 1), suffix=True)
    ctrt(exec_string)
    dvsn()
    i = input(' {0} : '.format(dl['01']))
    if len(i) >= 1:
        if i.lower() == dl['02'] or i.lower() == 'exit':
            return 'exit'
        if i.isnumeric():
            if int(i) in range(1, max_value):
                return int(i)


def stdly():
    dl = {'00': lo['a11'], '01': lo['a46'], '02': lo['c43'], '03': lo['c80'], '04': lo['a52'], '05': lo['a59']}
    dvsn('-')
    ctrt('~~~ {0} ~~~'.format(dl['00']))
    ctrt('0 - 5', suffix=True)
    ctrt(dl['01'])
    ctrt(dl['02'], suffix=True)
    ctrt(dl['03'])
    dvsn()
    i = input(' {0} : '.format(dl['04']))
    if len(i) >= 1:
        if i.lower() == dl['05'] or i.lower() == 'exit':
            return 'exit'
        if i.isnumeric():
            if int(i) in range(6):
                return int(i)


def prcd():
    dl = {'00': lo['a11'], '01': lo['c84'], '02': lo['b48'], '03': lo['a52'], '04': lo['a59'], '05': lo['c85'],
          '06': lo['b19']}
    dvsn('-')
    ctrt('~~~ {0} ~~~'.format(dl['00']))
    ctrt(dl['01'], suffix=True)
    ctrt(dl['02'])
    dvsn()
    i = input(' {0} : '.format(dl['03']))
    if len(i) >= 1:
        if i.lower() == dl['04'] or i.lower() == 'exit':
            return 'exit'
        if i.isalpha():
            if i.lower() == dl['05'].lower() or i.lower() == 'yes':
                return True
            elif i.lower() == dl['06'].lower() or i.lower() == 'no':
                return 'exit'


def nthng(title, subtitle, exec_string):
    dl = {'00': lo['c88']}
    scrn(title, subtitle)
    dvsn('*')
    ctrt(exec_string, suffix=True)
    dvsn('*')
    input(dl['00'])


def trnct(content, length=100, suffix='..'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length + 1].split(' ')[0:-1]) + suffix


def scpxt():
    dl = {'00': lo['c42'], '01': lo['a24'], '02': lo['c83'], '03': lo['a98']}
    os.system('cls' if os.name == 'nt' else 'clear')
    ctrt('{0} DoA Tools v{1}'.format(dl['00'], __version__), prefix=True, suffix=True)
    ctrt(dl['01'])
    ctrt(fStat['author'])
    ctrt('{0} {1}'.format(dl['02'], fStat['contrib']), suffix=True)
    ctrt(dl['03'])
    ctrt(fStat['url'], suffix=True)
    sleep(3)
    quit()


def scpnt():
    global d_ui, d_dh, d_rn, d_cn
    dl = {'00': lo['b06'], '01': lo['b98'], '02': lo['a07'], '03': lo['b26'], '04': lo['a52'], '05': lo['b15'],
          '06': lo['b14']}
    slc, d_ui, d_dh, d_rn, d_cn, r_file = [{}, 0, 0, 0, 0, None]
    try:
        with open('DoA-Tools.doa', 'r') as read_file:
            r_file = json.load(read_file)
            for x in range(len(r_file)):
                slc[r_file[x]['id']] = '{0}({1})'.format(r_file[x]['ac'], r_file[x]['rn'])
    except FileNotFoundError:
        pass
    load_acct = False
    if slc:
        while not load_acct:
            scrn(dl['00'], dl['01'])
            ctrt('~~~ {0} ~~~'.format(dl['02']), suffix=True)
            dsply(slc)
            print('\n\n {0}'.format(dl['03']))
            dvsn()
            i = input(' {0} : '.format(dl['04']))
            if len(i) >= 1:
                if i.lower() == dl['05'] or i.lower() == 'new':
                    break
                for key, value in slc.items():
                    if i.lower() == value.lower():
                        for x in range(len(r_file)):
                            if r_file[x]['id'] == key:
                                d_ui = r_file[x]['ui']
                                d_dh = r_file[x]['dh']
                                d_rn = r_file[x]['rn']
                                d_cn = r_file[x]['cn']
                                load_acct = True
                                break
                        break
                else:
                    for key, value in slc.items():
                        if i.lower() in value.lower():
                            for x in range(len(r_file)):
                                if r_file[x]['id'] == key:
                                    d_ui = r_file[x]['ui']
                                    d_dh = r_file[x]['dh']
                                    d_rn = r_file[x]['rn']
                                    d_cn = r_file[x]['cn']
                                    load_acct = True
                                    break
                            break
    x = dl['00'] if load_acct else dl['06']
    gtacct(x)
    gtrlm(x)
    switch_realm(x, d_rn, d_cn)


def chkinp(entry, input_list):
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
def gtacct(title):
    global d_ui, d_dh, d_si
    dl = {'00': lo['a67'], '01': lo['a56'], '02': lo['c77'], '03': lo['a55']}
    while not d_ui:
        scrn(title, dl['00'])
        d_select = input(' {0} : '.format(dl['01']))
        if len(d_select) >= 1:
            if d_select.isnumeric():
                d_ui = int(d_select)

    while not d_dh:
        scrn(title, dl['00'])
        ctrt('{0}: {1}'.format(dl['02'], d_ui))
        dvsn()
        d_select = input(' {0} : '.format(dl['03']))
        if len(d_select) >= 3:
            if d_select.isalnum():
                d_dh = d_select


def gtrlm(title=''):
    global d_rn, d_cn
    dl = {'00': lo['c32'], '01': lo['a68'], '02': lo['c77'], '03': lo['a45'], '04': lo['a54'], '05': lo['b58'],
          '06': lo['a53']}
    x = dl['00'] if not title else title
    while not d_rn:
        scrn(x, dl['01'])
        ctrt('{0}: {1}   {2}: {3:.15}..'.format(dl['02'], d_ui, dl['03'], d_dh))
        ctrt(' ')
        dvsn()
        d_select = input(' {0} : '.format(dl['04']))
        if len(d_select) >= 1:
            if d_select.isnumeric():
                d_rn = int(d_select)

    while not d_cn:
        scrn(x, dl['01'])
        ctrt('{0}: {1}   {2}: {3:.15}..'.format(dl['02'], d_ui, dl['03'], d_dh))
        ctrt('{0}: {1}'.format(dl['05'], d_rn))
        dvsn()
        d_select = input(' {0} : '.format(dl['06']))
        if len(d_select) >= 1:
            if d_select.isnumeric():
                d_cn = int(d_select)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                      FORGE CLASS                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
def craft_equipment():
    dl = {'00': lo['a31'], '01': lo['c08'], '02': lo['a92'], '03': lo['c47'], '04': lo['a12'], '05': lo['a52'],
          '06': lo['a59'], '07': lo['a57'], '08': lo['a33'], '09': lo['a42'], '10': lo['b05'], '11': lo['b11'],
          '12': lo['b55'], '13': lo['b56'], '14': lo['c29'], '15': lo['c07'], '16': lo['c65'], '17': lo['a52'],
          '18': lo['c16'], '19': lo['c67'], '20': lo['b22'], '21': lo['b31'], '22': lo['a35'], '23': lo['a90'],
          '24': lo['a32'], '25': lo['c15'], '26': lo['a43'], '27': lo['b57'], '28': lo['b51'], '29': lo['a47'],
          '30': lo['a34'], '31': lo['b34'], '32': lo['c30'], '33': lo['a60'], '34': lo['b02'], '35': lo['a37'],
          '36': lo['b01'], '37': lo['a36'], '38': lo['b84'], '39': lo['b82'], '40': lo['c31'], '41': lo['b49'],
          '42': lo['b47'], '43': lo['c72']}
    scrn(dl['00'], dl['01'])
    ctrt(dl['02'])
    d_lst, slctn = [list(), {}]
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
                d_queue = 9999
                met_req = (len(recipe['items']))
                for r_key, r_value in recipe['items'].items():
                    for r_item in range(len(ingredients)):
                        if r_key == ingredients[r_item]['name']:
                            if r_value < ingredients[r_item]['quantity']:
                                met_req -= 1
                                if d_queue > int(ingredients[r_item]['quantity'] / r_value):
                                    d_queue = int(ingredients[r_item]['quantity'] / r_value)
                            else:
                                break
                if met_req == 0:
                    f_multiply = fStat[key] if key in fStat else 1
                    for x in range(len(mData['units'])):
                        if mData['units'][x]['type'] == fData['forge']['items'][key]['troop_type']:
                            my_dict = {'troop': mData['units'][x]['type'],
                                       'item': key, 'craftable': d_queue,
                                       'defense': int(mData['units'][x]['stats']['defense'] * f_multiply),
                                       'life': int(mData['units'][x]['stats']['life'] * f_multiply),
                                       'melee': int(mData['units'][x]['stats']['melee'] * f_multiply),
                                       'range': int(mData['units'][x]['stats']['range'] * f_multiply),
                                       'ranged': int(mData['units'][x]['stats']['ranged'] * f_multiply),
                                       'speed': int(mData['units'][x]['stats']['speed'] * f_multiply)}
                            d_lst.append(my_dict)
    if not d_lst:
        nthng(dl['00'], dl['01'], dl['03'])
        return
    else:
        for x in range(len(d_lst)):
            if d_lst[x]['troop'] not in slctn.keys():
                slctn[d_lst[x]['troop']] = t(d_lst[x]['troop'])
    d_troop = None
    while d_troop is None:
        scrn(dl['00'], dl['01'])
        ctrt('~~~ {0} ~~~'.format(dl['04']))
        dsply(slctn)
        dvsn()
        d_select = input(' {0} : '.format(dl['05']))
        if len(d_select) >= 1:
            if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                return
            else:
                d_troop = chkinp(d_select, slctn)
    d_lst[:] = [d for d in d_lst if d.get('troop') == d_troop]
    slctn.clear()
    for x in range(len(d_lst)):
        if d_lst[x]['item'] not in slctn.keys():
            slctn[d_lst[x]['item']] = t(d_lst[x]['item'])
    a, b, c, d, e, f, g, h = [dl['07'], dl['08'], dl['09'].title(), dl['10'].title(), dl['11'].title(),
                              dl['12'].title(), dl['13'].title(), dl['14'].title()]
    a1, b1, c1, d1, e1, f1, g1, h1 = [len(a), len(b), len(c), len(d), len(e), len(f), len(g), len(h)]
    for x in range(len(d_lst)):
        if len(t(d_lst[x]['item'])) > a1:
            a1 = len(t(d_lst[x]['item']))
        if len('{0:,}'.format(d_lst[x]['craftable'])) > b1:
            b1 = len('{0:,}'.format(d_lst[x]['craftable']))
        if len('{0:,}'.format(d_lst[x]['defense'])) > c1:
            c1 = len('{0:,}'.format(d_lst[x]['defense']))
        if len('{0:,}'.format(d_lst[x]['life'])) > d1:
            d1 = len('{0:,}'.format(d_lst[x]['life']))
        if len('{0:,}'.format(d_lst[x]['melee'])) > e1:
            e1 = len('{0:,}'.format(d_lst[x]['melee']))
        if len('{0:,}'.format(d_lst[x]['range'])) > f1:
            f1 = len('{0:,}'.format(d_lst[x]['range']))
        if len('{0:,}'.format(d_lst[x]['ranged'])) > g1:
            g1 = len('{0:,}'.format(d_lst[x]['ranged']))
        if len('{0:,}'.format(d_lst[x]['speed'])) > h1:
            h1 = len('{0:,}'.format(d_lst[x]['speed']))
    d_item = None
    while d_item is None:
        scrn(dl['00'], dl['15'])
        ctrt('{0}: {1}'.format(dl['16'], t(d_troop)))
        ctrt(' ')
        dvsn('-')
        ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}} {6:^{7}} {8:^{9}} {10:^{11}} {12:^{13}} {14:^{15}}'.format(
                a, a1, b, b1, c, c1, d, d1, e, e1, f, f1, g, g1, h, h1))
        ctrt('{0}  {1}  {2} {3} {4} {5} {6} {7}'.format(
                '~' * a1, '~' * b1, '~' * c1, '~' * d1, '~' * e1, '~' * f1, '~' * g1, '~' * h1))
        for x in range(len(d_lst)):
            ctrt('{0:<{1}}  {2:^{3},}  {4:>{5},} {6:>{7},} {8:>{9},} {10:>{11},} {12:>{13},} {14:>{15},}'.format(
                    t(d_lst[x]['item']), a1, d_lst[x]['craftable'], b1, d_lst[x]['defense'], c1, d_lst[x]['life'],
                    d1, d_lst[x]['melee'], e1, d_lst[x]['range'], f1, d_lst[x]['range'], g1, d_lst[x]['speed'], h1))
        dvsn()
        d_select = input(' {0} : '.format(dl['17']))
        if len(d_select) >= 1:
            if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                return
            else:
                d_item = chkinp(d_select, slctn)
    d_lst[:] = [d for d in d_lst if d.get('item') == d_item]
    d_attrib, d_stat = [None, None]
    while d_attrib is None:
        scrn(dl['00'], dl['18'])
        ctrt('{0}: {1}   {2}: {3}'.format(dl['16'], t(d_troop), dl['19'], t(d_item)))
        ctrt(' ')
        dvsn('-')
        ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}  {8:^{9}}  {10:^{11}}'.format(
                c, c1, d, d1, e, e1, f, f1, g, g1, h, h1))
        ctrt('{0}  {1}  {2}  {3}  {4}  {5}'.format('~' * c1, '~' * d1, '~' * e1, '~' * f1, '~' * g1, '~' * h1))
        for x in range(len(d_lst)):
            ctrt('{0:^{1},}  {2:^{3},}  {4:^{5},}  {6:^{7},}  {8:^{9},}  {10:^{11},}'.format(
                    d_lst[x]['defense'], c1, d_lst[x]['life'], d1, d_lst[x]['melee'], e1, d_lst[x]['range'], f1,
                    d_lst[x]['range'], g1, d_lst[x]['speed'], h1))
        print('\n {0}'.format(dl['20']))
        dvsn()
        d_select = input(' {0} : '.format(dl['17']))
        if len(d_select) >= 4:
            if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                return
            else:
                try:
                    i_attrib, i_stat = d_select.split('@')
                    if i_stat.isnumeric():
                        if i_attrib.lower() == dl['09'] or i_attrib.lower() == 'defense':
                            d_attrib = 'defense'
                        elif i_attrib.lower() == dl['10'] or i_attrib.lower() == 'life':
                            d_attrib = 'life'
                        elif i_attrib.lower() == dl['11'] or i_attrib.lower() == 'melee':
                            d_attrib = 'melee'
                        elif i_attrib.lower() == dl['12'] or i_attrib.lower() == 'range':
                            d_attrib = 'range'
                        elif i_attrib.lower() == dl['13'] or i_attrib.lower() == 'ranged':
                            d_attrib = 'ranged'
                        elif i_attrib.lower() == dl['14'] or i_attrib.lower() == 'speed':
                            d_attrib = 'speed'
                        d_stat = int(i_stat)
                        break
                except(TypeError, ValueError):
                    sleep(1)
    d_batch = None
    while d_batch is None:
        scrn(dl['00'], dl['21'])
        ctrt('{0}: {1}   {2}: {3}'.format(dl['16'], t(d_troop), dl['19'], t(d_item)))
        ctrt('{0}: {1:,} {2}'.format(dl['22'], d_stat, d_attrib.title()))
        d_batch = stbtch(d_lst[0]['craftable'] + 1, '{0}'.format(dl['23']))
        if d_batch == dl['06'] or d_batch == 'exit':
            return
    d_delay = None
    while d_delay is None:
        scrn(dl['00'], dl['25'])
        ctrt('{0}: {1}   {2}: {3}'.format(dl['16'], t(d_troop), dl['19'], t(d_item)))
        ctrt('{0}: {1:,} {2}   {3}: {4:,}'.format(dl['22'], d_stat, d_attrib.title(), dl['24'], d_batch))
        d_delay = stdly()
        if d_batch == dl['06'] or d_batch == 'exit':
            return
    d_proceed = False
    while not d_proceed:
        scrn(dl['00'], dl['27'])
        ctrt('{0}: {1}   {2}: {3}'.format(dl['16'], t(d_troop), dl['19'], t(d_item)))
        ctrt('{0}: {1:,} {2}   {3}: {4:,}   {5}: {6}s'.format(
                dl['22'], d_stat, d_attrib.title(), dl['24'], d_batch, dl['26'], d_delay))
        d_proceed = prcd()
        if d_proceed == dl['06'] or d_proceed == 'exit':
            return
    d_strt, f_succ, f_fail, len_item, kpt_itm, crsh_itm = [time(), 0, 0, 0, list(), {}]
    for x in range(1, d_batch + 1):
        scrn(dl['00'], dl['28'])
        ctrt('{0}: {1}   {2}: {3}'.format(dl['16'], t(d_troop), dl['19'], t(d_item)))
        ctrt('{0}: {1:,} {2}   {3}: {4:,}   {5}: {6}s   {7}: {8}'.format(
                dl['22'], d_stat, d_attrib.title(), dl['24'], d_batch, dl['26'], d_delay, dl['29'],
                cvttm(time() - d_strt)))
        dvsn('-')
        prg(x, d_batch, '{0}: {1} {2} {3}'.format(dl['30'], x, dl['31'], d_batch),
            '{0}: {1:,}  {2}: {3:,}  {4}: {5:,}  {6}: {7:,}'.format(
                    dl['32'], f_succ, dl['33'], f_fail, dl['34'], len(kpt_itm), dl['35'], f_succ - len(kpt_itm)))
        if kpt_itm:
            ctrt('~~~ {0} ~~~'.format(dl['36']), prefix=True)
            for y in range(len(kpt_itm)):
                k_item = '#{0:<2}: '.format(y + 1) + ', '.join('{0} {1}'.format(
                        k_i.title(), v_i) for k_i, v_i in kpt_itm[y].items())
                if len(k_item) > len_item:
                    len_item = len(k_item)
                ctrt('{0:<{1}}'.format(k_item, len_item))
        if crsh_itm:
            ctrt('~~~ {0} ~~~'.format(dl['37']), prefix=True)
            dsply(crsh_itm, single=False)
        crush_it = False
        x_param = 'output%5Fname={0}&'.format(d_item)
        for web_retry in range(5):
            sleep(d_delay)
            try:
                main_json = web_op('forge/forge_item', x_param)
                result = main_json['result']['success']
                if result:
                    forge_equip = main_json['result']['forge_result']
                    if forge_equip != 'failure':
                        f_succ += 1
                        if d_attrib in forge_equip['stats'].keys() and d_stat <= forge_equip['stats'][d_attrib]:
                            kpt_itm.append(forge_equip['stats'])
                        else:
                            x_param = 'player%5Fforge%5Fequipment%5Fid={0}&'.format(forge_equip['id'])
                            crush_it = True
                    else:
                        f_fail += 1
                    break
            except (KeyError, TypeError):
                sleep(1)
                continue
        else:
            errmsg(dl['38'])
        if crush_it:
            for web_retry in range(5):
                sleep(d_delay)
                try:
                    crush_json = web_op('forge/disenchant_equipment', x_param)
                    result = crush_json['result']['success']
                    if result:
                        for y in range(len(crush_json['result']['disenchanted_ingredients'])):
                            if t(crush_json['result']['disenchanted_ingredients'][y]) in crsh_itm:
                                crsh_itm[t(crush_json['result']['disenchanted_ingredients'][y])] += 1
                            else:
                                crsh_itm[t(crush_json['result']['disenchanted_ingredients'][y])] = 1
                        break
                except (KeyError, TypeError):
                    sleep(1)
                    continue
            else:
                errmsg(dl['39'])
    scrn(dl['00'], dl['40'])
    ctrt('{0}: {1}   {2}: {3}'.format(dl['16'], t(d_troop), dl['19'], t(d_item)))
    ctrt('{0}: {1:,} {2}   {3}: {4:,}   {5}: {6}s   {7}: {8}'.format(
            dl['22'], d_stat, d_attrib.title(), dl['24'], d_batch, dl['26'], d_delay, dl['29'], cvttm(time() - d_strt)))
    dvsn('-')
    prg(1, 1, '{0} {1}'.format(dl['41'], cvttm(time() - d_strt)),
        '{0}: {1:,}  {2}: {3:,}  {4}: {5:,}  {6}: {7:,}'.format(
                dl['32'], f_succ, dl['33'], f_fail, dl['34'], len(kpt_itm), dl['35'], f_succ - len(kpt_itm)))
    if kpt_itm:
        ctrt('~~~ {0} ~~~'.format(dl['36']), prefix=True)
        for y in range(len(kpt_itm)):
            k_item = '#{0:<3}: '.format(y + 1) + ', '.join('{0} {1}'.format(
                    k_i.title(), v_i) for k_i, v_i in kpt_itm[y].items())
            if len(k_item) > len_item:
                len_item = len(k_item)
            ctrt('{0:<{1}}'.format(k_item, len_item))
    if crsh_itm:
        ctrt('~~~ {0} ~~~'.format(dl['37']), prefix=True)
        dsply(crsh_itm, single=False)
    dvsn()
    input(dl['42'])
    print(dl['43'])
    gtdt(pf=True, pl=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def forge_ingredient():
    dl = {'00': lo['a73'], '01': lo['b99'], '02': lo['a92'], '03': lo['c48'], '04': lo['a91'], '05': lo['a13'],
          '06': lo['a77'], '07': lo['a52'], '08': lo['a59'], '09': lo['b32'], '10': lo['a76'], '11': lo['c15'],
          '12': lo['a43'], '13': lo['b57'], '14': lo['b51'], '15': lo['a47'], '16': lo['a78'], '17': lo['a97'],
          '18': lo['b85'], '19': lo['c31'], '20': lo['b49'], '21': lo['b47'], '22': lo['c72'], '23': lo['a88']}
    scrn(dl['00'], dl['01'])
    ctrt(dl['02'])
    d_lst, slctn = [list(), {}]
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
                d_queue = 1024
                d_avail = 0
                for r_item in range(len(ingredients)):
                    if forge_key == ingredients[r_item]['name']:
                        d_avail = ingredients[r_item]['quantity']
                        d_queue = 1024 - d_avail
                if d_queue != 0:
                    count = (len(recipe['items']))
                    for r_key, r_qty in recipe['items'].items():
                        for r_item in range(len(ingredients)):
                            if r_key == ingredients[r_item]['name']:
                                if r_qty < ingredients[r_item]['quantity']:
                                    count -= 1
                                    if d_queue > int(ingredients[r_item]['quantity'] / r_qty):
                                        d_queue = int(ingredients[r_item]['quantity'] / r_qty)
                                else:
                                    break
                    if count == 0:
                        my_dict = {'item': forge_key, 'available': d_avail, 'craftable': d_queue}
                        d_lst.insert(x, my_dict)
    if not d_lst:
        nthng(dl['00'], dl['01'], dl['03'])
        return
    a, b, c = [dl['04'], dl['05'], dl['06']]
    a1, b1, c1 = [len(a), len(b), len(c)]
    for x in range(len(d_lst)):
        if d_lst[x]['item'] not in slctn.keys():
            slctn[d_lst[x]['item']] = t(d_lst[x]['item'])
        if len(t(d_lst[x]['item'])) > a1:
            a1 = len(t(d_lst[x]['item']))
        if len('{0:,}'.format(d_lst[x]['available'])) > b1:
            b1 = len('{0:,}'.format(d_lst[x]['available']))
        if len('{0:,}'.format(d_lst[x]['craftable'])) > c1:
            c1 = len('{0:,}'.format(d_lst[x]['craftable']))
    d_item = None
    while d_item is None:
        scrn(dl['00'], dl['01'])
        ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
        ctrt('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
        for x in range(len(d_lst)):
            ctrt('{0:<{1}}  {2:>{3},}  {4:>{5},}'.format(
                    t(d_lst[x]['item']), a1, d_lst[x]['available'], b1, d_lst[x]['craftable'], c1))
        dvsn()
        d_select = input(' {0} : '.format(dl['07']))
        if d_select.lower() == dl['08'] or d_select.lower() == 'exit':
            return
        else:
            d_item = chkinp(d_select, slctn)
    d_lst[:] = [d for d in d_lst if d.get('item') == d_item]
    d_batch = None
    while d_batch is None:
        scrn(dl['00'], dl['09'])
        ctrt('{0}: {1}'.format(dl['04'], t(d_item)))
        ctrt(' ')
        d_batch = stbtch(d_lst[0]['craftable'] + 1, dl['23'])
        if d_batch == dl['08'] or d_batch == 'exit':
            return
    d_delay = None
    while d_delay is None:
        scrn(dl['00'], dl['11'])
        ctrt('{0}: {1}   {2}: {3:,}'.format(dl['04'], t(d_item), dl['10'], d_batch))
        ctrt(' ')
        d_delay = stdly()
        if d_delay == dl['08'] or d_delay == 'exit':
            return
    d_proceed = False
    while not d_proceed:
        scrn(dl['00'], dl['13'])
        ctrt('{0}: {1}   {2}: {3:,}'.format(dl['04'], t(d_item), dl['10'], d_batch))
        ctrt('{0}: {1}s'.format(dl['12'], d_delay))
        d_proceed = prcd()
        if d_proceed == dl['08'] or d_proceed == 'exit':
            return
    slctn.clear()
    base_list, d_start = [{}, time()]
    for x in range(len(pData['forge']['items']['ingredients'])):
        if t(pData['forge']['items']['ingredients'][x]['name']) not in base_list:
            base_list[t(pData['forge']['items']['ingredients'][x]['name'])] = pData[
                'forge']['items']['ingredients'][x]['quantity']
    for x in range(1, d_batch + 1):
        scrn(dl['00'], dl['14'])
        ctrt('{0}: {1}   {2}: {3:,}'.format(dl['04'], t(d_item), dl['10'], d_batch))
        ctrt('{0}: {1}s   {2}: {3}'.format(dl['12'], d_delay, dl['15'], cvttm(time() - d_start)))
        dvsn('-')
        prg(x, d_batch, '{0}: {1}/{2}'.format(dl['16'], x, d_batch))
        if slctn:
            ctrt('~~~ {0} ~~~'.format(dl['17']), prefix=True)
            dsply(slctn, single=False)
        for web_retry in range(5):
            sleep(d_delay)
            try:
                x_param = 'output%5Fname={0}&'.format(d_item)
                main_json = web_op('forge/forge_item', x_param)
                result = main_json['result']['success']
                if result:
                    check_use = main_json['result']['forge_items']['ingredients']
                    for y in range(len(check_use)):
                        item_name = t(check_use[y]['name'])
                        if item_name in base_list.keys() and check_use[y]['quantity'] < base_list[item_name]:
                            slctn[item_name] = base_list[item_name] - check_use[y]['quantity']
                    break
            except (KeyError, TypeError):
                sleep(1)
                continue
        else:
            errmsg(dl['18'])
    scrn(dl['00'], dl['19'])
    ctrt('{0}: {1}   {2}: {3:,}'.format(dl['04'], t(d_item), dl['10'], d_batch))
    ctrt('{0}: {1}s'.format(dl['12'], d_delay))
    dvsn('-')
    prg(1, 1, '{0} {1}'.format(dl['20'], cvttm(time() - d_start)))
    if slctn:
        ctrt('~~~ {0} ~~~'.format(dl['17']), prefix=True)
        dsply(slctn, single=False)
    dvsn()
    input(dl['21'])
    print(dl['22'])
    gtdt(pf=True, pl=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #


def farm_mission():
    dl = {'00': lo['a61'], '01': lo['c03'], '02': lo['a92'], '03': lo['c44'], '04': lo['b13'], '05': lo['c54'],
          '06': lo['a62'], '07': lo['b17'], '08': lo['a52'], '09': lo['a59'], '10': lo['a20'], '11': lo['a18'],
          '12': lo['a21'], '13': lo['a22'], '14': lo['a23'], '15': lo['b03'], '16': lo['a99'], '17': lo['c21'],
          '18': lo['a83'], '19': lo['a19'], '20': lo['a95'], '21': lo['a44'], '22': lo['a13'], '23': lo['c76'],
          '24': lo['c18'], '25': lo['c51'], '26': lo['a47'], '27': lo['b13'], '28': lo['a03'], '29': lo['b12'],
          '30': lo['b16'], '31': lo['b33'], '32': lo['a87'], '33': lo['c15'], '34': lo['a15'], '35': lo['b51'],
          '36': lo['a43'], '37': lo['a63'], '38': lo['c28'], '39': lo['a96'], '40': lo['b89'], '41': lo['b79'],
          '42': lo['b81'], '43': lo['c31'], '44': lo['b49'], '45': lo['b47'], '46': lo['c72'], '47': lo['b24'],
          '48': lo['a51'], '49': lo['b57'], '50': lo['b94'], '51': lo['a08']}
    scrn(dl['00'], dl['01'])
    ctrt(dl['02'])
    d_lst, slctn, claimed, ingd = [list(), {}, False, {}]
    adv = pData['forge']['adventurers']
    msn = fData['forge']['missions']
    for x in range(len(adv)):
        if adv[x]['current_mission'] is not None:
            x_param = 'adventurer_id={0}&mission_type={1}&'.format(adv[x]['adventurer_id'], adv[x]['current_mission'])
            item_json = web_op('player_missions/claim_mission', x_param)
            if item_json['result']['success']:
                claimed = True
            else:
                slctn[adv[x]['current_mission']] = adv[x]['current_mission']
    if claimed:
        gtdt(dl['00'], pf=True, unmute=False)
        adv = pData['forge']['adventurers']
    for x in range(len(pData['forge']['items']['ingredients'])):
        ingd[pData['forge']['items']['ingredients'][x]['name']] = pData['forge']['items']['ingredients'][x]['quantity']
    for x in range(len(adv)):
        if adv[x]['current_mission'] is None:
            d_level = 0
            for key, value in reversed(
                    sorted(fData['forge']['adventurers'][adv[x]['type']]['level_exp'].items())):
                if adv[x]['experience'] >= value:
                    d_level = int(key) + 1
                    break
            for ms in sorted(msn.keys()):
                checked = False
                d_queue = 9999999
                if ms in slctn.keys():
                    continue
                if d_level < msn[ms]['requirements']['adventurer_level']:
                    continue
                if msn[ms]['ends_at'] != 0 and msn[ms]['ends_at'] < time():
                    continue
                if 'any' not in msn[ms]['adventurers'][0] and adv[x]['type'] not in msn[ms]['adventurers'][0]:
                    continue
                y = len(msn[ms]['requirements']['items'])
                if y > 0:
                    for key, value in (msn[ms]['requirements']['items']).items():
                        if key in ingd.keys():
                            if value < ingd[key]:
                                y -= 1
                                if y == 0:
                                    checked = True
                                if int(ingd[key] / value) < d_queue:
                                    d_queue = int(ingd[key] / value)
                else:
                    checked = True
                if checked:
                    my_dict = {'adventurer': adv[x]['type'], 'id': adv[x]['adventurer_id'], 'time': msn[ms]['cooldown'],
                               'batch': d_queue, 'mission': ms, 'desc': t(ms)}
                    d_lst.append(my_dict)
    if not d_lst:
        nthng(dl['00'], dl['01'], dl['03'])
        return
    else:
        slctn.clear()
        d_lst = sorted(d_lst, key=itemgetter('desc'))
        a, b, c = [dl['04'], dl['05'], dl['06']]
        a1, b1, c1 = [len(a), len(b), len(c)]
        for x in range(len(d_lst)):
            if len(t(d_lst[x]['mission'])) > a1:
                a1 = len(t(d_lst[x]['mission']))
            if len(cvttm(d_lst[x]['time'], ss=False)) > b1:
                b1 = len(cvttm(d_lst[x]['time'], ss=False))
            if len('{0:,}'.format(d_lst[x]['batch'])) > c1:
                c1 = len('{0:,}'.format(d_lst[x]['batch']))
        d_ms = None
        while d_ms is None:
            slctn.clear()
            scrn(dl['00'], dl['01'])
            ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
            ctrt('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
            for x in range(len(d_lst)):
                if d_lst[x]['mission'] not in slctn.keys():
                    slctn[d_lst[x]['mission']] = d_lst[x]['desc']
                    c = dl['07'] if d_lst[x]['batch'] == 9999999 else '{0:,}'.format(d_lst[x]['batch'])
                    ctrt('{0:<{1}}  {2:>{3}}  {4:>{5}}'.format(
                            d_lst[x]['desc'], a1, cvttm(d_lst[x]['time'], ss=False), b1, c, c1))
            dvsn()
            d_select = input(' {0} : '.format(dl['08']))
            if d_select.lower() == dl['09'] or d_select.lower() == 'exit':
                return
            else:
                d_ms = chkinp(d_select, slctn)
    d_lst[:] = [d for d in d_lst if d.get('mission') == d_ms]
    d_tm = d_lst[0]['time']
    slctn.clear()
    for x in range(len(d_lst)):
        if d_lst[x]['adventurer'] not in slctn.keys():
            slctn[d_lst[x]['adventurer']] = t(d_lst[x]['adventurer'])
    if len(slctn) == 1:
        d_adv = d_lst[0]['adventurer']
    else:
        d_adv = None
        while d_adv is None:
            scrn(dl['00'], dl['50'])
            ctrt('{0}: {1} ({2})'.format(dl['04'], t(d_ms), cvttm(d_tm, ss=False)))
            ctrt(' ')
            dvsn('-')
            ctrt('~~~ {0} ~~~'.format(dl['51']))
            dsply(slctn)
            dvsn()
            d_select = input(' {0} : '.format(dl['08']))
            if d_select.lower() == dl['09'] or d_select.lower() == 'exit':
                return
            else:
                d_adv = chkinp(d_select, slctn)
    d_lst[:] = [d for d in d_lst if d.get('adventurer') == d_adv]
    spd_itm = [{'item': 'Blitz', 'exceed': 216000, 'time': 345600, 'desc': dl['10']},
               {'item': 'Blast', 'exceed': 86400, 'time': 216000, 'desc': dl['11']},
               {'item': 'Bolt', 'exceed': 54000, 'time': 86400, 'desc': dl['12']},
               {'item': 'Bore', 'exceed': 28800, 'time': 54000, 'desc': dl['13']},
               {'item': 'Bounce', 'exceed': 9000, 'time': 28800, 'desc': dl['14']},
               {'item': 'Leap', 'exceed': 3600, 'time': 9000, 'desc': dl['15']},
               {'item': 'Jump', 'exceed': 900, 'time': 3600, 'desc': dl['16']},
               {'item': 'Skip', 'exceed': 300, 'time': 900, 'desc': dl['17']},
               {'item': 'Hop', 'exceed': 60, 'time': 300, 'desc': dl['18']},
               {'item': 'Blink', 'exceed': 0, 'time': 60, 'desc': dl['19']}]
    d_speed = list()
    a, b, c, d = [dl['20'], dl['21'], dl['22'], dl['23']]
    a1, b1, c1, d1 = [len(a), len(b), len(c), len(d)]
    for key in range(len(spd_itm)):
        look_up = spd_itm[key]
        if look_up['item'] in pData['items'] and pData['items'][look_up['item']] > 0:
            if len(look_up['desc']) > a1:
                a1 = len(look_up['desc'])
            if len(cvttm(look_up['time'], ss=False)) > b1:
                b1 = len(cvttm(look_up['time'], ss=False))
            if len('{0:,}'.format(pData['items'][look_up['item']])) > c1:
                c1 = len('{0:,}'.format(pData['items'][look_up['item']]))
            my_dict = {'item': look_up['item'], 'desc': t(look_up['item']), 'use': 0,
                       'time': look_up['time'], 'qty': pData['items'][look_up['item']]}
            d_speed.append(my_dict)
    if not d_speed:
        nthng(dl['00'], dl['24'], dl['25'])
        return
    else:
        while True:
            scrn(dl['00'], dl['24'])
            ctrt('{0}: {1} ({2})   {3}: {4}'.format(dl['27'], t(d_ms), cvttm(d_tm, ss=False), dl['28'], t(d_adv)))
            ctrt(' ')
            dvsn('-')
            ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}'.format(a, a1, b, b1, c, c1, d, d1))
            ctrt('{0}  {1}  {2}  {3}'.format('~' * a1, '~' * b1, '~' * c1, '~' * d1))
            reduced_time = d_lst[0]['time']
            for key in range(len(d_speed)):
                ctrt('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}'.format(
                        d_speed[key]['desc'], a1, cvttm(d_speed[key]['time'], ss=False), b1,
                        d_speed[key]['qty'], c1, d_speed[key]['use'], d1))
                if d_speed[key]['use']:
                    reduced_time -= d_speed[key]['time'] * d_speed[key]['use']
                    reduced_time = 0 if reduced_time <= 0 else reduced_time
            ctrt('{0}: {1}'.format(dl['29'], cvttm(reduced_time, ss=False)), prefix=True, suffix=True)
            print(' {0}'.format(dl['47'])) if reduced_time != 0 else print(' {0}'.format(dl['48']))
            dvsn()
            d_select = input(' {0} : '.format(dl['08']))
            if d_select.lower() == dl['09'] or d_select.lower() == 'exit':
                return
            elif reduced_time == 0 and (d_select.lower() == dl['30'] or d_select.lower() == 'next'):
                break
            else:
                try:
                    i_item, i_qty = d_select.split('@')
                    if i_qty.isnumeric():
                        for x in range(len(d_speed)):
                            if i_item.lower() == d_speed[x]['desc'].lower() and int(i_qty) < d_speed[x]['qty']:
                                d_speed[x]['use'] = int(i_qty)
                                break
                        else:
                            for x in range(len(d_speed)):
                                if i_item.lower() in d_speed[x]['desc'].lower() and int(i_qty) < d_speed[x]['qty']:
                                    d_speed[x]['use'] = int(i_qty)
                                    break
                except(TypeError, ValueError):
                    pass
    d_speed[:] = [d for d in d_speed if d.get('use') != 0]
    d_queue = d_lst[0]['batch']
    for x in range(len(d_speed)):
        if d_queue > int(d_speed[x]['qty'] / d_speed[x]['use']):
            d_queue = int(d_speed[x]['qty'] / d_speed[x]['use'])
    d_batch = 1 if d_queue == 1 else None
    while d_batch is None:
        scrn(dl['00'], dl['31'])
        ctrt('{0}: {1} ({2})   {3}: {4}'.format(dl['27'], t(d_ms), cvttm(d_tm, ss=False), dl['28'], t(d_adv)))
        ctrt(' ')
        d_batch = stbtch(d_queue + 1, dl['32'])
        if d_batch == dl['09'] or d_batch == 'exit':
            return
    d_delay = None
    while d_delay is None:
        scrn(dl['00'], dl['33'])
        ctrt('{0}: {1} ({2})   {3}: {4}'.format(dl['27'], t(d_ms), cvttm(d_tm, ss=False), dl['28'], t(d_adv)))
        ctrt('{0}: {1:,}'.format(dl['34'], d_batch))
        d_delay = stdly()
        if d_delay == dl['09'] or d_delay == 'exit':
            return
    d_proceed = False
    while not d_proceed:
        scrn(dl['00'], dl['49'])
        ctrt('{0}: {1} ({2})   {3}: {4}'.format(dl['27'], t(d_ms), cvttm(d_tm, ss=False), dl['28'], t(d_adv)))
        ctrt('{0}: {1:,}   {2}: {3}s'.format(dl['34'], d_batch, dl['36'], d_delay))
        d_proceed = prcd()
        if d_proceed == dl['09'] or d_proceed == 'exit':
            return
    d_start = time()
    spd_use, itm_gain = [{}, {}]
    for x in range(d_batch):
        job_id = 0
        dur = -1
        for item in d_speed:
            for y in range(item['use']):
                if dur == 0 and y < item['use'] - 1:
                    break
                scrn(dl['00'], dl['35'])
                ctrt('{0}: {1} ({2})   {3}: {4}'.format(dl['27'], t(d_ms), cvttm(d_tm, ss=False), dl['28'], t(d_adv)))
                ctrt('{0}: {1:,}   {2}: {3}s   {4}: {5}'.format(
                        dl['34'], d_batch, dl['36'], d_delay, dl['26'], cvttm(time() - d_start)))
                dvsn('-')
                prg(x + 1, d_batch, '{0}: {1}/{2}'.format(dl['37'], x + 1, d_batch))
                if spd_use:
                    ctrt('~~~ {0} ~~~'.format(dl['38']), prefix=True)
                    dsply(spd_use, single=False)
                if itm_gain:
                    ctrt('~~~ {0} ~~~'.format(dl['39']), prefix=True)
                    dsply(itm_gain, single=False)
                if dur == -1:
                    for web_retry in range(5):
                        sleep(d_delay)
                        x_param = 'adventurer_id={0}&mission_type={1}&'.format(d_lst[0]['id'], d_ms)
                        try:
                            main_json = web_op('player_missions', x_param)
                            result = main_json['result']['success']
                            if result:
                                dur = int(main_json['result']['job']['duration'])
                                job_id = main_json['result']['job']['id']
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
                    else:
                        errmsg(dl['40'])
                if dur > 0:
                    for web_retry in range(5):
                        sleep(d_delay)
                        x_param = '%5Fmethod=delete&job%5Fid={0}&'.format(job_id)
                        try:
                            item_json = web_op('player_items/{0}'.format(item['item']), x_param)
                            result = item_json['result']['success']
                            if result:
                                dur = int(item_json['result']['item_response']['run_at'] - item_json['timestamp'])
                                if dur < 0:
                                    dur = 0
                                if t(item['item']) in spd_use:
                                    spd_use[t(item['item'])] += 1
                                else:
                                    spd_use[t(item['item'])] = 1
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
                    else:
                        errmsg(dl['41'])
                if dur == 0:
                    for web_retry in range(5):
                        sleep(d_delay)
                        x_param = 'adventurer_id={0}&mission_type={1}&'.format(d_lst[0]['id'], d_ms)
                        try:
                            claim_json = web_op('player_missions/claim_mission', x_param)
                            result = claim_json['result']['success']
                            if result:
                                for z in range(len(claim_json['result']['items'])):
                                    if t(claim_json['result']['items'][z]) in itm_gain:
                                        itm_gain[t(claim_json['result']['items'][z])] += 1
                                    else:
                                        itm_gain[t(claim_json['result']['items'][z])] = 1
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
                    else:
                        errmsg(dl['42'])
    scrn(dl['00'], dl['43'])
    ctrt('{0}: {1} ({2})   {3}: {4}'.format(dl['27'], t(d_ms), cvttm(d_tm, ss=False), dl['28'], t(d_adv)))
    ctrt('{0}: {1:,}   {2}: {3}s'.format(dl['34'], d_batch, dl['36'], d_delay))
    dvsn('-')
    prg(1, 1, '{0} {1}'.format(dl['44'], cvttm(time() - d_start)))
    if spd_use:
        ctrt('~~~ {0} ~~~'.format(dl['38']), prefix=True)
        dsply(spd_use, single=False)
    if itm_gain:
        ctrt('~~~ {0} ~~~'.format(dl['39']), prefix=True)
        dsply(itm_gain, single=False)
    dvsn()
    input(dl['45'])
    print(dl['46'])
    gtdt(pf=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                      CHEST CLASS                                                     #
# -------------------------------------------------------------------------------------------------------------------- #
def open_chest():
    dl = {'00': lo['b36'], '01': lo['b97'], '02': lo['a92'], '03': lo['c46'], '04': lo['a27'], '05': lo['c72'],
          '06': lo['b52'], '07': lo['b38'], '08': lo['c85'], '09': lo['b19'], '10': lo['b23'], '11': lo['a48'],
          '12': lo['a51'], '13': lo['a52'], '14': lo['a59'], '15': lo['b16'], '16': lo['a04'], '17': lo['b20'],
          '18': lo['c68'], '19': lo['c14'], '20': lo['c57'], '21': lo['a86'], '22': lo['c15'], '23': lo['b37'],
          '24': lo['a43'], '25': lo['b57'], '26': lo['b51'], '27': lo['a06'], '28': lo['c29'], '29': lo['c41'],
          '30': lo['a82'], '31': lo['b40'], '32': lo['b51'], '33': lo['a47'], '34': lo['b41'], '35': lo['a38'],
          '36': lo['b39'], '37': lo['b88'], '38': lo['c31'], '39': lo['b49'], '40': lo['b47']}
    scrn(dl['00'], dl['01'])
    ctrt(dl['02'])
    d_lst, slctn, max_len = [list(), {}, 0]
    for key, value in pData['items'].items():
        if 'ConfigurableChest' in key and value != 0:
            max_qty = 0
            for manifest in range(len(mData['store']['chest'])):
                if key in mData['store']['chest'][manifest]['type']:
                    max_qty = mData['store']['chest'][manifest]['max_use_quantity']
                    break
            max_len = len(str(value)) if max_len < len(str(value)) else max_len
            my_dict = {'chest': key, 'desc': t(key), 'qty': value, 'max_use': max_qty, 'open': False}
            d_lst.append(my_dict)

    if not d_lst:
        nthng(dl['00'], dl['01'], dl['03'])
        return
    else:
        d_lst = sorted(d_lst, key=itemgetter('desc'))
        if len(d_lst) == 1:
            d_lst[0]['open'] = True
        else:
            a, b, c = [dl['04'], dl['06'], dl['07']]
            a1, b1, c1 = [len(a), len(b), len(c)]
            for x in range(len(d_lst)):
                if len(d_lst[x]['desc']) > a1:
                    a1 = len(d_lst[x]['desc'])
                if len('{0:,}'.format(d_lst[x]['qty'])) > b1:
                    b1 = len('{0:,}'.format(d_lst[x]['qty']))
                if len('{0}'.format(dl['08'])) > c1:
                    c1 = len('{0}'.format(dl['08']))
                if len('{0}'.format(dl['09'])) > c1:
                    c1 = len('{0}'.format(dl['09']))
            while True:
                scrn(dl['00'], dl['01'])
                ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
                ctrt('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
                selected = False
                for x in range(len(d_lst)):
                    d = dl['08'].title() if d_lst[x]['open'] else dl['09'].title()
                    if d_lst[x]['open']:
                        selected = True
                    ctrt('{0:<{1}}  {2:>{3},}  {4:>{5}}'.format(d_lst[x]['desc'], a1, d_lst[x]['qty'], b1, d, c1))
                if not selected:
                    print('\n {0}'.format(dl['10']))
                    print('       {0}'.format(dl['11']))
                else:
                    print('\n {0}\n'.format(dl['12']))
                dvsn()
                d_select = input(' {0} : '.format(dl['13']))
                if len(d_select) >= 3:
                    if d_select.lower() == dl['14'] or d_select.lower() == 'exit':
                        return
                    elif selected and (d_select.lower() == dl['15'] or d_select.lower() == 'next'):
                        break
                    elif d_select.lower() == dl['16'] or d_select.lower() == 'all':
                        for x in range(len(d_lst)):
                            d_lst[x]['open'] = True
                    elif d_select.lower() == dl['17'] or d_select.lower() == 'none':
                        for x in range(len(d_lst)):
                            d_lst[x]['open'] = False
                    else:
                        for x in range(len(d_lst)):
                            if d_select.lower() == t(d_lst[x]['chest']).lower():
                                d_lst[x]['open'] = False if d_lst[x]['open'] else True
                                break
                        else:
                            for x in range(len(d_lst)):
                                if d_select.lower() in t(d_lst[x]['chest']).lower():
                                    d_lst[x]['open'] = False if d_lst[x]['open'] else True
    d_lst[:] = [d for d in d_lst if d.get('open') == True]
    d_batch = None
    if len(d_lst) == 1:
        d_chest = '{0}: {1}'.format(dl['04'], t(d_lst[0]['chest']))
        d_total = d_lst[0]['qty']
        if d_total == 1:
            d_batch = 1
        max_chest = d_lst[0]['qty']
        if max_chest > d_lst[0]['max_use']:
            max_chest = d_lst[0]['max_use']
    else:
        d_chest = '{0}: {1}'.format(dl['18'], len(d_lst))
        d_total, max_chest = [0, 0]
        for x in range(len(d_lst)):
            d_total += d_lst[x]['qty']
            if max_chest < d_lst[x]['qty']:
                max_chest = d_lst[x]['qty']
            if max_chest > d_lst[x]['max_use']:
                max_chest = d_lst[x]['max_use']
    while d_batch is None:
        scrn(dl['00'], dl['19'])
        ctrt('{0}   {1}: {2:,}'.format(d_chest, dl['20'], d_total))
        ctrt(' ')
        d_batch = stbtch(max_chest + 1, dl['21'])
        if d_batch == dl['14'] or d_batch == 'exit':
            return
    d_delay = None
    while d_delay is None:
        scrn(dl['00'], dl['22'])
        ctrt('{0}   {1}: {2:,}'.format(d_chest, dl['20'], d_total))
        ctrt('{0}: {1}'.format(dl['23'], d_batch))
        d_delay = stdly()
        if d_delay == dl['14'] or d_delay == 'exit':
            return
    d_proceed = False
    while not d_proceed:
        scrn(dl['00'], dl['25'])
        ctrt('{0}   {1}: {2:,}'.format(d_chest, dl['20'], d_total))
        ctrt('{0}: {1}   {2}: {3}s'.format(dl['23'], d_batch, dl['24'], d_delay))
        d_proceed = prcd()
        if d_proceed == dl['14'] or d_proceed == 'exit':
            return
    scrn(dl['00'], dl['26'])
    ctrt('{0}   {1}: {2:,}'.format(d_chest, dl['20'], d_total))
    ctrt('{0}: {1}   {2}: {3}s'.format(dl['23'], d_batch, dl['24'], d_delay))
    dvsn('-')
    prg(0, 1, dl['02'])
    slctn.clear()
    d_start, ttl_open = [time(), 0]
    look_up = pData['items']
    o_rcvd = {dl['04']: {}, dl['27']: {}, dl['28']: {}, dl['29']: {}, dl['30']: {}, dl['31']: {}}
    spd_itms = ('Hop', 'TranceMarchDrops', 'ForcedMarchDrops', 'TranceMarchElixir', 'Godspeed', 'Bounce', 'Skip',
                'Jump', 'Leap', 'Bore', 'Bolt', 'Blast', 'Blitz', 'Blink')
    for x in range(len(d_lst)):
        i_received = {dl['04']: {}, dl['27']: {}, dl['28']: {}, dl['29']: {}, dl['30']: {}, dl['31']: {}}
        opened, count = [d_lst[x]['qty'], 0]
        open_qty = d_batch if d_lst[x]['max_use'] >= d_batch else d_lst[x]['max_use']
        open_qty = d_lst[x]['qty'] if d_lst[x]['qty'] <= open_qty else open_qty
        while opened != 0:
            if opened < open_qty:
                open_qty = opened
            for web_retry in range(5):
                sleep(d_delay)
                try:
                    x_param = '%5Fmethod=delete&quantity={0}&'.format(open_qty)
                    main_data = web_op('player_items/{0}'.format(d_lst[x]['chest']), x_param)
                    result = main_data['result']['success']
                    if result:
                        opened -= open_qty
                        count += open_qty
                        ttl_open += open_qty
                        for key, value in main_data['result']['items'].items():
                            if 'Chest' in key:
                                if key in look_up.keys() and value > look_up[key]:
                                    i_received[dl['04']][t(key)] = value - look_up[key]
                                if key not in look_up.keys():
                                    i_received[dl['04']][t(key)] = value
                            elif 'TroopPrize' in key:
                                if key in look_up.keys() and value > look_up[key]:
                                    i_received[dl['27']][t(key)] = value - look_up[key]
                                if key not in look_up.keys():
                                    i_received[dl['27']][t(key)] = value
                            elif 'Seal' in key or 'Grant' in key:
                                if key in look_up.keys() and value > look_up[key]:
                                    i_received[dl['30']][t(key)] = value - look_up[key]
                                if key not in look_up.keys():
                                    i_received[dl['30']][t(key)] = value
                            elif 'Testronius' in key:
                                if key in look_up.keys() and value > look_up[key]:
                                    i_received[dl['29']][t(key)] = value - look_up[key]
                                if key not in look_up.keys():
                                    i_received[dl['29']][t(key)] = value
                            elif key in spd_itms:
                                if key in look_up.keys() and value > look_up[key]:
                                    i_received[dl['28']][t(key)] = value - look_up[key]
                                if key not in look_up.keys():
                                    i_received[dl['28']][t(key)] = value
                            else:
                                if key in look_up.keys() and value > look_up[key]:
                                    i_received[dl['31']][t(key)] = value - look_up[key]
                                if key not in look_up.keys():
                                    i_received[dl['31']][t(key)] = value
                        scrn(dl['00'], dl['32'])
                        ctrt('{0}   {1}: {2:,}'.format(d_chest, dl['20'], d_total))
                        ctrt('{0}: {1}   {2}: {3}s   {4}: {5}'.format(
                                dl['23'], d_batch, dl['24'], d_delay, dl['33'], cvttm(time() - d_start)))
                        dvsn('-')
                        if len(d_lst) > 1:
                            prg(ttl_open, d_total, '{0}: {1:,}/{2:,}'.format(dl['34'], ttl_open, d_total))
                            prg(count, d_lst[x]['qty'], '{0}: {1}'.format(dl['35'], t(d_lst[x]['chest'])),
                                '{0}: {1:,}/{2:,}'.format(dl['36'], count, d_lst[x]['qty']))
                        else:
                            prg(count, d_lst[x]['qty'], '{0} {1:,}/{2:,}'.format(dl['36'], count, d_lst[x]['qty']))
                        for category in (dl['04'], dl['27'], dl['28'], dl['29'], dl['30'], dl['31']):
                            if len(i_received[category]) > 0:
                                slctn = i_received[category]
                                ctrt('~~~ {0} ~~~'.format(category.title()), prefix=True)
                                dsply(slctn, single=False)
                        if count == d_lst[x]['qty']:
                            look_up = main_data['result']['items']
                        break
                except (KeyError, TypeError):
                    sleep(1)
                    continue
            else:
                errmsg(dl['37'])
        for category in (dl['04'], dl['27'], dl['28'], dl['29'], dl['30'], dl['31']):
            for key, value in i_received[category].items():
                if key in o_rcvd[category].keys():
                    o_rcvd[category][key] += value
                else:
                    o_rcvd[category][key] = value
    scrn(dl['00'], dl['38'])
    ctrt('{0}   {1}: {2:,}'.format(d_chest, dl['20'], d_total))
    ctrt('{0}: {1}   {2}: {3}s'.format(dl['23'], d_batch, dl['24'], d_delay))
    dvsn('-')
    prg(1, 1, '{0} {1}'.format(dl['39'], cvttm(time() - d_start)))
    for category in (dl['04'], dl['27'], dl['28'], dl['29'], dl['30'], dl['31']):
        if len(o_rcvd[category]) > 0:
            slctn = o_rcvd[category]
            ctrt('~~~ {0} ~~~'.format(category.title()), prefix=True)
            dsply(slctn, single=False)
    dvsn()
    input(dl['40'])
    print(dl['05'])
    gtdt(pf=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def unpack_arsenal():
    dl = {'00': lo['c69'], '01': lo['c08'], '02': lo['a92'], '03': lo['a66'], '04': lo['a71'], '05': lo['b35'],
          '06': lo['c36'], '07': lo['a65'], '08': lo['c53'], '09': lo['c64'], '10': lo['c56'], '11': lo['b44'],
          '12': lo['a52'], '13': lo['a59'], '14': lo['c67'], '15': lo['b52'], '16': lo['b44'], '17': lo['b38'],
          '18': lo['b95'], '19': lo['c65'], '20': lo['c85'], '21': lo['b19'], '22': lo['b21'], '23': lo['a51'],
          '24': lo['a59'], '25': lo['a04'], '26': lo['b20'], '27': lo['b16'], '28': lo['a16'], '29': lo['a17'],
          '30': lo['b90'], '31': lo['c19'], '32': lo['a89'], '33': lo['c70'], '34': lo['c15'], '35': lo['b57'],
          '36': lo['a43'], '37': lo['b51'], '38': lo['a47'], '39': lo['c71'], '40': lo['b45'], '41': lo['c31'],
          '42': lo['b49'], '43': lo['b47'], '44': lo['c72']}
    scrn(dl['00'], dl['01'])
    ctrt(dl['02'])
    d_lst, slctn, m_use_qty = [list(), {}, 0]
    for key, value in sorted(pData['items'].items()):
        for manifest in range(len(mData['store']['arsenal'])):
            if key in mData['store']['arsenal'][manifest]['type']:
                m_use_qty = mData['store']['arsenal'][manifest]['max_use_quantity']
                break
        if 'TroopPrizeItem' in key and value > 0:
            for x in range(len(mData['units'])):
                if key.startswith(mData['units'][x]['type']):
                    if '50TroopPrizeItem' in key:
                        bin_desc, bin_type = [dl['03'], 50]
                    elif '500TroopPrizeItem' in key:
                        bin_desc, bin_type = [dl['04'], 500]
                    elif '1000TroopPrizeItem' in key:
                        bin_desc, bin_type = [dl['05'], 1000]
                    elif '10kTroopPrizeItem' in key:
                        bin_desc, bin_type = [dl['06'], 10000]
                    elif '50kTroopPrizeItem' in key:
                        bin_desc, bin_type = [dl['07'], 50000]
                    else:
                        continue
                    my_dict = {'trp': mData['units'][x]['type'], 'dsc': t(mData['units'][x]['type']), 'b': key,
                               'qty': value, 'pwr': mData['units'][x]['stats']['power'], 'b_dsc': bin_desc,
                               'b_typ': bin_type, 'm_use': m_use_qty, 'use': False}
                    d_lst.append(my_dict)
    if not d_lst:
        nthng(dl['00'], dl['01'], dl['08'])
        return
    if len(d_lst) == 1:
        d_troop = d_lst[0]['trp']
    else:
        d_troop = None
        a, b, c = [dl['09'], dl['10'], dl['11']]
        a1, b1, c1 = [len(a), len(b), len(c)]
        for x in range(len(d_lst)):
            if d_lst[x]['dsc'] not in slctn.keys():
                my_dict = {'ttl': d_lst[x]['qty'], 'gain': d_lst[x]['qty'] * d_lst[x]['b_typ'] * d_lst[x]['pwr']}
                slctn[d_lst[x]['dsc']] = my_dict
            else:
                slctn[d_lst[x]['dsc']]['ttl'] += d_lst[x]['qty']
                slctn[d_lst[x]['dsc']]['gain'] += (d_lst[x]['qty'] * d_lst[x]['b_typ'] * d_lst[x]['pwr'])
            if len(d_lst[x]['dsc']) > a1:
                a1 = len(d_lst[x]['dsc'])
            if len('{0:,}'.format(slctn[d_lst[x]['dsc']]['ttl'])) > b1:
                b1 = len('{0:,}'.format(slctn[d_lst[x]['dsc']]['ttl']))
            if len('{0:,}'.format(slctn[d_lst[x]['dsc']]['gain'])) > c1:
                c1 = len('{0:,}'.format(slctn[d_lst[x]['dsc']]['gain']))
        while not d_troop:
            scrn(dl['00'], dl['01'])
            ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
            ctrt('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
            for key in sorted(slctn):
                ctrt('{0:<{1}}  {2:>{3},}  {4:>{5},}'.format(key, a1, slctn[key]['ttl'], b1, slctn[key]['gain'], c1))
            dvsn()
            d_select = input(' {0} : '.format(dl['12']))
            if d_select.lower() == dl['13'] or d_select.lower() == 'exit':
                return
            else:
                for key in slctn:
                    if d_select.lower() == key.lower():
                        d_troop = key
                        break
                else:
                    for key in slctn:
                        if d_select.lower() in key.lower():
                            d_troop = key
                            break
    d_lst[:] = [d for d in d_lst if d.get('dsc') == d_troop]
    if len(d_lst) == 1:
        d_lst[0]['use'] = True
    else:
        a, b, c, d = [dl['14'], dl['15'], dl['16'], dl['17']]
        a1, b1, c1, d1 = [len(a), len(b), len(c), len(d)]
        for x in range(len(d_lst)):
            if len('{0}'.format(d_lst[x]['b_dsc'])) > a1:
                a1 = len('{0}'.format(d_lst[x]['b_dsc']))
            if len('{0:,}'.format(d_lst[x]['qty'])) > b1:
                b1 = len('{0:,}'.format(d_lst[x]['qty']))
            if len('{0:,}'.format(d_lst[x]['b_typ'] * d_lst[x]['qty'] * d_lst[x]['pwr'])) > c1:
                c1 = len('{0:,}'.format(d_lst[x]['b_typ'] * d_lst[x]['qty'] * d_lst[x]['pwr']))
        selected = False
        while not selected:
            scrn(dl['00'], dl['18'])
            ctrt('{0}: {1}'.format(dl['19'], t(d_troop)))
            ctrt(' ')
            dvsn('-')
            ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}'.format(a, a1, b, b1, c, c1, d, d1))
            ctrt('{0}  {1}  {2}  {3}'.format('~' * a1, '~' * b1, '~' * c1, '~' * d1))
            gtg = False
            for x in range(len(d_lst)):
                e = '{0:,}'.format(d_lst[x]['b_typ'] * d_lst[x]['qty'] * d_lst[x]['pwr'])
                if d_lst[x]['use']:
                    f = dl['20'].title()
                    gtg = True
                else:
                    f = dl['21'].title()
                ctrt('{0:<{1}}  {2:>{3},}  {4:>{5}}  {6:>{7}}'.format(
                        d_lst[x]['b_dsc'], a1, d_lst[x]['qty'], b1, e, c1, f, d1))
            if not gtg:
                print('\n {0}'.format(dl['22']))
            else:
                print('\n {0}'.format(dl['23']))
            dvsn()
            d_select = input(' {0} : '.format(dl['12']))
            if d_select.lower() == dl['24'] or d_select.lower() == 'exit':
                return
            elif d_select.lower() == dl['25'] or d_select.lower() == 'all':
                for x in range(len(d_lst)):
                    d_lst[x]['use'] = True
            elif d_select.lower() == dl['26'] or d_select.lower() == 'none':
                for x in range(len(d_lst)):
                    d_lst[x]['use'] = False
            elif (d_select.lower() == dl['27'] or d_select.lower() == 'next') and gtg is True:
                selected = True
            else:
                for x in range(len(d_lst)):
                    if d_select.lower() == d_lst[x]['b_dsc'].lower():
                        d_lst[x]['use'] = True if not d_lst[x]['use'] else False
                        break
                else:
                    for x in range(len(d_lst)):
                        if d_select.lower() in d_lst[x]['b_dsc'].lower():
                            d_lst[x]['use'] = True if not d_lst[x]['use'] else False
    d_lst[:] = [d for d in d_lst if d.get('use') == True]
    if len(d_lst) > 1:
        d_bin_type = '{0} {1}'.format(len(d_lst), dl['28'])
        d_batch = 0
        for x in range(len(d_lst)):
            d_batch += d_lst[x]['qty']
    else:
        d_batch = None
        d_bin_type = '{0:,} {1}'.format(d_lst[0]['b_typ'], dl['29'])
        # Set Number Of Batches
        while d_batch is None:
            scrn(dl['00'], dl['31'])
            ctrt('{0}: {1}   {2}: {3}'.format(dl['19'], t(d_troop), dl['29'], d_bin_type))
            ctrt(' ')
            d_batch = stbtch(d_lst[0]['qty'] + 1, dl['32'])
            if d_batch == dl['13'] or d_batch == 'exit':
                return
    d_delay = None
    while d_delay is None:
        scrn(dl['00'], dl['34'])
        ctrt('{0}: {1}   {2}: {3}'.format(dl['19'], t(d_troop), dl['29'], d_bin_type))
        ctrt('{0}: {1:,}'.format(dl['33'], d_batch))
        d_delay = stdly()
        if d_delay == dl['13'] or d_delay == 'exit':
            return
    d_proceed = False
    while not d_proceed:
        scrn(dl['00'], dl['35'])
        ctrt('{0}: {1}   {2}: {3}'.format(dl['19'], t(d_troop), dl['29'], d_bin_type))
        ctrt('{0}: {1:,}   {2}: {3}s'.format(dl['33'], d_batch, dl['36'], d_delay))
        d_proceed = prcd()
        if d_proceed == dl['13'] or d_proceed == 'exit':
            return
    scrn(dl['00'], dl['37'])
    ctrt('{0}: {1}   {2}: {3}'.format(dl['19'], t(d_troop), dl['29'], d_bin_type))
    ctrt('{0}: {1:,}   {2}: {3}s'.format(dl['33'], d_batch, dl['36'], d_delay))
    dvsn('-')
    prg(0, 1, dl['02'])
    d_start = time()
    total_opened = 0
    d_power = 0
    for x in range(len(d_lst)):
        current_opened = 0
        if len(d_lst) > 1:
            d_quantity = d_lst[x]['qty']
        else:
            d_quantity = d_batch
        open_quantity = d_lst[x]['m_use']
        while d_quantity != 0:
            scrn(dl['00'], dl['37'])
            ctrt('{0}: {1}   {2}: {3}'.format(dl['19'], t(d_troop), dl['29'], d_bin_type))
            ctrt('{0}: {1:,}   {2}: {3}s   {4}: {5}'.format(
                    dl['33'], d_batch, dl['36'], d_delay, dl['38'], cvttm(time() - d_start)))
            dvsn('-')
            prg(total_opened, d_batch, '{0}: {1:,}/{2:,}'.format(dl['39'], total_opened, d_batch))
            if len(d_lst) > 1:
                prg(current_opened, d_lst[x]['qty'], '{0} {1}'.format(dl['39'], t(d_lst[x]['b'])))
            ctrt('~~~ {0} ~~~'.format(dl['40']), prefix=True)
            ctrt('{0:,}'.format(d_power))
            if d_quantity < open_quantity:
                open_quantity = d_quantity
            for web_retry in range(5):
                sleep(d_delay)
                try:
                    x_param = '%5Fmethod=delete&quantity={0}&'.format(open_quantity)
                    main_json = web_op('player_items/{0}.json'.format(d_lst[x]['b']), x_param)
                    result = main_json['result']['success']
                    if result:
                        total_opened += open_quantity
                        current_opened += open_quantity
                        d_quantity -= open_quantity
                        d_power += (open_quantity * d_lst[x]['b_typ']) * d_lst[x]['pwr']
                        break
                except (KeyError, TypeError):
                    sleep(1)
                    continue
            else:
                errmsg(dl['30'])
    scrn(dl['00'], dl['41'])
    ctrt('{0}: {1}   {2}: {3}'.format(dl['19'], t(d_troop), dl['29'], d_bin_type))
    ctrt('{0}: {1:,}   {2}: {3}s'.format(dl['33'], d_batch, dl['36'], d_delay))
    dvsn('-')
    prg(1, 1, '{0} {1}'.format(dl['42'], cvttm(time() - d_start)))
    ctrt('~~~ {0} ~~~'.format(dl['40']), prefix=True)
    ctrt('{0:,}'.format(d_power))
    dvsn()
    input(dl['43'])
    print(dl['44'])
    gtdt(pf=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #


def fill_slot():
    dl = {'00': lo['a69'], '01': lo['c02'], '02': lo['a92'], '03': lo['c50'], '04': lo['b07'], '05': lo['a30'],
          '06': lo['a64'], '07': lo['a52'], '08': lo['a59'], '09': lo['a26'], '10': lo['c54'], '11': lo['c24'],
          '12': lo['b96'], '13': lo['c22'], '14': lo['a11'], '15': lo['b68'], '16': lo['b69'], '17': lo['b67'],
          '18': lo['b66'], '19': lo['b70'], '20': lo['a95'], '21': lo['a44'], '22': lo['a13'], '23': lo['a02'],
          '24': lo['c76'], '25': lo['a20'], '26': lo['a18'], '27': lo['a21'], '28': lo['a22'], '29': lo['a23'],
          '30': lo['b03'], '31': lo['a99'], '32': lo['c21'], '33': lo['a83'], '34': lo['a19'], '35': lo['c06'],
          '36': lo['c23'], '37': lo['b28'], '38': lo['a49'], '39': lo['a50'], '40': lo['a01'], '41': lo['b16'],
          '42': lo['a04'], '43': lo['b20'], '44': lo['a25'], '45': lo['c15'], '46': lo['a43'], '47': lo['b57'],
          '48': lo['b51'], '49': lo['a47'], '50': lo['a70'], '51': lo['c28'], '52': lo['c79'], '53': lo['b83'],
          '54': lo['b79'], '55': lo['c31'], '56': lo['b49'], '57': lo['a97'], '58': lo['b71'], '59': lo['b47'],
          '60': lo['c72'], '61': lo['c85'], '62': lo['b19']}
    bldg_dict = {
        'capital': {
            'fs': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 32, 9: 35, 10: 38, 11: 39},
            'cs': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 32}},
        'cave': {
            'fs': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
            'cs': {1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8, 9: 8, 10: 8, 11: 8, 12: 8, 13: 8, 14: 13, 15: 8}},
        'chrono': {
            'fs': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30},
            'cs': {1: 29, 2: 29, 3: 29, 4: 29, 5: 29, 6: 29, 7: 29, 8: 29, 9: 29, 10: 29, 11: 29, 12: 29}},
        'colossus': {
            'fs': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
            'cs': {1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10, 10: 10, 11: 10, 12: 10}},
        'desert': {
            'fs': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30},
            'cs': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31, 12: 31}},
        'fire': {
            'fs': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30},
            'cs': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31, 12: 31}},
        'forest': {
            'fs': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30},
            'cs': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31, 12: 31}},
        'ice': {
            'fs': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30},
            'cs': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31, 12: 31}},
        'leviathan': {
            'fs': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
            'cs': {1: 10, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10, 10: 10, 11: 10, 12: 10}},
        'luna': {
            'fs': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
            'cs': {1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 8, 7: 8, 8: 8, 9: 8, 10: 8, 11: 8, 12: 8}},
        'skythrone': {
            'fs': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
            'cs': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}},
        'spectral': {
            'fs': {1: 2, 2: 2, 3: 2, 4: 4, 5: 6, 6: 8, 7: 11, 8: 14, 9: 17, 10: 20, 11: 20, 12: 20},
            'cs': {1: 2, 2: 2, 3: 4, 4: 6, 5: 8, 6: 10, 7: 14, 8: 18, 9: 22, 10: 26, 11: 26, 12: 26}},
        'stone': {
            'fs': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30},
            'cs': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31, 12: 31}},
        'swamp': {
            'fs': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30},
            'cs': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31, 12: 31}},
        'water': {
            'fs': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30},
            'cs': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31, 12: 31}},
        'wind': {
            'fs': {1: 11, 2: 14, 3: 17, 4: 20, 5: 23, 6: 26, 7: 29, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30},
            'cs': {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31, 7: 31, 8: 31, 9: 31, 10: 31, 11: 31, 12: 31}}}
    scrn(dl['00'], dl['01'])
    ctrt(dl['02'])
    d_lst, built, slctn, cptl_bldg = [list(), list(), {}, {}]
    for x in range(len(cData['capital']['city']['buildings'])):
        building = cData['capital']['city']['buildings'][x]
        if building['type'] not in cptl_bldg:
            cptl_bldg[building['type']] = building['level']
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
                c_slot = bldg_dict[key]['cs'][city['level']]
                f_slot = bldg_dict[key]['fs'][city['level']]
            elif key != 'capital' and 'DragonKeep' in city['type']:
                c_slot = bldg_dict[key]['cs'][city['level']]
                f_slot = bldg_dict[key]['fs'][city['level']]
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
                                               'lctn_id': cData[key]['city']['id'], 'desc': t(key),
                                               'time': manifest['levels'][z]['time']}
                                    d_lst.append(my_dict)
    if not d_lst:
        nthng(dl['00'], dl['01'], dl['03'])
        return
    elif len(d_lst) == 1:
        d_lct = d_lst[0]['city']
    else:
        d_lst = sorted(d_lst, key=itemgetter('desc'))
        d_lct = None
        a, b, c = [dl['04'], dl['05'], dl['06']]
        a1, b1, c1 = [len(a), len(b), len(c)]
        for x in range(len(d_lst)):
            if len(d_lst[x]['desc']) > a1:
                a1 = len(d_lst[x]['desc'])
        while d_lct is None:
            scrn(dl['00'], dl['01'])
            ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
            ctrt('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
            for x in range(len(d_lst)):
                d1, d2 = [d_lst[x]['c_slot_max'] - len(d_lst[x]['c_slot']),
                          d_lst[x]['f_slot_max'] - len(d_lst[x]['f_slot'])]
                if d_lst[x]['city'] not in slctn:
                    slctn[d_lst[x]['city']] = d_lst[x]['city']
                    ctrt('{0:<{1}}  {2:^{3}}  {4:^{5}}'.format(d_lst[x]['desc'], a1, d1, b1, d2, c1))
            dvsn()
            d_select = input(' {0} : '.format(dl['07']))
            if d_select.lower() == dl['08'] or d_select.lower() == 'exit':
                return
            else:
                for x in range(len(d_lst)):
                    if d_select.lower() == d_lst[x]['desc'].lower():
                        d_lct = d_lst[x]['city']
                        break
                else:
                    for x in range(len(d_lst)):
                        if d_select.lower() in d_lst[x]['desc'].lower():
                            d_lct = d_lst[x]['city']
                            break
    d_lst[:] = [d for d in d_lst if d.get('city') == d_lct]
    d_lct = t(d_lct)
    d_lst = sorted(d_lst, key=itemgetter('type'))
    if len(d_lst) == 1:
        d_bldg = d_lst[0]['type']
    else:
        d_bldg = None
        a, b, c = [dl['09'], dl['10'], dl['11']]
        a1, b1, c1 = [len(a), len(b), len(c)]
        for x in range(len(d_lst)):
            if len(d_lst[x]['type']) > a1:
                a1 = len(d_lst[x]['type'])
            if len(cvttm(d_lst[x]['time'])) > b1:
                b1 = len(cvttm(d_lst[x]['time']))
        while d_bldg is None:
            scrn(dl['00'], dl['12'])
            ctrt('{0}: {1}'.format(dl['04'], d_lct))
            ctrt(' ')
            dvsn('-')
            ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
            ctrt('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
            for x in range(len(d_lst)):
                if d_lst[x]['location'] == 'city':
                    d = d_lst[x]['c_slot_max'] - len(d_lst[x]['c_slot'])
                else:
                    d = d_lst[x]['f_slot_max'] - len(d_lst[x]['f_slot'])
                ctrt('{0:<{1}}  {2:>{3}}  {4:^{5}}'.format(d_lst[x]['type'], a1, cvttm(d_lst[x]['time']), b1, d, c1))
            dvsn()
            d_select = input(' {0} : '.format(dl['07']))
            if len(d_select) >= 3:
                if d_select.lower() == dl['08'] or d_select.lower() == 'exit':
                    return
                else:
                    for x in range(len(d_lst)):
                        if d_select.lower() == t(d_lst[x]['type'].lower()):
                            d_bldg = d_lst[x]['type']
                            break
                    else:
                        for x in range(len(d_lst)):
                            if d_select.lower() in t(d_lst[x]['type'].lower()):
                                d_bldg = d_lst[x]['type']
                                break
    d_lst[:] = [d for d in d_lst if d.get('type') == d_bldg]
    if d_lst[0]['location'] == 'city':
        max_slot = d_lst[0]['c_slot_max'] - len(d_lst[0]['c_slot'])
    else:
        max_slot = d_lst[0]['f_slot_max'] - len(d_lst[0]['f_slot'])
    gtg = False
    req = d_lst[0]['levels']['requirements']
    d_req = {'items': {}, 'buildings': {}, 'resources': {}}
    if d_lst[0]['per_city'] == 1:
        d_slots = 1
    else:
        d_slots = 0
        while d_slots is 0:
            scrn(dl['00'], dl['13'])
            ctrt('{0}: {1}   {2}: {3}'.format(dl['04'], d_lct, dl['09'], t(d_bldg)))
            ctrt(' ')
            dvsn('-')
            ctrt('~~~ {0} ~~~'.format(dl['14']))
            ctrt('1 - {0}'.format(max_slot))
            dvsn()
            d_select = input(' {0} : '.format(dl['07']))
            if d_select.lower() == dl['08'] or d_select.lower() == 'exit':
                return
            if d_select.isnumeric():
                if int(d_select) in range(max_slot + 1):
                    d_slots = int(d_select)
        while gtg is False:
            d_req = {'items': {}, 'buildings': {}, 'resources': {}}
            req_check = list()
            for key in req.keys():
                for c_key, c_value in req[key].items():
                    if c_key in d_req[key]:
                        if key == 'buildings':
                            if d_req[key][c_key] < c_value:
                                d_req[key][c_key] = c_value
                        else:
                            d_req[key][c_key] += c_value * d_slots
                    else:
                        d_req[key][c_key] = c_value * d_slots
            if len(d_req['items']) + len(d_req['buildings']) + len(d_req['resources']) > 0:
                for key in d_req:
                    if key == 'buildings':
                        for c_key, c_value in d_req[key].items():
                            if c_key in cptl_bldg.keys():
                                if c_value > cptl_bldg[c_key]:
                                    req = '{0} {1} {2} {3}'.format(c_key, c_value, dl['15'], cptl_bldg[c_key])
                                    req_check.append(req)
                            else:
                                req = '{0} {1} {2}'.format(c_key, c_value, dl['16'])
                                req_check.append(req)
                    if key == 'items':
                        for c_key, c_value in d_req[key].items():
                            if c_key in pData['items']:
                                if pData['items'][c_key] < c_value:
                                    req = '{0:,} {1} {2} {3:,}'.format(c_value, c_key, dl['17'], pData['items'][c_key])
                                    req_check.append(req)
                            else:
                                req = '{0:,} {1} {2}'.format(c_value, c_key, dl['18'])
                                req_check.append(req)
                    if key == 'resources':
                        for c_key, c_value in d_req[key].items():
                            if c_key in cData['capital']['city']['resources']:
                                if cData['capital']['city']['resources'][c_key] < c_value:
                                    req = '{0:,} {1} {2} {3:,}'.format(
                                            c_value, c_key, dl['17'], cData['capital']['city']['resources'][c_key])
                                    req_check.append(req)
                            else:
                                req = '{0:,} {1} {2}'.format(c_value, c_key, dl['18'])
                                req_check.append(req)
            scrn(dl['00'], dl['13'])
            ctrt('{0}: {1}   {2}: {3}'.format(dl['04'], d_lct, dl['09'], t(d_bldg)))
            ctrt(' ')
            dvsn('-')
            ctrt('~~~ {0} ~~~'.format(dl['14']))
            ctrt('1 - {0}'.format(max_slot), suffix=True)
            if len(req_check) != 0:
                for x in range(len(req_check)):
                    ctrt(req_check[x])
                ctrt('{0}'.format(dl['19']), prefix=True, suffix=True)
                dvsn()
            if len(req_check) == 0 and d_slots != 0:
                gtg = True
            else:
                d_select = input(' {0} : '.format(dl['07']))
                if len(d_select) >= 1:
                    if d_select.lower() == dl['08'] or d_select.lower() == 'exit':
                        return
                    if d_select.isnumeric():
                        if int(d_select) in range(max_slot + 1):
                            d_slots = int(d_select)
                            req_check.clear()
    if d_lst[0]['time'] < 20:
        d_speed = list()
    else:
        slctn, d_speed = [list(), list()]
        spd_itm = [{'item': 'Blitz', 'exceed': 216000, 'time': 345600, 'desc': dl['25']},
                   {'item': 'Blast', 'exceed': 86400, 'time': 216000, 'desc': dl['26']},
                   {'item': 'Bolt', 'exceed': 54000, 'time': 86400, 'desc': dl['27']},
                   {'item': 'Bore', 'exceed': 28800, 'time': 54000, 'desc': dl['28']},
                   {'item': 'Bounce', 'exceed': 9000, 'time': 28800, 'desc': dl['29']},
                   {'item': 'Leap', 'exceed': 3600, 'time': 9000, 'desc': dl['30']},
                   {'item': 'Jump', 'exceed': 900, 'time': 3600, 'desc': dl['31']},
                   {'item': 'Skip', 'exceed': 300, 'time': 900, 'desc': dl['32']},
                   {'item': 'Hop', 'exceed': 60, 'time': 300, 'desc': dl['33']},
                   {'item': 'Blink', 'exceed': 0, 'time': 60, 'desc': dl['34']}]
        a, b, c, d, e = [dl['20'], dl['21'], dl['22'], dl['23'], dl['24']]
        a1, b1, c1, d1, e1 = [len(a), len(b), len(c), len(d), len(e)]
        for key in range(len(spd_itm)):
            look_up = spd_itm[key]
            if look_up['item'] in pData['items'] and pData['items'][look_up['item']] > 0:
                if len(look_up['desc']) > a1:
                    a1 = len(look_up['desc'])
                if len(cvttm(look_up['time'], ss=False)) > b1:
                    b1 = len(cvttm(look_up['time'], ss=False))
                if len('{0:,}'.format(pData['items'][look_up['item']])) > c1:
                    c1 = len('{0:,}'.format(pData['items'][look_up['item']]))
                if len(cvttm(look_up['exceed'], ss=False)) > d1:
                    d1 = len(cvttm(look_up['exceed'], ss=False))
                my_dict = {'item': look_up['item'], 'exceed': look_up['exceed'], 'time': look_up['time'],
                           'quantity': pData['items'][look_up['item']], 'use': False, 'desc': look_up['desc']}
                slctn.append(my_dict)
        if slctn:
            while True:
                scrn(dl['00'], dl['35'])
                ctrt('{0}: {1}   {2}: {3}'.format(dl['04'], d_lct, dl['09'], t(d_bldg)))
                ctrt('{0}: {1}'.format(dl['36'], d_slots))
                dvsn('-')
                ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}  {8:^{9}}'.format(a, a1, b, b1, c, c1, d, d1, e, e1))
                ctrt('{0}  {1}  {2}  {3}  {4}'.format('~' * a1, '~' * b1, '~' * c1, '~' * d1, '~' * e1))
                for key in range(len(slctn)):
                    use_item = dl['61'].title() if slctn[key]['use'] is True else dl['62'].title()
                    ctrt('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}  {8:>{9}}'.format(
                            slctn[key]['desc'], a1, cvttm(slctn[key]['time'], ss=False), b1,
                            slctn[key]['quantity'], c1, cvttm(slctn[key]['exceed'], ss=False), d1, use_item, e1))
                ctrt('{0}: {1}'.format(dl['44'], d_lst[0]['time']))
                print('\n {0}'.format(dl['40']))
                dvsn('.')
                print(' {0}'.format(dl['37']))
                print('       {0}'.format(dl['38']))
                print('       {0}'.format(dl['39']))
                dvsn()
                d_select = input(' {0} : '.format(dl['07']))
                if len(d_select) >= 2:
                    if d_select.lower() == dl['08'] or d_select.lower() == 'exit':
                        return
                    elif d_select.lower() == dl['41'] or d_select.lower() == 'next':
                        break
                    elif d_select.lower() == dl['42'] or d_select.lower() == 'all':
                        for key in range(len(slctn)):
                            slctn[key]['use'] = True
                    elif d_select.lower() == dl['43'] or d_select.lower() == 'none':
                        for key in range(len(slctn)):
                            slctn[key]['use'] = False
                    else:
                        for key in range(len(slctn)):
                            if d_select.lower() == slctn[key]['desc'].lower():
                                slctn[key]['use'] = True if slctn[key]['use'] is False else False
                                break
                        else:
                            for key in range(len(slctn)):
                                if d_select.lower() in slctn[key]['desc'].lower():
                                    slctn[key]['use'] = True if slctn[key]['use'] is False else False
        for x in range(len(slctn)):
            if slctn[x]['use'] is True:
                d_speed.append(slctn[x])
    d_delay = None
    while d_delay is None:
        scrn(dl['00'], dl['45'])
        ctrt('{0}: {1}   {2}: {3}'.format(dl['04'], d_lct, dl['09'], t(d_bldg)))
        ctrt('{0}: {1}'.format(dl['36'], d_slots))
        d_delay = stdly()
        if d_delay == dl['08'] or d_delay == 'exit':
            return
    d_proceed = False
    while not d_proceed:
        scrn(dl['00'], dl['47'])
        ctrt('{0}: {1}   {2}: {3}'.format(dl['04'], d_lct, dl['09'], t(d_bldg)))
        ctrt('{0}: {1}   {2}: {3}s'.format(dl['36'], d_slots, dl['46'], d_delay))
        d_proceed = prcd()
        if d_proceed == dl['08'] or d_proceed == 'exit':
            return
    scrn(dl['00'], dl['48'])
    ctrt('{0}: {1}   {2}: {3}'.format(dl['04'], d_lct, dl['09'], t(d_bldg)))
    ctrt('{0}: {1}   {2}: {3}s'.format(dl['36'], d_slots, dl['46'], d_delay))
    dvsn('-')
    prg(0, 1, dl['02'])
    d_start, speeds_used, slots, count = [time(), {}, list(), 0]
    if d_lst[0]['location'] == 'city':
        for x in range(d_lst[0]['c_slot_max']):
            if x not in d_lst[0]['c_slot']:
                slots.append(x)
    else:
        for x in range(d_lst[0]['f_slot_max']):
            if x not in d_lst[0]['f_slot']:
                slots.append(x)
    for x in range(d_slots):
        job_id = 0
        dur = -1
        while dur != 0:
            scrn(dl['00'], dl['48'])
            ctrt('{0}: {1}   {2}: {3}'.format(dl['04'], d_lct, dl['09'], t(d_bldg)))
            ctrt('{0}: {1}   {2}: {3}s   {4}: {5}'.format(
                    dl['36'], d_slots, dl['46'], d_delay, dl['49'], cvttm(time() - d_start)))
            dvsn('-')
            if speeds_used:
                prg(x + 1, d_slots, '{0}: {1}/{2}'.format(dl['50'], x + 1, d_slots))
                ctrt('~~~ {0} ~~~'.format(dl['51']), prefix=True)
                dsply(speeds_used, single=False)
            elif dur != -1:
                prg(x + 1, d_slots, '{0}: {1}/{2}'.format(dl['50'], x + 1, d_slots),
                    '{0}: {1}'.format(dl['52'], cvttm(dur)))
            else:
                prg(x + 1, d_slots, '{0}: {1}/{2}'.format(dl['50'], x + 1, d_slots), dl['02'])
            if dur == -1:
                x_param = 'city%5F{0}%5B{0}%5Ftype%5D={1}&%5Fmethod=post&city%5F{0}%5Bslot%5D={2}&'.format(
                        'building', d_bldg, slots[x])
                for web_retry in range(5):
                    try:
                        sleep(d_delay)
                        json_data = web_op('cities/{0}/buildings'.format(d_lst[0]['lctn_id']), x_param)
                        result = json_data['result']['success']
                        if result:
                            dur = json_data['result']['job']['duration']
                            job_id = json_data['result']['job']['id']
                            break
                    except (KeyError, TypeError):
                        sleep(1)
                        continue
                else:
                    errmsg(dl['53'])
            elif dur != 0 and len(d_speed) > 0:
                speed_item = None
                for y in range(len(d_speed)):
                    if dur > d_speed[y]['exceed']:
                        speed_item = d_speed[y]['item']
                        break
                if speed_item is None:
                    if len(d_speed) == 1:
                        speed_item = d_speed[0]['item']
                    else:
                        for y in range(len(d_speed) + 1, -1, -1):
                            if dur <= d_speed[y]['time']:
                                speed_item = d_speed[y]['item']
                                break
                x_param = '%5Fmethod=delete&job%5Fid={0}&'.format(job_id)
                for web_retry in range(5):
                    try:
                        sleep(d_delay)
                        json_data = web_op('player_items/{0}'.format(speed_item), x_param)
                        result = json_data['result']['success']
                        if result:
                            if speed_item in speeds_used:
                                speeds_used[speed_item] += 1
                            else:
                                speeds_used[speed_item] = 1
                            dur = int(json_data['result']['item_response']['run_at'] - json_data['timestamp'])
                            if dur < 1:
                                dur = 0
                            break
                    except TypeError:
                        sleep(1)
                        continue
                else:
                    errmsg(dl['54'])
            else:
                dur -= 1
                if dur < 1:
                    dur = 0
                sleep(1)
    scrn(dl['00'], dl['55'])
    ctrt('{0}: {1}   {2}: {3}'.format(dl['04'], d_lct, dl['09'], t(d_bldg)))
    ctrt('{0}: {1}   {2}: {3}s'.format(dl['36'], d_slots, dl['46'], d_delay))
    dvsn('-')
    prg(1, 1, '{0} {1}'.format(dl['56'], cvttm(time() - d_start)))
    if speeds_used:
        ctrt('~~~ {0} ~~~'.format(dl['51']), prefix=True)
        dsply(speeds_used, single=False)
    if len(d_req['items']) >= 1:
        ctrt('~~~ {0} ~~~'.format(dl['57']), prefix=True)
        for key, value in d_req['items'].items():
            ctrt('{0:>}: {1:,}'.format(t(key), value))
    if len(d_req['resources']) >= 1:
        ctrt('~~~ {0} ~~~'.format(dl['58']), prefix=True)
        for key, value in d_req['resources'].items():
            ctrt('{0:>5}: {1:,}'.format(key.title(), value))
    dvsn()
    input(dl['59'])
    print(dl['60'])
    gtdt(pl=True, op=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def upgrade_building():
    dl = {'00': lo['c73'], '01': lo['c02'], '02': lo['a92'], '03': lo['c45'], '04': lo['a10'], '05': lo['a52'],
          '06': lo['a59'], '07': lo['b96'], '08': lo['b07'], '09': lo['a26'], '10': lo['a09'], '11': lo['c20'],
          '12': lo['c81'], '13': lo['b65'], '14': lo['a05'], '15': lo['b68'], '16': lo['b69'], '17': lo['b67'],
          '18': lo['b66'], '19': lo['b70'], '20': lo['a95'], '21': lo['a44'], '22': lo['a13'], '23': lo['a02'],
          '24': lo['c76'], '25': lo['a20'], '26': lo['a18'], '27': lo['a21'], '28': lo['a22'], '29': lo['a23'],
          '30': lo['b03'], '31': lo['a99'], '32': lo['c21'], '33': lo['a83'], '34': lo['a19'], '35': lo['c06'],
          '36': lo['c35'], '37': lo['b28'], '38': lo['a49'], '39': lo['a50'], '40': lo['a01'], '41': lo['b16'],
          '42': lo['a04'], '43': lo['b20'], '44': lo['b18'], '45': lo['c15'], '46': lo['a43'], '47': lo['b57'],
          '48': lo['b51'], '49': lo['a47'], '50': lo['c75'], '51': lo['c28'], '52': lo['b64'], '53': lo['b83'],
          '54': lo['b79'], '55': lo['c31'], '56': lo['b49'], '57': lo['a97'], '58': lo['b71'], '59': lo['b47'],
          '60': lo['c72'], '61': lo['c85'], '62': lo['b19'], '63': lo['c74']}
    scrn(dl['00'], dl['01'])
    ctrt(dl['02'])
    slctn, c_bldg, d_lst = [{}, {}, list()]
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
                        my_dict = {'city': key, 'max_level': manifest['city_max'][key], 'bldg_id': city['id'],
                                   'type': city['type'], 'level': city['level'], 'levels': levels,
                                   'lctn_id': cData[key]['city']['id'], 'desc': t(key)}
                        d_lst.append(my_dict)
                        break
    if not d_lst:
        nthng(dl['00'], dl['01'], dl['03'])
        return
    if len(d_lst) == 1:
        d_lct = d_lst[0]['city']
    else:
        d_lct = None
        for x in range(len(d_lst)):
            if d_lst[x]['city'] not in slctn.keys():
                slctn[d_lst[x]['city']] = t(d_lst[x]['city'])
        while d_lct is None:
            scrn(dl['00'], dl['01'])
            ctrt('~~~ {0} ~~~'.format(dl['04']))
            dsply(slctn)
            dvsn()
            d_select = input(' {0} : '.format(dl['05']))
            if len(d_select) >= 3:
                if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                    return
                else:
                    d_lct = chkinp(d_select, slctn)
    d_lst[:] = [d for d in d_lst if d.get('city') == d_lct]
    slctn.clear()
    if len(d_lst) == 1:
        d_bldg = d_lst[0]['type']
    else:
        for x in range(len(d_lst)):
            if d_lst[x]['type'] not in slctn:
                slctn[d_lst[x]['type']] = t(d_lst[x]['type'])
        d_bldg = None
        while d_bldg is None:
            scrn(dl['00'], dl['07'])
            ctrt('{0}: {1}'.format(dl['08'], t(d_lct)))
            ctrt(' ')
            dvsn('-')
            ctrt('~~~ {0} ~~~'.format(dl['10']))
            dsply(slctn)
            dvsn()
            d_select = input(' {0} : '.format(dl['05']))
            if len(d_select) >= 3:
                if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                    return
                else:
                    d_bldg = chkinp(d_select, slctn)
    d_lst[:] = [d for d in d_lst if d.get('type') == d_bldg]
    d_bldg = t(d_bldg)
    max_level = d_lst[0]['max_level']
    min_lvl = max_level
    for x in range(len(d_lst)):
        if d_lst[x]['level'] < min_lvl:
            min_lvl = d_lst[x]['level']
    gtg, d_lvl, d_req = [False, 0, {'items': {}, 'buildings': {}, 'research': {}, 'resources': {}}]
    while d_lvl is 0:
        scrn(dl['00'], dl['11'])
        ctrt('{0}: {1}   {2}: {3}'.format(dl['08'], t(d_lct), dl['09'], d_bldg))
        ctrt(' ')
        dvsn('-')
        ctrt('{0}'.format(dl['12']), prefix=True)
        x = '{0}'.format(min_lvl + 1) if max_level == min_lvl + 1 else '{0} - {1}'.format(min_lvl + 1, max_level)
        ctrt(x, suffix=True)
        dvsn()
        d_select = input(' {0} : '.format(dl['05']))
        if len(d_select) >= 1:
            if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                return
            if d_select.isnumeric():
                if int(d_select) in range(min_lvl + 1, max_level + 1):
                    d_lvl = int(d_select)
    while gtg is False:
        d_req = {'items': {}, 'buildings': {}, 'research': {}, 'resources': {}}
        req_check = list()
        for x in range(len(d_lst)):
            for y in range(len(d_lst[x]['levels'])):
                if d_lst[x]['levels'][y]['level'] <= d_lvl:
                    req = d_lst[x]['levels'][y]['requirements']
                    for key in req.keys():
                        for c_key, c_value in req[key].items():
                            if c_key in d_req[key]:
                                if key == 'buildings':
                                    if d_req[key][c_key] < c_value:
                                        d_req[key][c_key] = c_value
                                else:
                                    d_req[key][c_key] += c_value
                            else:
                                d_req[key][c_key] = c_value
        if len(d_req['items']) + len(d_req['buildings']) + len(d_req['resources']) > 0:
            for key in d_req:
                if key == 'buildings':
                    for c_key, c_value in d_req[key].items():
                        for x in range(len(cData[d_lct]['city']['buildings'])):
                            if c_key == cData[d_lct]['city']['buildings'][x]['type']:
                                if c_value > cData[d_lct]['city']['buildings'][x]['level']:
                                    req = '{0} {1} {2} {3}'.format(
                                            t(c_key), c_value, dl['15'], cData[d_lct]['city']['buildings'][x]['level'])
                                    req_check.append(req)
                                break
                        else:
                            if c_key in c_bldg.keys():
                                if c_value > c_bldg[c_key]:
                                    req = '{0} {1} {2} {3}'.format(t(c_key), c_value, dl['15'], c_bldg[c_key])
                                    req_check.append(req)
                            else:
                                req = '{0} {1} {2}'.format(t(c_key), c_value, dl['16'])
                                req_check.append(req)
                if key == 'items':
                    for c_key, c_value in d_req[key].items():
                        if c_key in pData['items']:
                            if pData['items'][c_key] < c_value:
                                req = '{0:,} {1} {2} {3:,}'.format(
                                        c_value, c_key, dl['17'], pData['items'][c_key])
                                req_check.append(req)
                        else:
                            req = '{0:,} {1} {2}'.format(c_value, c_key, dl['18'])
                            req_check.append(req)
                if key == 'research':
                    for c_key, c_value in d_req[key].items():
                        if c_key in pData['research']:
                            if pData['research'][c_key] < c_value:
                                req = '{1} {0} {2} {3}'.format(c_value, c_key, dl['15'], pData['research'][c_key])
                                req_check.append(req)
                        else:
                            req = '{1} {0} {2} {1}'.format(c_value, c_key, dl['13'])
                            req_check.append(req)
                if key == 'resources':
                    for c_key, c_value in d_req[key].items():
                        if c_key in cData['capital']['city']['resources']:
                            if cData['capital']['city']['resources'][c_key] < c_value:
                                req = '{0:,} {1} {2} {3:,}'.format(
                                        c_value, c_key, dl['17'], cData['capital']['city']['resources'][c_key])
                                req_check.append(req)
        scrn(dl['00'], dl['11'])
        ctrt('{0}: {1}   {2}: {3}'.format(dl['08'], t(d_lct), dl['09'], d_bldg))
        ctrt(' ')
        dvsn('-')
        ctrt(dl['12'], prefix=True)
        ctrt('{0} - {1}'.format(min_lvl + 1, max_level), suffix=True)
        if len(req_check) != 0:
            dvsn('#')
            ctrt(dl['19'], suffix=True)
            for x in range(len(req_check)):
                ctrt(req_check[x])
            dvsn('#')
        if len(req_check) == 0 and d_lvl != 0:
            gtg = True
        else:
            dvsn()
            d_select = input(' {0} : '.format(dl['05']))
            if len(d_select) >= 1:
                if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                    return
                if d_select.isnumeric():
                    if int(d_select) in range(min_lvl + 1, max_level + 1):
                        d_lvl = int(d_select)
                        req_check.clear()
    slctn = list()
    spd_itm = [{'item': 'Blitz', 'exceed': 216000, 'time': 345600, 'desc': dl['25']},
               {'item': 'Blast', 'exceed': 86400, 'time': 216000, 'desc': dl['26']},
               {'item': 'Bolt', 'exceed': 54000, 'time': 86400, 'desc': dl['27']},
               {'item': 'Bore', 'exceed': 28800, 'time': 54000, 'desc': dl['28']},
               {'item': 'Bounce', 'exceed': 9000, 'time': 28800, 'desc': dl['29']},
               {'item': 'Leap', 'exceed': 3600, 'time': 9000, 'desc': dl['30']},
               {'item': 'Jump', 'exceed': 900, 'time': 3600, 'desc': dl['31']},
               {'item': 'Skip', 'exceed': 300, 'time': 900, 'desc': dl['32']},
               {'item': 'Hop', 'exceed': 60, 'time': 300, 'desc': dl['33']},
               {'item': 'Blink', 'exceed': 0, 'time': 60, 'desc': dl['34']}]
    a, b, c, d, e = [dl['20'], dl['21'], dl['22'], dl['23'], dl['24']]
    a1, b1, c1, d1, e1 = [len(a), len(b), len(c), len(d), len(e)]
    for key in range(len(spd_itm)):
        look_up = spd_itm[key]
        if look_up['item'] in pData['items'] and pData['items'][look_up['item']] > 0:
            if len(look_up['desc']) > a1:
                a1 = len(look_up['desc'])
            if len(cvttm(look_up['time'], ss=False)) > b1:
                b1 = len(cvttm(look_up['time'], ss=False))
            if len('{0:,}'.format(pData['items'][look_up['item']])) > c1:
                c1 = len('{0:,}'.format(pData['items'][look_up['item']]))
            if len(cvttm(look_up['exceed'], ss=False)) > d1:
                d1 = len(cvttm(look_up['exceed'], ss=False))
            my_dict = {'item': look_up['item'], 'exceed': look_up['exceed'], 'time': look_up['time'],
                       'quantity': pData['items'][look_up['item']], 'use': False, 'desc': look_up['desc']}
            slctn.append(my_dict)
    if slctn:
        while True:
            scrn(dl['00'], dl['35'])
            ctrt('{0}: {1}   {2}: {3}   {4}: {5}'.format(dl['08'], t(d_lct), dl['09'], d_bldg, dl['36'], d_lvl))
            ctrt(' ')
            dvsn('-')
            ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}  {8:^{9}}'.format(a, a1, b, b1, c, c1, d, d1, e, e1))
            ctrt('{0}  {1}  {2}  {3}  {4}'.format('~' * a1, '~' * b1, '~' * c1, '~' * d1, '~' * e1))
            for x in range(len(slctn)):
                use_item = dl['61'].title() if slctn[x]['use'] is True else dl['62'].title()
                ctrt('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}  {8:>3}'.format(
                        slctn[x]['desc'], a1, cvttm(slctn[x]['time'], ss=False), b1, slctn[x]['quantity'], c1,
                        cvttm(slctn[x]['exceed'], ss=False), d1, use_item))
            print('\n {0}'.format(dl['40']))
            dvsn('.')
            print(' {0}'.format(dl['37']))
            print('       {0}'.format(dl['38']))
            print('       {0}'.format(dl['39']))
            dvsn()
            d_select = input(' {0} : '.format(dl['05']))
            if len(d_select) >= 2:
                if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                    return
                elif d_select.lower() == dl['41'] or d_select.lower() == 'next':
                    break
                elif d_select.lower() == dl['42'] or d_select.lower() == 'all':
                    for x in range(len(slctn)):
                        slctn[x]['use'] = True
                elif d_select.lower() == dl['43'] or d_select.lower() == 'none':
                    for x in range(len(slctn)):
                        slctn[x]['use'] = False
                else:
                    for x in range(len(slctn)):
                        if d_select.lower() == slctn[x]['desc'].lower():
                            slctn[x]['use'] = True if not slctn[x]['use'] else False
                            break
                    else:
                        for x in range(len(slctn)):
                            if d_select.lower() in slctn[x]['desc'].lower():
                                slctn[x]['use'] = True if not slctn[x]['use'] else False
    d_speed = list()
    for x in range(len(slctn)):
        if slctn[x]['use'] is True:
            d_speed.append(slctn[x])
    d_delay = None
    while d_delay is None:
        scrn(dl['00'], dl['45'])
        ctrt('{0}: {1}   {2}: {3}   {4}: {5}'.format(dl['08'], t(d_lct), dl['09'], d_bldg, dl['36'], d_lvl))
        ctrt(' ')
        d_delay = stdly()
        if d_delay == dl['06'] or d_delay == 'exit':
            return
    d_proceed = False
    while not d_proceed:
        scrn(dl['00'], dl['47'])
        ctrt('{0}: {1}   {2}: {3}   {4}: {5}'.format(dl['08'], t(d_lct), dl['09'], d_bldg, dl['36'], d_lvl))
        ctrt('{0}: {1}s'.format(dl['46'], d_delay))
        d_proceed = prcd()
        if d_proceed == dl['06'] or d_proceed == 'exit':
            return
    scrn(dl['00'], dl['48'])
    ctrt('{0}: {1}   {2}: {3}   {4}: {5}'.format(dl['08'], t(d_lct), dl['09'], d_bldg, dl['36'], d_lvl))
    ctrt('{0}: {1}s'.format(dl['46'], d_delay))
    dvsn('-')
    prg(0, 1, dl['02'])
    d_start, spd_usd, len_d_lst = [time(), {}, len(d_lst)]
    for y in range(min_lvl, d_lvl):
        total = len([d for d in d_lst if d.get('level') == y])
        count = 0
        speed_item = None
        for x in range(len_d_lst):
            if d_lst[x]['level'] == y:
                job_id, dur, prog_dur = [0, -1, 0]
                while dur != 0:
                    if dur == -1:
                        x_param = '%5Fmethod=put&'
                        for server_retry in range(5):
                            sleep(d_delay + 1)
                            try:
                                main_json = web_op('cities/{0}/buildings/{1}'.format(
                                        d_lst[x]['lctn_id'], d_lst[x]['bldg_id']), x_param)
                                result = main_json['result']['success']
                                if result:
                                    dur = int(main_json['result']['job']['duration'])
                                    prog_dur = dur
                                    job_id = main_json['result']['job']['id']
                                    count += 1
                                    break
                            except (KeyError, TypeError):
                                sleep(1)
                                continue
                        else:
                            errmsg(dl['53'])
                    elif dur > 15 and len(d_speed) > 0:
                        speed_item = None
                        for z in range(len(d_speed)):
                            if dur > d_speed[z]['exceed'] and d_speed[z]['quantity'] != 0:
                                speed_item = d_speed[z]['item']
                                break
                        if speed_item is None:
                            if len(d_speed) == 1 and d_speed[0]['quantity'] != 0:
                                speed_item = d_speed[0]['item']
                            else:
                                for z in range(len(d_speed) - 1, -1, -1):
                                    if dur <= d_speed[z]['time'] and d_speed[z]['quantity'] != 0:
                                        speed_item = d_speed[z]['item']
                                        break
                        x_param = '%5Fmethod=delete&job%5Fid={0}&'.format(job_id)
                        for server_retry in range(5):
                            sleep(d_delay + 1)
                            try:
                                item_json = web_op('player_items/{0}'.format(speed_item), x_param)
                                result = item_json['result']['success']
                                if result:
                                    for z in range(len(d_speed)):
                                        if speed_item == d_speed[z]['item']:
                                            d_speed[z]['quantity'] -= 1
                                    if speed_item in spd_usd:
                                        spd_usd[speed_item] += 1
                                    else:
                                        spd_usd[speed_item] = 1
                                    dur = int(item_json['result']['item_response']['run_at'] - item_json['timestamp'])
                                    if dur < 1:
                                        dur = 0
                                        d_lst[x]['level'] = item_json['result']['item_response']['level']
                                    break
                            except (KeyError, TypeError):
                                sleep(1)
                                continue
                        else:
                            errmsg(dl['54'])
                    else:
                        dur -= 1
                        if dur < 1:
                            dur = 0
                            d_lst[x]['level'] += 1
                        sleep(1)
                    scrn(dl['00'], dl['48'])
                    ctrt('{0}: {1}   {2}: {3}   {4}: {5}'.format(dl['08'], t(d_lct), dl['09'], d_bldg, dl['36'], d_lvl))
                    ctrt('{0}: {1}s   {2}: {3}'.format(dl['46'], d_delay, dl['49'], cvttm(time() - d_start)))
                    dvsn('-')
                    prg_sf = '{0} {1}/{2}'.format(dl['63'], count, total) if total > 1 else ' '
                    # prg_sf = '{0} {1}/{2}'.format(dl['63'], count, total) if total > 1 else ' '
                    prg((d_lvl - min_lvl) - (d_lvl - y), (d_lvl - min_lvl), '{0} {1}'.format(dl['50'], y + 1), prg_sf)
                    if speed_item:
                        prg(prog_dur - dur, prog_dur, '{0}: {1}'.format(dl['14'], speed_item),
                            '{0}: {1}'.format(dl['52'], cvttm(dur)))
                    else:
                        if dur != -1:
                            prg(prog_dur - dur, prog_dur, dl['44'], '{0}: {1}'.format(dl['52'], cvttm(dur)))
                        else:
                            prg(prog_dur - dur, prog_dur, dl['02'])
                    if spd_usd:
                        ctrt('~~~ {0} ~~~'.format(dl['51']), prefix=True)
                        dsply(spd_usd, single=False)
    scrn(dl['00'], dl['55'])
    ctrt('{0}: {1}   {2}: {3}   {4}: {5}'.format(dl['08'], t(d_lct), dl['09'], d_bldg, dl['36'], d_lvl))
    ctrt('{0}: {1}s'.format(dl['46'], d_delay))
    dvsn('-')
    prg(1, 1, '{0} {1}'.format(dl['56'], cvttm(time() - d_start)))
    if spd_usd:
        ctrt('~~~ {0} ~~~'.format(dl['51']), prefix=True)
        dsply(spd_usd, single=False)
    if len(d_req['items']) >= 1:
        ctrt('~~~ {0} ~~~'.format(dl['57']), prefix=True)
        for key, value in d_req['items'].items():
            ctrt('{0:>}: {1:,}'.format(t(key), value))
    if len(d_req['resources']) >= 1:
        ctrt('~~~ {0} ~~~'.format(dl['58']), prefix=True)
        for key, value in d_req['resources'].items():
            ctrt('{0:>5}: {1:,}'.format(key.title(), value))
    dvsn()
    input(dl['59'])
    print(dl['60'])
    gtdt(pl=True, op=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def train_troop():
    dl = {'00': lo['c59'], '01': lo['c08'], '02': lo['a94'], '03': lo['a11'], '04': lo['c84'], '05': lo['a52'],
          '06': lo['a59'], '07': lo['c85'], '08': lo['b19'], '09': lo['a92'], '10': lo['c52'], '11': lo['c65'],
          '12': lo['c60'], '13': lo['b44'], '14': lo['b07'], '15': lo['b04'], '16': lo['c58'], '17': lo['c54'],
          '18': lo['c02'], '19': lo['b63'], '20': lo['b25'], '21': lo['b10'], '22': lo['c38'], '23': lo['c37'],
          '24': lo['c39'], '25': lo['a20'], '26': lo['a18'], '27': lo['a21'], '28': lo['a22'], '29': lo['a23'],
          '30': lo['b03'], '31': lo['a99'], '32': lo['c21'], '33': lo['a83'], '34': lo['a19'], '35': lo['b59'],
          '36': lo['c62'], '37': lo['b24'], '38': lo['a51'], '39': lo['b16'], '40': lo['b30'], '41': lo['c18'],
          '42': lo['b53'], '43': lo['a85'], '44': lo['c15'], '45': lo['c34'], '46': lo['b57'], '47': lo['a43'],
          '48': lo['b51'], '49': lo['a47'], '50': lo['c61'], '51': lo['b64'], '52': lo['a05'], '53': lo['c40'],
          '54': lo['c28'], '55': lo['c66'], '56': lo['b45'], '57': lo['b87'], '58': lo['b79'], '59': lo['c31'],
          '60': lo['b49'], '61': lo['b47'], '62': lo['c72'], '63': lo['c27'], '64': lo['a44'], '65': lo['a13'],
          '66': lo['c76'], '67': lo['b80']}
    low_req = None
    while low_req is None:
        scrn(dl['00'], dl['01'])
        ctrt(dl['02'], prefix=True, suffix=True)
        ctrt('~~~ {0} ~~~'.format(dl['03']))
        ctrt(dl['04'])
        dvsn()
        d_select = input(' {0} : '.format(dl['05']))
        if len(d_select) >= 1:
            if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                break
            if d_select.isalpha():
                if d_select.lower() == dl['07'].lower() or d_select.lower() == 'yes':
                    low_req = True
                elif d_select.lower() == dl['08'].lower() or d_select.lower() == 'no':
                    low_req = False
    scrn(dl['00'], dl['01'])
    ctrt(dl['09'])
    d_lst, slctn, pseudo_tc, d_rookery = [list(), {}, ('Garrison', 'TrainingCamp', 'CaveTrainingCamp'), 0]
    for x in cData:
        tclvl, tcttl, tccmb = [0, 0, 0]
        for y in range(len(cData[x]['city']['buildings'])):
            if cData[x]['city']['buildings'][y]['type'] in pseudo_tc:
                tclvl = cData[x]['city']['buildings'][y]['level'] if tclvl < cData[x]['city']['buildings'][y][
                    'level'] else tclvl
                tcttl += 1
                tccmb += cData[x]['city']['buildings'][y]['level']
        my_dict = {'tclvl': tclvl, 'tccmb': tccmb, 'tcttl': tcttl}
        slctn[x] = my_dict
    for x in range(len(mData['units'])):
        train_in = None
        if mData['units'][x]['category'] == 'limited' and low_req:
            train_in = ('capital', 'chrono')
        if mData['units'][x]['trainable_in'] or train_in:
            d_queue, d_pop = [-1, -1]
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
                                if d_queue > int(lookup[key] / value) or d_queue == -1:
                                    d_queue = int(lookup[key] / value)
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
                                    if d_queue > int(lookup[key] / value) or d_queue == -1:
                                        d_queue = int(lookup[key] / value)
                    met_item = True if met_req == 0 else False
            if 'units' in d_req.keys():
                met_req = len(d_req['units'])
                lookup = cData['capital']['city']['units']
                for key, value in d_req['units'].items():
                    if key in lookup:
                        if value <= lookup[key]:
                            met_req -= 1
                            if value != 0:
                                if d_queue > int(lookup[key] / value) or d_queue == -1:
                                    d_queue = int(lookup[key] / value)
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
                if low_req and not mData['units'][x]['trainable_in']:
                    train_in_loc = train_in
                else:
                    train_in_loc = mData['units'][x]['trainable_in']
                for d_loc in train_in_loc:
                    if 'buildings' in d_req.keys():
                        for key, value in d_req['buildings'].items():
                            if key in pseudo_tc and value <= slctn[d_loc]['tclvl']:
                                mltplr = slctn[d_loc]['tcttl'] + ((slctn[d_loc]['tccmb'] - slctn[d_loc]['tcttl']) / 10)
                                if mData['units'][x]['type'] in ('BattleDragon', 'SwiftStrikeDragon') \
                                        and d_loc == 'capital':
                                    mltplr += (mltplr / 100) * d_rookery
                                if d_pop > d_queue:
                                    d_pop = d_queue
                                my_dict = {'troop': mData['units'][x]['type'], 'desc': t(mData['units'][x]['type']),
                                           'id': cData[d_loc]['city']['id'], 'time': mData['units'][x]['time'],
                                           'tclvl': slctn[d_loc]['tclvl'], 'power': mData['units'][x]['stats']['power'],
                                           'tcttl': slctn[d_loc]['tcttl'], 'mltplr': mltplr, 'loc_desc': t(d_loc),
                                           'trnbl': d_queue, 'location': d_loc, 'qty': d_pop}
                                d_lst.append(my_dict)
                                break
    d_lst = sorted(d_lst, key=itemgetter('desc'))
    slctn.clear()
    if not d_lst:
        nthng(dl['00'], dl['01'], dl['10'])
        return
    elif len(d_lst) == 1:
        d_trp = d_lst[0]['troop']
    else:
        a, b, c = [dl['11'], dl['12'], dl['13']]
        a1, b1, c1 = [len(a), len(b), len(c)]
        for x in range(len(d_lst)):
            if len(d_lst[x]['desc']) > a1:
                a1 = len(d_lst[x]['desc'])
            if len('{0:,}'.format(d_lst[x]['trnbl'])) > b1:
                b1 = len('{0:,}'.format(d_lst[x]['trnbl']))
            if len('{0:,}'.format(d_lst[x]['trnbl'] * d_lst[x]['power'])) > c1:
                c1 = len('{0:,}'.format(d_lst[x]['trnbl'] * d_lst[x]['power']))
        d_trp = None
        while d_trp is None:
            slctn.clear()
            scrn(dl['00'], dl['01'])
            ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
            ctrt('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
            for x in range(len(d_lst)):
                if d_lst[x]['troop'] not in slctn:
                    slctn[d_lst[x]['troop']] = d_lst[x]['desc']
                    ctrt('{0:<{1}}  {2:>{3},}  {4:>{5},}'.format(
                            d_lst[x]['desc'], a1, d_lst[x]['trnbl'], b1, d_lst[x]['trnbl'] * d_lst[x]['power'], c1))
            dvsn()
            d_select = input(' {0} : '.format(dl['05']))
            if len(d_select) >= 3:
                if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                    return
                else:
                    d_trp = chkinp(d_select, slctn)
    d_lst[:] = [d for d in d_lst if d.get('troop') == d_trp]
    slctn.clear()
    if len(d_lst) == 1:
        d_lctn = d_lst[0]['location']
    else:
        d_lctn = None
        d_lst = sorted(d_lst, key=itemgetter('loc_desc'))
        a, b, c, d = [dl['14'], dl['15'], dl['16'], dl['17']]
        a1, b1, c1, d1 = [len(a), len(b), len(c), len(d)]
        for x in range(len(d_lst)):
            if len(d_lst[x]['loc_desc']) > a1:
                a1 = len(d_lst[x]['loc_desc'])
            if len('{0}'.format(d_lst[x]['tclvl'])) > b1:
                b1 = len('{0}'.format(d_lst[x]['tclvl']))
            if len('{0}'.format(d_lst[x]['tcttl'])) > c1:
                c1 = len('{0}'.format(d_lst[x]['tcttl']))
            if len(cvttm(d_lst[x]['time'] / d_lst[x]['mltplr'])) > d1:
                d1 = len(cvttm(d_lst[x]['time'] / d_lst[x]['mltplr']))
        while d_lctn is None:
            scrn(dl['00'], dl['18'])
            ctrt('{0}: {1}'.format(dl['11'], t(d_trp)))
            ctrt(' ')
            dvsn('-')
            ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}'.format(a, a1, b, b1, c, c1, d, d1))
            ctrt('{0}  {1}  {2}  {3}'.format('~' * a1, '~' * b1, '~' * c1, '~' * d1))
            for x in range(len(d_lst)):
                ctrt('{0:<{1}}  {2:^{3}}  {4:^{5}}  {6:>{7}}'.format(
                        d_lst[x]['loc_desc'], a1, d_lst[x]['tclvl'], b1, d_lst[x]['tcttl'], c1,
                        cvttm(d_lst[x]['time'] / d_lst[x]['mltplr']), d1))
            dvsn()
            d_select = input(' {0} : '.format(dl['05']))
            if len(d_select) >= 3:
                if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                    return
                else:
                    for x in range(len(d_lst)):
                        if d_select.lower() == d_lst[x]['loc_desc'].lower():
                            d_lctn = d_lst[x]['location']
                            break
                    else:
                        for x in range(len(d_lst)):
                            if d_select.lower() in d_lst[x]['loc_desc'].lower():
                                d_lctn = d_lst[x]['location']
                                break
    d_lst[:] = [d for d in d_lst if d.get('location') == d_lctn]
    d_queue = 1 if d_lst[0]['qty'] == 1 else 0
    while d_queue is 0:
        scrn(dl['00'], dl['19'])
        ctrt('{0}: {1}   {2}: {3}'.format(dl['11'], t(d_trp), dl['14'], t(d_lctn)))
        ctrt(' ')
        dvsn('-')
        ctrt('~~~ {0} ~~~'.format(dl['03']))
        ctrt('1 - {0}'.format(d_lst[0]['qty']), suffix=True)
        print(' {0}'.format(dl['20']))
        dvsn()
        d_select = input(' {0} : '.format(dl['05']))
        if len(d_select) >= 1:
            if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                return
            elif d_select.lower() == dl['21'] or d_select.lower() == 'max':
                d_queue = d_lst[0]['qty']
            elif d_select.isnumeric():
                if int(d_select) in range(1, d_lst[0]['qty'] + 1):
                    d_queue = int(d_select)
    d_lst[0]['qty'] = d_queue
    slctn.clear()
    a, b, c, d = [dl['63'], dl['64'], dl['65'], dl['66']]
    a1, b1, c1, d1 = [len(a), len(b), len(c), len(d)]
    slctn = [{'item': 'TestroniusInfusion', 'time': 0.99, 'desc': dl['22']},
             {'item': 'TestroniusDeluxe', 'time': 0.5, 'desc': dl['23']},
             {'item': 'TestroniusPowder', 'time': 0.3, 'desc': dl['24']},
             {'item': 'Blitz', 'time': 345600, 'desc': dl['25']},
             {'item': 'Blast', 'time': 216000, 'desc': dl['26']},
             {'item': 'Bolt', 'time': 86400, 'desc': dl['27']},
             {'item': 'Bore', 'time': 54000, 'desc': dl['28']},
             {'item': 'Bounce', 'time': 28800, 'desc': dl['29']},
             {'item': 'Leap', 'time': 9000, 'desc': dl['30']},
             {'item': 'Jump', 'time': 3600, 'desc': dl['31']},
             {'item': 'Skip', 'time': 900, 'desc': dl['32']},
             {'item': 'Hop', 'time': 300, 'desc': dl['33']},
             {'item': 'Blink', 'time': 60, 'desc': dl['34']}]
    d_speed = list()
    for x in range(len(slctn)):
        if slctn[x]['item'] in pData['items']:
            if pData['items'][slctn[x]['item']] > 0:
                if slctn[x]['time'] < 1:
                    y = '{0}% {1}'.format(int(slctn[x]['time'] * 100), dl['35'])
                else:
                    y = '{0}'.format(cvttm(slctn[x]['time'], ss=False))
                my_dict = {'item': slctn[x]['item'], 'qty': pData['items'][slctn[x]['item']],
                           'time': slctn[x]['time'], 'desc': slctn[x]['desc'], 'use': 0, 'itm_dsc': y}
                d_speed.append(my_dict)
                if len(slctn[x]['desc']) > a1:
                    a1 = len(slctn[x]['desc'])
                if len(y) > b1:
                    b1 = len(y)
                z = '{0:,}'.format(pData['items'][slctn[x]['item']])
                if len(z) > c1:
                    c1 = len(str(pData['items'][slctn[x]['item']]))
    while True:
        scrn(dl['00'], dl['41'])
        ctrt('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
                dl['11'], t(d_trp), dl['14'], t(d_lctn), dl['42'], d_lst[0]['qty']))
        ctrt(' ')
        dvsn('-')
        ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}'.format(a, a1, b, b1, c, c1, d, d1))
        ctrt('{0}  {1}  {2}  {3}'.format('~' * a1, '~' * b1, '~' * c1, '~' * d1))
        reduced_time = (d_lst[0]['time'] / d_lst[0]['mltplr']) * d_lst[0]['qty']
        for x in range(len(d_speed)):
            ctrt('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}'.format(
                    d_speed[x]['desc'], a1, d_speed[x]['itm_dsc'], b1, d_speed[x]['qty'], c1, d_speed[x]['use'], d1))
            if d_speed[x]['use'] != 0:
                if d_speed[x]['time'] < 1:
                    for y in range(d_speed[x]['use']):
                        reduced_time *= (1 - d_speed[x]['time'])
                else:
                    for y in range(d_speed[x]['use']):
                        reduced_time -= d_speed[x]['time']
        else:
            reduced_time = 0 if reduced_time < 1 else cvttm(reduced_time)
            ctrt('{0}: {1}'.format(dl['36'], reduced_time), prefix=True, suffix=True)
        if reduced_time != 0:
            print(' {0}'.format(dl['37']))
        else:
            print(' {0}'.format(dl['38']))
        dvsn()
        d_select = input(' {0} : '.format(dl['05']))
        if len(d_select) >= 3:
            if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                return
            elif (d_select.lower() == dl['39'] or d_select.lower() == 'next') and reduced_time == 0:
                break
            else:
                try:
                    i_item, i_qty = d_select.split('@')
                    if i_qty.isnumeric():
                        for x in range(len(d_speed)):
                            if i_item.lower() == t(d_speed[x]['desc']).lower() and int(i_qty) <= d_speed[x]['qty']:
                                d_speed[x]['use'] = int(i_qty)
                                break
                        else:
                            for x in range(len(d_speed)):
                                if i_item.lower() in t(d_speed[x]['desc']).lower() and int(i_qty) <= d_speed[x]['qty']:
                                    d_speed[x]['use'] = int(i_qty)
                                    break
                except(TypeError, ValueError):
                    pass
    d_speed[:] = [d for d in d_speed if d.get('use') != 0]
    d_queue = int(d_lst[0]['trnbl'] / d_lst[0]['qty'])
    speed_cut_off = 0
    for x in range(len(d_speed)):
        if d_queue > (d_speed[x]['qty'] / d_speed[x]['use']):
            d_queue = int(d_speed[x]['qty'] / d_speed[x]['use'])
        if 'Testronius' not in d_speed[x]['item']:
            speed_cut_off += d_speed[x]['time']
    d_batch = 1 if d_queue == 1 else None
    while d_batch is None:
        scrn(dl['00'], dl['40'])
        ctrt('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
                dl['11'], t(d_trp), dl['14'], t(d_lctn), dl['42'], d_lst[0]['qty']))
        ctrt(' ')
        d_batch = stbtch(d_queue + 1, '{0}'.format(dl['43']))
        if d_batch == dl['06'] or d_batch == 'exit':
            return
    d_delay = None
    while d_delay is None:
        scrn(dl['00'], dl['44'])
        ctrt('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
                dl['11'], t(d_trp), dl['14'], t(d_lctn), dl['42'], d_lst[0]['qty']))
        ctrt('{0}: {1:,}'.format(dl['45'], d_batch))
        d_delay = stdly()
        if d_delay == dl['06'] or d_delay == 'exit':
            return
    d_proceed = False
    while not d_proceed:
        scrn(dl['00'], dl['46'])
        ctrt('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
                dl['11'], t(d_trp), dl['14'], t(d_lctn), dl['42'], d_lst[0]['qty']))
        ctrt('{0}: {1:,}   {2}: {3}s'.format(dl['45'], d_batch, dl['47'], d_delay))
        d_proceed = prcd()
        if d_proceed == dl['06'] or d_proceed == 'exit':
            return
    speeds_used, powders_used = [{}, {}]
    d_start = time()
    for x in range(d_batch):
        dur = -1
        job_id = 0
        for item in d_speed:
            for y in range(item['use']):
                if 'Testronius' in item['item'] and speed_cut_off >= dur != -1 or dur == 0:
                    break
                scrn(dl['00'], dl['48'])
                ctrt('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
                        dl['11'], t(d_trp), dl['14'], t(d_lctn), dl['42'], d_lst[0]['qty']))
                ctrt('{0}: {1:,}   {2}: {3}s   {4}: {5}'.format(
                        dl['45'], d_batch, dl['47'], d_delay, dl['49'], cvttm(time() - d_start)))
                dvsn('-')
                prg(x + 1, d_batch, '{0}: {1:,}/{2:,}'.format(dl['50'], x + 1, d_batch))
                if speeds_used or powders_used:
                    init = dl['09'] if dur == -1 else '{0}: {1}'.format(dl['51'], cvttm(dur))
                    prg(y + 1, item['use'], '{0} {1}'.format(dl['52'], item['desc']), init)
                    if powders_used:
                        ctrt('~~~ {0} ~~~'.format(dl['53']), prefix=True)
                        dsply(powders_used, single=False)
                    if speeds_used:
                        ctrt('~~~ {0} ~~~'.format(dl['54']), prefix=True)
                        dsply(speeds_used, single=False)
                    if x > 0:
                        ctrt('~~~ {0} ~~~'.format(dl['55']), prefix=True)
                        ctrt('{0:,}'.format(d_lst[0]['qty'] * x))
                        ctrt('~~~ {0} ~~~'.format(dl['56']), prefix=True)
                        ctrt('{0:,}'.format(d_lst[0]['qty'] * x * d_lst[0]['power']))
                else:
                    prg(0, 1, dl['09'])
                if dur == -1:
                    x_param = 'units%5Bquantity%5D={0}&units%5Bunit%5Ftype%5D={1}&%5Fmethod=post&'.format(
                            d_lst[0]['qty'], d_trp)
                    for server_retry in range(5):
                        sleep(d_delay)
                        try:
                            main_json = web_op('cities/{0}/units.json'.format(d_lst[0]['id']), x_param)
                            result = main_json['result']['success']
                            if result:
                                job_id = main_json['result']['job']['id']
                                dur = int(main_json['result']['job']['duration'])
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
                    else:
                        errmsg(dl['57'])
                if dur > 0:
                    x_param = 'job%5Fid={0}&%5Fmethod=delete&'.format(job_id)
                    for server_retry in range(5):
                        sleep(d_delay)
                        try:
                            item_json = web_op('player_items/{0}'.format(item['item']), x_param)
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
                    else:
                        z = dl['67'] if 'Testronius' in item['item'] else dl['58']
                        errmsg(z)
    scrn(dl['00'], dl['59'])
    ctrt('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
            dl['11'], t(d_trp), dl['14'], t(d_lctn), dl['42'], d_lst[0]['qty']))
    ctrt('{0}: {1:,}   {2}: {3}s'.format(dl['45'], d_batch, dl['47'], d_delay))
    dvsn('-')
    prg(1, 1, '{0} {1}'.format(dl['60'], cvttm(time() - d_start)))
    if powders_used:
        ctrt('~~~ {0} ~~~'.format(dl['53']), prefix=True)
        dsply(powders_used, single=False)
    if speeds_used:
        ctrt('~~~ {0} ~~~'.format(dl['54']), prefix=True)
        dsply(speeds_used, single=False)
    ctrt('~~~ {0} ~~~'.format(dl['55']), prefix=True)
    ctrt('{0:,}'.format(d_lst[0]['qty'] * d_batch))
    ctrt('~~~ {0} ~~~'.format(dl['56']), prefix=True)
    ctrt('{0:,}'.format(d_lst[0]['qty'] * d_batch * d_lst[0]['power']))
    dvsn()
    input(dl['61'])
    print(dl['62'])
    gtdt(pl=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #


def revive_soul():
    dl = {'00': lo['b77'], '01': lo['c04'], '02': lo['a05'], '03': lo['a11'], '04': lo['c31'], '05': lo['a52'],
          '06': lo['a59'], '07': lo['b49'], '08': lo['b47'], '09': lo['a92'], '10': lo['c72'], '11': lo['c25'],
          '12': lo['b75'], '13': lo['c27'], '14': lo['b07'], '15': lo['a44'], '16': lo['c58'], '17': lo['a13'],
          '18': lo['c76'], '19': lo['c17'], '20': lo['b25'], '21': lo['b10'], '22': lo['a40'], '23': lo['a39'],
          '24': lo['a41'], '25': lo['a20'], '26': lo['a18'], '27': lo['a21'], '28': lo['a22'], '29': lo['a23'],
          '30': lo['b03'], '31': lo['a99'], '32': lo['c21'], '33': lo['a83'], '34': lo['a19'], '35': lo['b59'],
          '36': lo['b76'], '37': lo['b24'], '38': lo['a51'], '39': lo['b16'], '40': lo['b29'], '41': lo['c18'],
          '42': lo['b53'], '43': lo['a84'], '44': lo['c15'], '45': lo['c34'], '46': lo['b57'], '47': lo['a43'],
          '48': lo['b51'], '49': lo['a47'], '50': lo['a58'], '51': lo['b64'], '52': lo['b80'], '53': lo['c40'],
          '54': lo['c28'], '55': lo['c26'], '56': lo['b45'], '57': lo['b86'], '58': lo['b79'], '59': lo['b52']}
    scrn(dl['00'], dl['01'])
    ctrt(dl['09'])
    d_lst, dp_level, dp_total, dp_combo, d_lctn = [list(), 0, 0, 0, 'spectral']
    try:
        spec = cData[d_lctn]['city']['buildings']
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
                    if dp_level >= mData['units'][x]['requirements'][d_lctn]['buildings']['DarkPortal'] and be >= \
                            mData['units'][x]['requirements'][d_lctn]['resources']['blue_energy']:
                        y = int(be / mData['units'][x]['requirements'][d_lctn]['resources']['blue_energy'])
                        if y > value:
                            y = value
                        multiplier = dp_total + ((dp_combo - dp_total) / 10)
                        my_dict = {'troop': key, 'total': value, 'quantity': y, 'time': mData['units'][x]['time'],
                                   'multiplier': multiplier, 'desc': t(key), 'id': cData[d_lctn]['city']['id'],
                                   'power': mData['units'][x]['stats']['power']}
                        d_lst.append(my_dict)
    if not d_lst:
        nthng(dl['00'], dl['01'], dl['02'])
        return
    if len(d_lst) == 1:
        d_troop = d_lst[0]['troop']
    else:
        d_lst = sorted(d_lst, key=itemgetter('desc'))
        d_troop = None
        a, b, c = [dl['11'], dl['16'], dl['12']]
        a1, b1, c1 = [len(a), len(b), len(c)]
        for x in range(len(d_lst)):
            if len(d_lst[x]['desc']) > a1:
                a1 = len(d_lst[x]['desc'])
            if len('{0:,}'.format(d_lst[x]['total'])) > b1:
                b1 = len('{0:,}'.format(d_lst[x]['total']))
            if len('{0:,}'.format(d_lst[x]['quantity'])) > c1:
                c1 = len('{0:,}'.format(d_lst[x]['quantity']))
        while d_troop is None:
            scrn(dl['00'], dl['01'])
            ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}'.format(a, a1, b, b1, c, c1))
            ctrt('{0}  {1}  {2}'.format('~' * a1, '~' * b1, '~' * c1))
            for x in range(len(d_lst)):
                ctrt('{0:<{1}}  {2:>{3},}  {4:>{5},}'.format(
                        d_lst[x]['desc'], a1, d_lst[x]['total'], b1, d_lst[x]['quantity'], c1))
            dvsn()
            d_select = input(' {0} : '.format(dl['05']))
            if len(d_select) >= 3:
                if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                    return
                else:
                    for x in range(len(d_lst)):
                        if d_select.lower() == d_lst[x]['desc'].lower():
                            d_troop = d_lst[x]['troop']
                            break
                    else:
                        for x in range(len(d_lst)):
                            if d_select.lower() in d_lst[x]['desc'].lower():
                                d_troop = d_lst[x]['troop']
                                break
    d_lst[:] = [d for d in d_lst if d.get('troop') == d_troop]
    if d_lst[0]['total'] > 1:
        d_queue = 0
        while d_queue is 0:
            scrn(dl['00'], dl['19'])
            ctrt('{0}: {1}   {2}: {3}'.format(dl['11'], t(d_troop), dl['14'], t(d_lctn)))
            ctrt(' ')
            dvsn('-')
            ctrt('~~~ {0} ~~~'.format(dl['03']))
            ctrt('1 - {0}'.format(d_lst[0]['quantity']), suffix=True)
            print(' {0}'.format(dl['20']))
            dvsn()
            d_select = input(' {0} : '.format(dl['05']))
            if len(d_select) >= 1:
                if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                    return
                elif d_select.lower() == dl['21'] or d_select.lower() == 'max':
                    d_queue = d_lst[0]['quantity']
                elif d_select.isnumeric():
                    if int(d_select) in range(1, d_lst[0]['quantity'] + 1):
                        d_queue = int(d_select)
        d_lst[0]['quantity'] = d_queue
    a, b, c, d = [dl['13'], dl['15'], dl['59'], dl['18']]
    a1, b1, c1, d1 = [len(a), len(b), len(c), len(d)]
    slctn = [{'item': 'DarkTestroniusInfusion', 'time': 0.99, 'desc': dl['22']},
             {'item': 'DarkTestroniusDeluxe', 'time': 0.5, 'desc': dl['23']},
             {'item': 'DarkTestroniusPowder', 'time': 0.3, 'desc': dl['24']},
             {'item': 'Blitz', 'time': 345600, 'desc': dl['25']},
             {'item': 'Blast', 'time': 216000, 'desc': dl['26']},
             {'item': 'Bolt', 'time': 86400, 'desc': dl['27']},
             {'item': 'Bore', 'time': 54000, 'desc': dl['28']},
             {'item': 'Bounce', 'time': 28800, 'desc': dl['29']},
             {'item': 'Leap', 'time': 9000, 'desc': dl['30']},
             {'item': 'Jump', 'time': 3600, 'desc': dl['31']},
             {'item': 'Skip', 'time': 900, 'desc': dl['32']},
             {'item': 'Hop', 'time': 300, 'desc': dl['33']},
             {'item': 'Blink', 'time': 60, 'desc': dl['34']}]
    d_speed = list()
    for x in range(len(slctn)):
        if slctn[x]['item'] in pData['items']:
            if pData['items'][slctn[x]['item']] > 0:
                if slctn[x]['time'] < 1:
                    y = '{0}% {1}'.format(int(slctn[x]['time'] * 100), dl['35'])
                else:
                    y = cvttm(slctn[x]['time'], ss=False)
                my_dict = {'item': slctn[x]['item'], 'qty': pData['items'][slctn[x]['item']],
                           'time': slctn[x]['time'], 'dsc': y, 'use': 0, 'desc': slctn[x]['desc']}
                d_speed.append(my_dict)
                if len(slctn[x]['desc']) > a1:
                    a1 = len(slctn[x]['desc'])
                if len(y) > b1:
                    b1 = len(y)
                if len('{0:,}'.format(pData['items'][slctn[x]['item']])) > c1:
                    c1 = len(str(pData['items'][slctn[x]['item']]))
    while True:
        scrn(dl['00'], dl['41'])
        ctrt('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
                dl['11'], t(d_troop), dl['14'], t(d_lctn), dl['42'], d_lst[0]['quantity']))
        ctrt(' ')
        dvsn('-')
        ctrt('{0:^{1}}  {2:^{3}}  {4:^{5}}  {6:^{7}}'.format(a, a1, b, b1, c, c1, d, d1))
        ctrt('{0}  {1}  {2}  {3}'.format('~' * a1, '~' * b1, '~' * c1, '~' * d1))
        reduced_time = (d_lst[0]['time'] * d_lst[0]['quantity'] * 0.15 / d_lst[0]['multiplier'])
        for x in range(len(d_speed)):
            ctrt('{0:<{1}}  {2:>{3}}  {4:>{5},}  {6:>{7}}'.format(
                    d_speed[x]['desc'], a1, d_speed[x]['dsc'], b1, d_speed[x]['qty'], c1, d_speed[x]['use'], d1))
            if d_speed[x]['use'] != 0:
                if d_speed[x]['time'] < 1:
                    for y in range(d_speed[x]['use']):
                        reduced_time *= (1 - d_speed[x]['time'])
                else:
                    for y in range(d_speed[x]['use']):
                        reduced_time -= d_speed[x]['time']
        else:
            reduced_time = 0 if reduced_time < 0 else cvttm(reduced_time)
            ctrt('{0}: {1}'.format(dl['36'], reduced_time), prefix=True, suffix=True)
        if reduced_time != 0:
            print(' {0}'.format(dl['37']))
        else:
            print(' {0}'.format(dl['38']))
        dvsn()
        d_select = input(' {0} : '.format(dl['05']))
        if len(d_select) >= 3:
            if d_select.lower() == dl['06'] or d_select.lower() == 'exit':
                return
            elif (d_select.lower() == dl['39'] or d_select.lower() == 'next') and reduced_time == 0:
                break
            else:
                try:
                    i_item, i_qty = d_select.split('@')
                    if i_qty.isnumeric():
                        for x in range(len(d_speed)):
                            if i_item.lower() == d_speed[x]['desc'].lower() and int(i_qty) < d_speed[x]['qty']:
                                d_speed[x]['use'] = int(i_qty)
                                break
                        else:
                            for x in range(len(d_speed)):
                                if i_item.lower() in d_speed[x]['desc'].lower() and int(i_qty) < d_speed[x]['qty']:
                                    d_speed[x]['use'] = int(i_qty)
                                    break
                except(TypeError, ValueError):
                    pass
    d_speed[:] = [d for d in d_speed if d.get('use') != 0]
    d_queue = int(d_lst[0]['total'] / d_lst[0]['quantity'])
    speed_cut_off = 0
    for x in range(len(d_speed)):
        if d_queue > (d_speed[x]['qty'] / d_speed[x]['use']):
            d_queue = int(d_speed[x]['qty'] / d_speed[x]['use'])
        if 'Testronius' not in d_speed[x]['item']:
            speed_cut_off += d_speed[x]['time']
    d_batch = 1 if d_queue == 1 else None
    while d_batch is None:
        scrn(dl['00'], dl['40'])
        ctrt('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
                dl['11'], t(d_troop), dl['14'], t(d_lctn), dl['42'], d_lst[0]['quantity']))
        ctrt(' ')
        d_batch = stbtch(d_queue + 1, dl['43'])
        if d_batch == dl['06'] or d_batch == 'exit':
            return
    d_delay = None
    while d_delay is None:
        scrn(dl['00'], dl['44'])
        ctrt('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
                dl['11'], t(d_troop), dl['14'], t(d_lctn), dl['42'], d_lst[0]['quantity']))
        ctrt('{0}: {1:,}'.format(dl['45'], d_batch))
        d_delay = stdly()
        if d_delay == dl['06'] or d_delay == 'exit':
            return
    d_proceed = False
    while not d_proceed:
        scrn(dl['00'], dl['46'])
        ctrt('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
                dl['11'], t(d_troop), dl['14'], t(d_lctn), dl['42'], d_lst[0]['quantity']))
        ctrt('{0}: {1:,}   {2}: {3}s'.format(dl['45'], d_batch, dl['47'], d_delay))
        d_proceed = prcd()
        if d_proceed == dl['06'] or d_proceed == 'exit':
            return
    speeds_used, powders_used = [{}, {}]
    d_start = time()
    for x in range(d_batch):
        dur = -1
        job_id = 0
        for item in d_speed:
            for y in range(item['use']):
                if 'Testronius' in item['item'] and speed_cut_off >= dur != -1 or dur == 0:
                    break
                scrn(dl['00'], dl['48'])
                ctrt('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
                        dl['11'], t(d_troop), dl['14'], t(d_lctn), dl['42'], d_lst[0]['quantity']))
                ctrt('{0}: {1:,}   {2}: {3}s   {4}: {5}'.format(
                        dl['45'], d_batch, dl['47'], d_delay, dl['49'], cvttm(time() - d_start)))
                dvsn('-')
                prg(x + 1, d_batch, '{0}: {1:,}/{2:,}'.format(dl['50'], x + 1, d_batch))
                if speeds_used or powders_used:
                    init = dl['09'] if dur == -1 else '{0}: {1}'.format(dl['51'], cvttm(dur))
                    prg(y + 1, item['use'], '{0} {1}'.format(dl['02'], t(item['item'])), init)
                    if powders_used:
                        ctrt('~~~ {0} ~~~'.format(dl['53']), prefix=True)
                        dsply(powders_used, single=False)
                    if speeds_used:
                        ctrt('~~~ {0} ~~~'.format(dl['54']), prefix=True)
                        dsply(speeds_used, single=False)
                    if x > 0:
                        ctrt('~~~ {0} ~~~'.format(dl['55']), prefix=True)
                        ctrt('{0:,}'.format(d_lst[0]['quantity'] * x))
                        ctrt('~~~ {0} ~~~'.format(dl['56']), prefix=True)
                        ctrt('{0:,}'.format(d_lst[0]['quantity'] * x * d_lst[0]['power']))
                else:
                    prg(0, 1, dl['09'])
                if dur == -1:
                    x_param = 'units%5Bquantity%5D={0}&units%5Bunit%5Ftype%5D={1}&%5Fmethod=post&'.format(
                            d_lst[0]['quantity'], d_troop)
                    for server_retry in range(5):
                        sleep(d_delay)
                        try:
                            main_json = web_op('cities/{0}/units/resurrect.json'.format(d_lst[0]['id']), x_param)
                            result = main_json['result']['success']
                            if result:
                                job_id = main_json['result']['job']['id']
                                dur = int(main_json['result']['job']['duration'])
                                break
                        except (KeyError, TypeError):
                            sleep(1)
                            continue
                    else:
                        z = dl['52'] if 'Testronius' in item['item'] else dl['58']
                        errmsg(z)
                if dur > 0:
                    x_param = 'job%5Fid={0}&%5Fmethod=delete&'.format(job_id)
                    for server_retry in range(5):
                        sleep(d_delay)
                        try:
                            item_json = web_op('player_items/{0}'.format(item['item']), x_param)
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
                    else:
                        errmsg(dl['58'])
    scrn(dl['00'], dl['04'])
    ctrt('{0}: {1}   {2}: {3}   {4}: {5:,}'.format(
            dl['11'], t(d_troop), dl['14'], t(d_lctn), dl['42'], d_lst[0]['quantity']))
    ctrt('{0}: {1:,}   {2}: {3}s'.format(dl['45'], d_batch, dl['47'], d_delay))
    dvsn('-')
    prg(1, 1, '{0} {1}'.format(dl['07'], cvttm(time() - d_start)))
    if powders_used:
        ctrt('~~~ {0} ~~~'.format(dl['53']), prefix=True)
        dsply(powders_used, single=False)
    if speeds_used:
        ctrt('~~~ {0} ~~~'.format(dl['54']), prefix=True)
        dsply(speeds_used, single=False)
    ctrt('~~~ {0} ~~~'.format(dl['55']), prefix=True)
    ctrt('{0:,}'.format(d_lst[0]['quantity'] * d_batch))
    ctrt('~~~ {0} ~~~'.format(dl['56']), prefix=True)
    ctrt('{0:,}'.format(d_lst[0]['quantity'] * d_batch * d_lst[0]['power']))
    dvsn()
    input(dl['08'])
    print(dl['10'])
    gtdt(pl=True, unmute=False)


# -------------------------------------------------------------------------------------------------------------------- #

def switch_realm(title='', realm_no=0, c_no=0):
    dl = {'00': lo['c32']}
    global d_rn, d_cn, realm, cookie, std_param, d_si, d_conn
    x = dl['00'] if not title else title
    d_rn = realm_no
    d_cn = c_no
    gtrlm(x)
    d_si = b2a_hex(os.urandom(16))
    realm = 'realm{0}.c{1}.castle.rykaiju.com'.format(d_rn, d_cn)
    d_conn = http.client.HTTPConnection(realm, 80)
    cookie = 'dragons={0}'.format(d_si)
    std_param = 'dragon%5Fheart={0}&user%5Fid={1}&version=overarch&%5Fsession%5Fid={2}'.format(d_dh, d_ui, d_si)
    refresh_data()


# -------------------------------------------------------------------------------------------------------------------- #

def refresh_data():
    global pData, mData, fData, pfData, cData, tData
    gtdt(pl=True, fm=True, pf=True, op=True, w1=True, w2=True, w3=True, unmute=True)


# -------------------------------------------------------------------------------------------------------------------- #
#                                                      MENU CLASS                                                      #
# -------------------------------------------------------------------------------------------------------------------- #
def menu():
    dl = {'00': lo['b08'], '01': lo['c82'], '02': lo['c63'], '03': lo['a80'], '04': lo['c33'], '05': lo['b27'],
          '06': lo['a52'], '07': lo['b54'], '08': lo['a31'], '09': lo['a61'], '10': lo['a69'], '11': lo['a73'],
          '12': lo['b06'], '13': lo['b36'], '14': lo['b60'], '15': lo['b77'], '16': lo['c32'], '17': lo['c59'],
          '18': lo['c69'], '19': lo['c73'], '20': lo['a29'], '21': lo['b09'], '22': lo['b78']}
    module_dict = {craft_equipment: dl['08'].title(), forge_ingredient: dl['11'].title(),
                   farm_mission: dl['09'].title(), open_chest: dl['13'].title(), unpack_arsenal: dl['18'].title(),
                   upgrade_building: dl['19'].title(), fill_slot: dl['10'].title(), train_troop: dl['17'].title(),
                   revive_soul: dl['15'].title()}
    system_dict = {switch_realm: dl['16'].title(), refresh_data: dl['14'].title(), scpnt: dl['12'].title(),
                   chslng: dl['20'].title()}
    while True:
        scrn(dl['00'], dl['01'])
        ctrt('~~~ {0} ~~~'.format(dl['03']))
        dsply(module_dict)
        ctrt('~~~ {0} ~~~'.format(dl['04']), prefix=True)
        dsply(system_dict)
        print('\n {0}'.format(dl['05']))
        dvsn()
        d_select = input(' {0} : '.format(dl['06']))
        if len(d_select) >= 2:
            if d_select.lower() == dl['07'] or d_select.lower() == 'quit':
                scpxt()
            else:
                for menu_dict in (module_dict, system_dict):
                    for key, value in menu_dict.items():
                        if d_select.lower() == value.lower():
                            key()
                            break
                    else:
                        for key, value in menu_dict.items():
                            if d_select.lower() in value.lower():
                                key()
                                break


# -------------------------------------------------------------------------------------------------------------------- #
#                                                         MAIN                                                         #
# -------------------------------------------------------------------------------------------------------------------- #
d_dh, d_si, realm, cookie, std_param, d_conn, d_ui, d_rn, d_cn = [None, None, None, None, None, None, None, None, None]
pData, mData, fData, pfData, cData, fStat, lo, tData = [None, None, None, None, None, None, None, {}]
try:
    with open('locale.doa', 'r') as load_file:
        lo = json.load(load_file)
        if lo['a00'] == __version__:
            pass
except FileNotFoundError:
    chslng(title=False, shut_script=False)
except KeyError:
    del lo
    os.remove('locale.doa')
    chslng(title=False, shut_script=False)
for tlookup in ('dict_f_eqp', 'dict_build', 'dict_troop', 'dict_f_adv', 'dict_f_mis', 'dict_f_itm'):
    for tkey, tvalue in lo[tlookup].items():
        if tkey not in tData:
            tData[tkey] = tvalue
if __name__ == '__main__':
    scpnt()
    chkver()
    menu()
