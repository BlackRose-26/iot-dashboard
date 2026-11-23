"""Create fresh cloud secrets in an ignored local file; never prints their values."""
import base64
from pathlib import Path
import secrets


def main():
    target=Path(__file__).resolve().parents[1]/'.tools'/'render'/'initial-secrets.env'
    if target.exists():
        print('Existing deployment secrets preserved in .tools/render/initial-secrets.env.')
        return
    values={f'STACK_{name}_KEY':base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
            for name in ('IDENTITY','LOOKUP','CSRF')}
    values.update(STACK_DEVICE_TOKEN=secrets.token_urlsafe(40),STACK_INITIAL_ADMIN_PASSWORD=secrets.token_urlsafe(24))
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('x',encoding='utf-8') as output:
        output.write('\n'.join(f'{key}={value}' for key,value in values.items())+'\n')
    print('Fresh cloud secrets saved in .tools/render/initial-secrets.env; keep this file private.')


if __name__=='__main__': main()
