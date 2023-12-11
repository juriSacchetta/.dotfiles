#!/usr/bin/python3

import psutil
import time
from termcolor import colored

def is_qemu_process(process):
    return "qemu-x86_64" in process.name()  # Adjust the name as needed

def get_qemu_processes():
    qemu_processes = []

    for process in psutil.process_iter(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_info']):
        if is_qemu_process(process):
            qemu_processes.append(process.info)

    return qemu_processes

def print_qemu_process_info(qemu_processes, known_process):
    new_pids = {process['pid'] for process in qemu_processes} - known_process
    exited_pids = known_process - {process['pid'] for process in qemu_processes}

    for pid in new_pids:
        process = next((p for p in qemu_processes if p['pid'] == pid), None)
        if process is not None:
            name = process['name']
            username = process['username']
            cpu_percent = process['cpu_percent']
            memory_mb = process['memory_info'].rss / (1024 * 1024)

            status = "New"
            colored_status = colored(status, "green")

            print(f"{pid:6} | {name:11} | {username:12} | {cpu_percent:5.1f}% | {memory_mb:8.2f} MB | {colored_status}")

    for pid in exited_pids:
        process = next((p for p in known_process if p == pid))
        if process is not None:
            name = ""
            username = ""
            cpu_percent = 0
            memory_mb = 0

            status = "Exited"
            colored_status = colored(status, "red")

            print(f"{pid:6} | {name:11} | {username:12} | {cpu_percent:5.1f}% | {memory_mb:8.2f} MB | {colored_status}")

    known_process.update(new_pids)
    known_process.difference_update(exited_pids)

    return known_process


def init_table():
    print("PID    | Name        | User         | CPU %  | Memory (MB) | Status")
    print("-" * 70)

def main():
    known_process = set()
    old_state_empty = False
    init_table()
    while True:
        qemu_processes = get_qemu_processes()
        known_process = print_qemu_process_info(qemu_processes, known_process)
        
        if not qemu_processes and not old_state_empty:
            old_state_empty = True
        if qemu_processes and old_state_empty:
            old_state_empty = False
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
