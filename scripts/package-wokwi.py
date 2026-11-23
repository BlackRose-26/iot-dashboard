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
    with ZipFile(target,'w',ZIP_DEFLATED) as archive:
        for name,entry in files.items(): archive.write(source/name,entry)
    print('Public source bundle saved in docs/device-artifacts/stack-moko-baby-wokwi.zip (no event credentials).')


if __name__=='__main__': main()
