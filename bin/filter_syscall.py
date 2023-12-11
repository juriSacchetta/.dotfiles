#!/usr/bin/python3

import subprocess
import sys
import re
from termcolor import colored
import argparse

def run_qemu_with_strace(program, only_not_hooked=False, qemu_classic=False, fioraldi=False, filter=None):
    # Define an array of syscalls
    syscalls_hooked = [
        # file
        "read",
        "write",
        "pread64",
        "pwrite64",
        "connect",
        "poll",
        "recvfrom",
        "sendto",
        "readv",
        "writev",


        # thread
        "gettid",
        "set_tid_address",
        "fork",
        "clone",
        "futex",
        "nanosleep",
        "clock_nanosleep",
        "exit",
        # Add more syscalls here
    ]

    syscall_to_ignore = [
        "mmap",
        "mprotect",
        "brk",
        "arch_prctl",  # Check if this is needed
        "access",
        "openat",
        "newfstatat",
        "get_robust_list",
        "set_robust_list",
        "close",
        "munmap",
        "clock_gettime",
        "clock_gettime64",
        "dup",
        "getrandom",
        "madvise",
        "time",
        "gettimeofday",
        "rt_sigprocmask",
        "rt_sigaction",
        "sysinfo",
        "socket",
        ]
    
    if qemu_classic:
        qemu_command = f"~/DeSaCloud/Thesis/qemu_8/build/qemu-x86_64 -strace {program}"
    elif fioraldi:
        qemu_command = f"~/DeSaCloud/Thesis/build/qemu-x86_64 -d strace {program}"
    else:
        qemu_command = f"~/DeSaCloud/Thesis/qemu-fibers/build/qemu-x86_64 -d strace {program}"
    print(f"Starting: {qemu_command}")
    
    re_hooked_syscall = f"({'|'.join([re.escape(s) for s in syscalls_hooked])})(\\()"
    re_ignore_syscall = f"({'|'.join([re.escape(s) for s in syscall_to_ignore])})(\\()"

    # Start qemu with the specified program and capture its output (stdout and stderr) separately
    qemu_process = subprocess.Popen(qemu_command, shell=True, stderr=subprocess.PIPE, text=True)

    count = 0 
    while True:
        line = qemu_process.stderr.readline().strip().replace("\n", "")
        if not line:
            continue
        count += 1
        ignore_syscall = re.search(re_ignore_syscall, line)
        hooked_syscall = re.search(re_hooked_syscall, line)
        matched_fiber_log = re.search(r"fiber:", line)
        
        if only_not_hooked and (ignore_syscall or hooked_syscall or matched_fiber_log):
            continue

        matched_filter = False
        if filter:
            for f in filter:
                if f and re.search(f, line):
                    matched_filter = True
                    break
        
        if filter and not matched_filter:
            continue

        if ignore_syscall:
            print(colored(f"stderr {count}: {line}", color="blue"))
        elif hooked_syscall:
            print(colored(f"stderr {count}: {line}", "green"))
        elif matched_fiber_log:
            print(colored(line, "yellow"))
        else:
            print(colored(f"stderr {count}: {line}", "red"))
        
        if qemu_process.poll() is not None:
            exit()
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run a program with QEMU and monitor system calls.")
    parser.add_argument("program", help="The program to run with QEMU")
    parser.add_argument("-nh", "--only-not-hooked", action="store_true", help="Only display syscalls not hooked")
    parser.add_argument("-c", "--qemu-classic", action="store_true", help="Use a classic QEMU build")
    parser.add_argument("-fq", "--fioraldi", action="store_true", help="Use Fioraldi's prototype")
    parser.add_argument("-f", "--filter", nargs='+', help="Filter out syscalls by name")
    
    args = parser.parse_args()
    
    try:
        run_qemu_with_strace(args.program, args.only_not_hooked, args.qemu_classic, args.fioraldi, args.filter)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
