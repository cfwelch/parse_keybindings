

import subprocess
import sys
import os


def main():
    spath = raw_input("Input path to Stanford Core NLP: ")
    ipath = raw_input("Install location: ")
    ipath = ipath if ipath.endswith("/") else ipath + "/"
    spath = spath if spath.endswith("/") else spath + "/"
    os.system("unzip parse_visualize.zip -d " + ipath)
    os.system("echo " + spath + " > " + ipath + "parse_visualize/config")
    ipath = ipath + "parse_visualize/"
    install_command("constituency parse", "python " + ipath + "con_to_dot.py " + ipath, "<Control><Shift>exclam")
    install_command("dependency parse", "python " + ipath + "dep_to_dot.py " + ipath, "<Control><Shift>at")

def install_command(name, script, keys):
    # defining keys & strings to be used
    key = "org.gnome.settings-daemon.plugins.media-keys custom-keybindings"
    subkey1 = key.replace(" ", ".")[:-1]+":"
    item_s = "/"+key.replace(" ", "/").replace(".", "/")+"/"
    firstname = "custom"
    # get the current list of custom shortcuts
    get = lambda cmd: subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8")
    z = get("gsettings get " + key).strip()
    current = eval(z) if "@as []" != z else []
    # make sure the additional keybinding mention is no duplicate
    n = 1
    while True:
        new = item_s + firstname + str(n) + "/"
        n_name = get("gsettings get " + subkey1 + new + " name")
        #print(get("gsettings get " + subkey1 + new + " binding"))
        if n_name[1:-2] == name:
            print("Key for '" + name + "' already exists.")
            return
        if new in current:
            n = n + 1
        else:
            break
    # add the new keybinding to the list
    current.append(new)
    # create the shortcut, set the name, command and shortcut key
    cmd0 = 'gsettings set ' + key + ' "'+str(current)+'"'
    cmd1 = 'gsettings set ' + subkey1 + new + " name '" + name + "'"
    cmd2 = 'gsettings set ' + subkey1 + new + " command '" + script + "'"
    cmd3 = 'gsettings set ' + subkey1 + new + " binding '" + keys + "'"

    for cmd in [cmd0, cmd1, cmd2, cmd3]:
        subprocess.call(["/bin/bash", "-c", cmd])
    print("Created key for '" + name + "'.")

if __name__ == "__main__":
    main()
