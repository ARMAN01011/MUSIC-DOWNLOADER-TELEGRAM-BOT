import os
import subprocess
import sys

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Sᴜᴄᴄᴇssғᴜʟʟʏ Exᴇᴄᴜᴛᴇᴅ → {command}")
    except subprocess.CalledProcessError as e:
        print(f"Eʀʀᴏʀ Exᴇᴄᴜᴛɪɴɢ → '{command}': {e}")
        sys.exit(1)

def main():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nPʟᴇᴀsᴇ Wᴀɪᴛ Dᴏɴ'ᴛ Tᴏᴜᴄʜ Aɴʏ Bᴜᴛᴛᴏn\n\n\n")
    print("\n\nSᴛᴇᴘ 1 → Iɴsᴛᴀʟʟɪɴɢ Lɪʙʀᴀʀɪᴇs Fʀᴏᴍ Rᴇϙᴜɪʀᴇᴍᴇɴᴛs.ᴛxᴛ\n\n\n\n")
    if os.path.exists("requirements.txt"):
        run_command("pip3 install -r requirements.txt")
    else:
        print("\n\nEʀʀᴏʀ → Rᴇϙᴜɪʀᴇᴍᴇɴᴛs.ᴛxᴛ Nᴏᴛ Fᴏᴜɴᴅ")
        sys.exit(1)

    print("\n\nSᴛᴇᴘ 2: Exᴇᴄᴜᴛɪɴɢ ғɪʟᴇ Mᴀɪɴ.ᴘʏ.\n\n")

    print("\n\nSᴛᴇᴘ 4: Rᴜɴɴɪɴɢ ARMAN/ᴍᴀɪɴ.ᴘʏ.\n\n\n======================================\n")
    if os.path.exists("ARMAN/main.py"):
        run_command("python3 ARMAN/main.py")
    else:
        print("\n\nEʀʀᴏʀ: ARMAN/ᴍᴀɪɴ.ᴘʏ Nᴏᴛ Fᴏᴜɴᴅ.")
        sys.exit(1)

if __name__ == "__main__":
    main()