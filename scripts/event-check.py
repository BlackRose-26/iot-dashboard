"""Event-day laptop check: will this PC keep the dashboard, tunnel and cabinet running?

  npm run event:check                 read-only report (default)
  npm run event:check -- --fix-power  on the charger: never sleep or hibernate, closing the lid
                                      does nothing, USB power-saving off (current power plan only)

Checks MySQL, the charger, sleep/hibernate/lid settings, USB selective suspend, a pending
Windows restart, free disk space for backups and the files the launcher needs. Power
changes apply to "plugged in" only; battery settings are left alone. Undo them in
Settings > System > Power, or with: powercfg -restoredefaultschemes (resets all plans).
"""
import argparse
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HIDDEN = {'creationflags': 0x08000000} if os.name == 'nt' else {}
SLEEP, STANDBY, HIBERNATE = 'SUB_SLEEP', 'STANDBYIDLE', 'HIBERNATEIDLE'
BUTTONS, LID = 'SUB_BUTTONS', 'LIDACTION'
USB, USB_SUSPEND = '2a737441-1930-4402-8d77-b2bebba308a3', '48e6b7a6-50f5-4782-a5d4-53bb8f07e226'


def run(*command):
    result = subprocess.run(command, capture_output=True, text=True, **HIDDEN)
    return result.returncode, result.stdout + result.stderr


def power_value(group, setting):
    code, text = run('powercfg', '/query', 'SCHEME_CURRENT', group, setting)
    values = {}
    for line in text.splitlines():
        if 'Current AC Power Setting Index' in line: values['ac'] = int(line.split(':')[-1].strip(), 16)
        if 'Current DC Power Setting Index' in line: values['dc'] = int(line.split(':')[-1].strip(), 16)
    return values


def port_open(port):
    with socket.socket() as probe:
        probe.settimeout(1.5)
        return probe.connect_ex(('127.0.0.1', port)) == 0


def on_charger():
    code, text = run('powershell', '-NoProfile', '-Command',
                     '(Get-CimInstance Win32_Battery | Select-Object -First 1).BatteryStatus')
    text = text.strip()
    if not text: return None  # no battery (desktop) or not reported
    return text in ('2', '3', '6', '7', '8', '9', '11')  # AC / charging states


def pending_restart():
    keys = [r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired',
            r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending']
    return any(run('reg', 'query', key)[0] == 0 for key in keys)


def checks():
    results = []

    def add(ok, label, fix=''):
        results.append((ok, label, fix))
    mysql = port_open(3306)
    add(mysql, 'MySQL is running' if mysql else 'MySQL is not running',
        '' if mysql else 'npm run online starts XAMPP MySQL automatically; or start it in the XAMPP Control Panel.')
    service = run('sc', 'query', 'mysql')[0] == 0
    add(True, 'MySQL runs as a Windows service' if service else
        'MySQL is not a Windows service (fine: npm run online starts it and restarts it if it stops)')
    charger = on_charger()
    if charger is None:
        add(True, 'No battery reported: this looks like a desktop PC. Run this check again on the event laptop.')
    else:
        add(charger, 'Laptop is on the charger' if charger else 'Laptop is on battery',
            '' if charger else 'Plug in the charger: the laptop powers the ESP32 and the LED panels.')
    standby, hibernate = power_value(SLEEP, STANDBY), power_value(SLEEP, HIBERNATE)
    add(standby.get('ac') == 0, 'Plugged in: never sleeps' if standby.get('ac') == 0 else
        f"Plugged in: sleeps after {standby.get('ac', 0)//60} min", 'Run with --fix-power.')
    if hibernate:
        add(hibernate.get('ac') == 0, 'Plugged in: never hibernates' if hibernate.get('ac') == 0 else
            f"Plugged in: hibernates after {hibernate.get('ac', 0)//60} min", 'Run with --fix-power.')
    lid = power_value(BUTTONS, LID)
    names = {0: 'does nothing', 1: 'sleeps', 2: 'hibernates', 3: 'shuts down'}
    if 'ac' not in lid:
        add(True, 'No lid setting on this PC')
    else:
        add(lid['ac'] == 0, f"Plugged in: closing the lid {names.get(lid['ac'], 'does something else')}",
            '' if lid['ac'] == 0 else 'Run with --fix-power, or keep the lid open.')
    usb = power_value(USB, USB_SUSPEND)
    if usb:
        add(usb.get('ac') == 0, 'Plugged in: USB power-saving is off' if usb.get('ac') == 0 else
            'Plugged in: USB power-saving (selective suspend) is on', 'Run with --fix-power.')
    restart = pending_restart()
    add(not restart, 'No Windows restart pending' if not restart else 'Windows wants to restart',
        'Restart and install updates the day before, then pause updates (Settings > Windows Update > Pause).')
    backups = Path(os.getenv('STACK_BACKUP_DIR') or Path.home()/'StackMokoBaby-backups')
    free_gb = shutil.disk_usage(backups if backups.exists() else Path.home()).free / 1e9
    add(free_gb >= 2, f'{free_gb:.0f} GB free for backups', 'Free up disk space (at least 2 GB).')
    needed = {'backend/.env': 'run the local setup', 'frontend/dist/index.html': 'the launcher builds it',
              '.tools/free-online/cloudflared.exe': 'run scripts/install-cloudflared.py'}
    for path, fix in needed.items():
        present = (ROOT/path).exists()
        add(present or path.startswith('frontend'), f'{path} present' if present else f'{path} missing', '' if present else fix)
    add(not port_open(8000), 'Port 8000 is free for the launcher' if not port_open(8000) else
        'Port 8000 is in use (an API is already running)', 'Stop the other terminal before npm run online.')
    return results


def fix_power():
    commands = [('powercfg', '/change', 'standby-timeout-ac', '0'),
                ('powercfg', '/change', 'hibernate-timeout-ac', '0'),
                ('powercfg', '/setacvalueindex', 'SCHEME_CURRENT', USB, USB_SUSPEND, '0'),
                ('powercfg', '/setactive', 'SCHEME_CURRENT')]
    if 'ac' in power_value(BUTTONS, LID):  # desktops have no lid setting
        commands.insert(2, ('powercfg', '/setacvalueindex', 'SCHEME_CURRENT', BUTTONS, LID, '0'))
    for command in commands:
        code, text = run(*command)
        if code: print(f'Could not apply {" ".join(command[1:3])}: {text.strip()[:200]}')
    print('Power settings applied for "plugged in". Battery settings unchanged.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--fix-power', action='store_true')
    args = parser.parse_args(argv)
    if os.name != 'nt':
        print('This check is for the Windows event laptop.'); return 0
    if args.fix_power: fix_power()
    results = checks()
    for ok, label, fix in results:
        print(f"[{'OK' if ok else 'FIX'}] {label}" + (f'  ->  {fix}' if not ok and fix else ''))
    problems = sum(not ok for ok, _, _ in results)
    print(f'\n{problems} item(s) to fix.' if problems else '\nThis laptop is ready for the event.')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
