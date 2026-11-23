"""Install the official tunnel helper locally, checking GitHub's asset digest."""
from pathlib import Path
import hashlib
import json
import os
import urllib.request


def main():
    if os.name!='nt': raise SystemExit('Use the official Cloudflare package for your OS and set STACK_CLOUDFLARED.')
    root=Path(__file__).resolve().parents[1]
    target=root/'.tools'/'free-online'/'cloudflared.exe'
    request=urllib.request.Request('https://api.github.com/repos/cloudflare/cloudflared/releases/latest',headers={'User-Agent':'Stack-Moko-Baby-Setup'})
    with urllib.request.urlopen(request,timeout=30) as response: release=json.load(response)
    asset=next(a for a in release['assets'] if a['name']=='cloudflared-windows-amd64.exe')
    if not asset['browser_download_url'].startswith('https://github.com/cloudflare/cloudflared/releases/download/'):
        raise RuntimeError('Unexpected download source.')
    expected=asset.get('digest','')
    if not expected.startswith('sha256:'): raise RuntimeError('The official release has no SHA-256 asset digest; use the documented manual install.')
    with urllib.request.urlopen(asset['browser_download_url'],timeout=60) as response: content=response.read()
    if hashlib.sha256(content).hexdigest()!=expected.split(':',1)[1]: raise RuntimeError('Download integrity check failed.')
    target.parent.mkdir(parents=True,exist_ok=True)
    temporary=target.with_suffix('.download')
    temporary.write_bytes(content); temporary.replace(target)
    print(f'Official cloudflared {release["tag_name"]} installed locally; SHA-256 verified.')


if __name__=='__main__': main()
