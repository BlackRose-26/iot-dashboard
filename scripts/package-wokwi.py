"""Package public firmware sources only. Never include config.h or binaries."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def main():
    root=Path(__file__).resolve().parents[1]
    source=root/'firmware'/'stack_moko_baby'
    target=root/'docs'/'device-artifacts'/'stack-moko-baby-wokwi.zip'
    files={'stack_moko_baby.ino':'sketch.ino','game_engine.h':'game_engine.h',
           'transport_job.hpp':'transport_job.hpp','config.example.h':'config.example.h',
           'diagram.json':'diagram.json','libraries.txt':'libraries.txt'}
    target.parent.mkdir(parents=True,exist_ok=True)
    layout=(source/'display_layout.h').read_text(encoding='utf-8')
    # Wokwi's led-matrix part is row-serpentine only; the physical HUD default is column-major.
    wokwi_layout=layout.replace('#define STACK_HUD_COLUMN_MAJOR 1','#define STACK_HUD_COLUMN_MAJOR 0',1)
    if wokwi_layout==layout: raise SystemExit('display_layout.h changed; update the Wokwi HUD override.')
    with ZipFile(target,'w',ZIP_DEFLATED) as archive:
        for name,entry in files.items(): archive.write(source/name,entry)
        archive.writestr('display_layout.h',wokwi_layout)
    print('Public source bundle saved in docs/device-artifacts/stack-moko-baby-wokwi.zip (no event credentials).')


if __name__=='__main__': main()
