"""Prepare ignored firmware config without printing the private token.

Pass --ca a PEM trust anchor exported from your HTTPS certificate chain.
The source stays local; uploading it to Wokwi is an explicit user action.
"""
import argparse
import json
import os
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]


def private_lan(host):
    """Same RFC 1918 ranges the firmware accepts (Android 192.168/10, iPhone 172.20.10)."""
    if host.startswith(('192.168.','10.')): return True
    parts=host.split('.')
    return len(parts)==4 and parts[0]=='172' and parts[1].isdigit() and 16<=int(parts[1])<=31


def wifi_problem(ssid,password):
    """Return a plain-language problem with the hotspot name/password, never echoing the password."""
    if not ssid or len(ssid.encode('utf-8'))>32:
        return 'The Wi-Fi name must be 1-32 characters.'
    if not all(' '<=ch<='~' for ch in ssid):
        return ('Rename the hotspot to plain letters, numbers and spaces (iPhone names often use a curly '
                'apostrophe, e.g. "Alex’s iPhone"). Then set STACK_FIRMWARE_WIFI_SSID to the new name.')
    if password and (not 8<=len(password)<=63 or not all(' '<=ch<='~' for ch in password)):
        return 'The hotspot password must be 8-63 plain ASCII characters.'
    return None


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',required=True)
    parser.add_argument('--ca',type=Path)
    parser.add_argument('--local-http',action='store_true')
    parser.add_argument('--ssid',default=os.getenv('STACK_FIRMWARE_WIFI_SSID') or 'Wokwi-GUEST')
    parser.add_argument('--cloud',action='store_true',help='Use STACK_FIRMWARE_DEVICE_TOKEN instead of the local backend token.')
    args=parser.parse_args()
    password=os.getenv('STACK_FIRMWARE_WIFI_PASSWORD','')
    problem=wifi_problem(args.ssid,password)
    if problem: parser.error(problem)
    url=urlsplit(args.url)
    local=url.hostname in ('host.wokwi.internal','localhost','127.0.0.1') or private_lan(url.hostname or '')
    if (url.scheme!='https' and not (args.local_http and url.scheme=='http' and local)) or url.path not in ('','/') or url.query or url.fragment or url.username or url.password:
        parser.error('Use an HTTPS origin, or explicit local HTTP with the private Wokwi gateway.')
    ca=args.ca.read_text(encoding='utf-8') if args.ca else ''
    if url.scheme=='https' and '-----BEGIN CERTIFICATE-----' not in ca:
        parser.error('Supply --ca with the HTTPS trust anchor PEM. TLS verification is required.')
    from dotenv import dotenv_values
    token=os.getenv('STACK_FIRMWARE_DEVICE_TOKEN') if args.cloud else dotenv_values(ROOT/'backend'/'.env').get('STACK_DEVICE_TOKEN')
    if not token: parser.error('Run backend setup first; no device token was printed.')
    values={'STACK_WIFI_SSID':args.ssid,'STACK_WIFI_PASSWORD':password,'STACK_API_BASE':args.url.rstrip('/'),
            'STACK_DEVICE_TOKEN':token,'STACK_ROOT_CA':ca}
    content='#pragma once\n'+''.join(f'#define {key} {json.dumps(value)}\n' for key,value in values.items())
    content+=f'#define STACK_ALLOW_LOCAL_HTTP {int(args.local_http)}\n#define STACK_USE_PIEZO 1\n#define STACK_USE_DFPLAYER 0\n#define STACK_DFPLAYER_VOLUME 8\n#define STACK_COUNTDOWN_STEP_MS 500\n'
    target=ROOT/'firmware'/'stack_moko_baby'/'config.h'
    target.write_text(content,encoding='utf-8')
    print('Private firmware config saved locally. Keep it out of public Wokwi projects and Git.')


if __name__=='__main__': main()
