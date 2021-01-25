#!/usr/bin/env python3

import os
import shutil
import sys
import socket
import psutil

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
    """Devuelve True si la particion root esta llena, Falso en caso contrario"""
    return check_disk_full(disk ="/", min_gb = 2, min_percent = 10)

def check_cpu_constrained():
    """Devuelve True si la CPU esta a tope, Falso en caso contrario"""
    return psutil.cpu_percent(1) > 75

def check_no_network():
    """Devuelve True si no resuelve la pagina de google, Falso en caso contrario"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True

def main():
    checks = [
        (check_reboot, "Pending reboot"),
        (check_root_full, "Root partition full"),
	(check_cpu_constrained, "CPU load too high."),
        (check_no_network, "No working network."),
    ]
    todo_ok = True
    for check, msg in checks:
        if check():
            print (msg)
            todo_ok=False

    if not todo_ok:
        sys.exit(1)

    print ("Todo ok.")
    sys.exit(0)

main()
