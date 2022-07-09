
""" This file will be converted into an .exe, packaged with the game files. """

import functools
import hashlib
import os
import shutil
import struct
import sys
import time
from tkinter import Tk, filedialog


# CWD should be set to DARK SOULS REMASTERED directory (run this script/exe from inside it).


def install_superhot(resource_path):
    """ Run the installation script in the current working directory. """

    # Check we're in the right directory by looking for the EXE.
    if not os.path.isfile('DarkSoulsRemastered.exe'):
        input("Could not find 'DarkSoulsRemastered.exe'. Make sure you're\n"
              "running this in the 'DARK SOULS REMASTERED' folder in your\n"
              "Steam files.\n\n"
              "Aborting installation. Press Enter to quit.")
        return

    # BEGIN INSTALLATION

    # Backup existing files.
    print("\nBacking up existing files...")
    backup_existing_files()

    # Install DOA files.
    print("\nInstalling Superhot files...")
    try:
        install_superhot_files(resource_path)
        print("Files successfully installed.")
    except RuntimeError:
        input("Aborting installation. Press any key to quit.\n")
        return

    # Final message.
    print("\n\n"
          "*************************\n"
          "* INSTALLATION COMPLETE *\n"
          "*************************\n\n")
    time.sleep(1)
    print("To uninstall Dark Souls: Superhot, simply copy all the contents\n"
          "of the 'pre-superhot-backup' folder into the main data directory,\n"
          "overwriting any folders and files encountered (including the\n"
          "executable).\n\n"
          ""
          ""
          "IMPORTANT:\n\n"
          "  - GO OFFLINE IN STEAM. Unlike the old version of Dark Souls, the\n"
          "    cheat protection in Dark Souls: Remastered is NOT mod-friendly.\n"
          "    This isn't a large mod, but it's never worth the risk. I take no\n"
          "    responsibility whatsoever for anything that happens to your Steam\n"
          "    account.\n\n"
          ""
          "  - This mod is not compatible with other mods that change any of the\n"
          "    same files (which will be most of them, e.g. Daughters of Ash or Item\n"
          "    Randomizer). However, you don't need to make a new save or anything -\n"
          "    you can freely uninstall and/or reinstall the mod during a single\n"
          "    playthrough of the game with the same character.\n\n"
          ""
          "  - Dark Souls: Superhot was originally created for LobosJr to play during\n"
          "    his St Jude charity fundraiser in May 2019. St Jude is a children's\n"
          "    research hospital that does incredible work for children all over the\n"
          "    United States.\n\n"
          ""
          "    If you love the mod, consider donating to St Jude. I can tell you\n"
          "    from first-hand experience that every dollar counts for these kids and\n"
          "    their wonderful carers and doctors.\n\n"
          ""
          "       https://www.stjude.org/donate/donate-to-st-jude.html\n\n")

    time.sleep(2)
    input("\nPress Enter to exit, and enjoy Dark Souls: SUPER. HOT. SUPER. HOT.\n")
    return


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy(s, d)


def backup_existing_files():

    if not os.path.isfile('DarkSoulsRemastered.exe'):
        raise RuntimeError("This does not appear to be the 'DARK SOULS REMASTERED' data folder.")

    if os.path.isdir('pre-superhot-backup'):
        if input("\nWARNING: A backup folder of your pre-Superhot files\n"
                 "already exists. Any existing backups will be overridden with\n"
                 "new backups if you continue. Do you still want to back up?\n"
                 "[y/n]: ").lower() != 'y':
            print("\nSkipping backup. You can always restore your original\n"
                  "Dark Souls: Remastered files through a Steam file validation.")
            return
    else:
        os.mkdir('pre-superhot-backup')

    print("\nBacking up now. (This might take a few seconds.)")

    for file_path in SUPERHOT_FILE_LIST:
        if not os.path.isfile(file_path):
            if input(f"\nWARNING: Could not find file {file_path} to back up. This\n"
                     f"is unusual, and you should stop now unless you know that\n"
                     f"you definitely already deleted this critical game file for some\n"
                     f"reason. Continue with backup?\n"
                     f"[y/n]:").lower() != 'y':
                print("\nSkipping backup. In the worst case, you can always restore\n"
                      "your original Dark Souls files through a Steam file\n"
                      "validation.")
                return
        else:
            backup_path = os.path.join('pre-superhot-backup', file_path)
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            shutil.copy2(file_path, backup_path)

    print("Backup complete.")


def install_superhot_files(install_data_dir):

    # Make sure Superhot files are present.
    for file_path in SUPERHOT_FILE_LIST:
        if not os.path.isfile(os.path.join(install_data_dir, file_path)):
            print(f"ERROR: {os.path.join(install_data_dir, file_path)} not found.\n"
                  f"Please ensure the files are present, or re-download this mod\n"
                  f"if you can't fix it (then contact me if needed).")
            raise RuntimeError

    # Copy files. This will overwrite any existing files (and doesn't care if files/folders don't already exist).
    for file_path in SUPERHOT_FILE_LIST:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        shutil.copy(os.path.join(install_data_dir, file_path), file_path)


SUPERHOT_FILE_LIST = [
    'chr/c0000.anibnd.dcx',
    'event/m10_00_00_00.emevd.dcx',
    'event/m10_01_00_00.emevd.dcx',
    'event/m10_02_00_00.emevd.dcx',
    'event/m11_00_00_00.emevd.dcx',
    'event/m12_00_00_00.emevd.dcx',
    'event/m12_01_00_00.emevd.dcx',
    'event/m13_00_00_00.emevd.dcx',
    'event/m13_01_00_00.emevd.dcx',
    'event/m13_02_00_00.emevd.dcx',
    'event/m14_00_00_00.emevd.dcx',
    'event/m14_01_00_00.emevd.dcx',
    'event/m15_00_00_00.emevd.dcx',
    'event/m15_01_00_00.emevd.dcx',
    'event/m16_00_00_00.emevd.dcx',
    'event/m17_00_00_00.emevd.dcx',
    'event/m18_00_00_00.emevd.dcx',
    'event/m18_01_00_00.emevd.dcx',
    'map/MapStudio/m10_00_00_00.msb',
    'map/MapStudio/m10_01_00_00.msb',
    'map/MapStudio/m10_02_00_00.msb',
    'map/MapStudio/m11_00_00_00.msb',
    'map/MapStudio/m12_00_00_01.msb',
    'map/MapStudio/m12_01_00_00.msb',
    'map/MapStudio/m13_00_00_00.msb',
    'map/MapStudio/m13_01_00_00.msb',
    'map/MapStudio/m13_02_00_00.msb',
    'map/MapStudio/m14_00_00_00.msb',
    'map/MapStudio/m14_01_00_00.msb',
    'map/MapStudio/m15_00_00_00.msb',
    'map/MapStudio/m15_01_00_00.msb',
    'map/MapStudio/m16_00_00_00.msb',
    'map/MapStudio/m17_00_00_00.msb',
    'map/MapStudio/m18_00_00_00.msb',
    'map/MapStudio/m18_01_00_00.msb',
    'menu/ENGLISH/menu_local.tpf.dcx',
    'param/GameParam/GameParam.parambnd.dcx',
    'script/m16_00_00_00.luabnd.dcx',
    'sound/frpg_smain.fsb',
]


def main():
    print("\n"
          "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
          "~                                                             ~\n"
          "~           D A R K   S O U L S  :  S U P E R H O T           ~\n"
          "~                           v1.0.0                            ~\n"
          "~                                                             ~\n"
          "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    print("This installer will take you through the steps of installing\n"
          "Dark Souls: Superhot for Dark Souls: Remastered. This simply\n"
          "involves backing up the handful of game files that Superhot\n"
          "will replace, so that you can easily 'uninstall' the mod by\n"
          "copying the original files back into the game directory.\n\n"
          "Start by finding your 'DarkSoulsRemastered.exe' file.\n\n"
          ""
          "If you don't know where it is, it should be somewhere like:\n"
          "    C:/Program Files (x86)/Steam/steamapps/common/DARK SOULS REMASTERED")

    root = Tk()
    root.withdraw()
    ds_exe_file = filedialog.askopenfilename(
        title='Please select your DarkSoulsRemastered.exe file.',
        initialdir='C:/Program Files (x86)/Steam/steamapps/common/DARK SOULS REMASTERED')  # guess
    root.destroy()

    if os.path.basename(ds_exe_file) != 'DarkSoulsRemastered.exe':
        input("\nYou must select your DarkSoulsRemastered.exe. Restart the installer\n"
              "and try again.\n\n"
              "Aborting installation. Press Enter to quit.")
    else:
        resource_path = getattr(sys, '_MEIPASS', os.path.abspath('./data'))
        os.chdir(os.path.dirname(ds_exe_file))
        install_superhot(resource_path)

    print('Exiting...')


if __name__ == '__main__':
    main()
