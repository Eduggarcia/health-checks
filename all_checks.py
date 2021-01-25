#!/usr/bin/env python3

import os
import shutil
import sys
import socket

def check_reboot():
    """Devuelve True si el PC tiene un reboot pendiente"""
    return os.path.exists("/run/reboot-required")

def check_disk_full(disk, min_gb, min_percent):
    """Devuelve True si no hay sufiente espacio en disco, False en cualquier otro caso"""
    du = shutil.disk_usage(disk)
    #Calculo del porcentaje de disco libre
    percent_free = 100 * du.free / du.total
    #Calculo de los gigabytes libres
    gigabytes_libres = du.free / 2**30
    if gigabytes_libres < min_gb or percent_free < min_percent:
        return True
    return False


def check_root_full():
    """Devuelve True si la particion root esta llena, Falso en cualquier caso"""
    return check_disk_full(disk ="/", min_gb = 2, min_percent = 10)

def main():
    checks = [
        (check_reboot, "Pending reboot"),
        (check_root_full, "Root partition full"),
    ]
    todo_ok = True
    for check, msg in checks:
        if check():
            print (msg)
            sys.exit(1)

    print ("Todo ok.")
    sys.exit(0)

main()