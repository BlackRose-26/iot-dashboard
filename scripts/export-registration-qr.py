"""Export the current event's public QR only; never export identity or auth data."""
import argparse
from pathlib import Path
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
sys.path.insert(0, str(ROOT / '.tools' / 'qr-export-libs'))

from app.config import Settings
from app.database import make_engine, one
import qrcode


def main():
    parser = argparse.ArgumentParser(description='Save the active Stack Moko Baby registration QR as a PNG.')
    parser.add_argument('--base-url', default=None, help='Public event website address, without /scan or /join')
    args = parser.parse_args()
    settings = Settings.load()
    address = urlsplit(args.base_url or settings.public_url)
    if address.scheme not in ('http', 'https') or not address.netloc or address.username or address.password or address.query or address.fragment or address.path not in ('', '/'):
        raise SystemExit('Supply an HTTP or HTTPS website address without a page path.')
    engine = make_engine(settings.database_url)
    try:
        with engine.connect() as connection:
            link = one(connection, '''SELECT q.token FROM qr_links q
              JOIN machines m ON m.id=q.machine_id AND m.event_id=q.event_id
              JOIN events e ON e.id=q.event_id
              WHERE q.enabled=1 AND m.enabled=1 AND e.code='acs-day'
              AND m.code='cabinet-01' ORDER BY q.id DESC LIMIT 1''')
        if not link:
            raise SystemExit('There is no active registration QR for Cabinet 01.')
        payload = f'{address.scheme}://{address.netloc}/join/{link["token"]}'
        code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=4)
        code.add_data(payload)
        code.make(fit=True)
        destination = ROOT / 'frontend' / 'public' / 'stack-moko-baby-registration-qr.png'
        destination.parent.mkdir(parents=True, exist_ok=True)
        code.make_image(fill_color='black', back_color='white').convert('RGB').save(destination, format='PNG')
        print(f'Saved QR image: {destination}')
    finally:
        engine.dispose()


if __name__ == '__main__':
    main()
