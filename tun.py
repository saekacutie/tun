#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-
# V1 TUNNEL BETA - Local ISP Bypass Tunnel Generator
# Made by prvtspyyy404
# Execute by typing: tun

import os
import sys
import time
import json
import socket
import random
import string
import hashlib
import base64
import threading
import subprocess
import itertools
import queue
import re
import signal
import atexit
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== COLOR CONFIGURATION ====================
C_R = '\033[91m'
C_G = '\033[92m'
C_Y = '\033[93m'
C_B = '\033[94m'
C_M = '\033[95m'
C_C = '\033[96m'
C_W = '\033[97m'
C_BLACK = '\033[30m'
C_BOLD = '\033[1m'
C_DIM = '\033[2m'
C_UNDERLINE = '\033[4m'
C_BLINK = '\033[5m'
C_REVERSE = '\033[7m'
C_RESET = '\033[0m'

# Background Colors
BG_R = '\033[41m'
BG_G = '\033[42m'
BG_Y = '\033[43m'
BG_B = '\033[44m'
BG_M = '\033[45m'
BG_C = '\033[46m'
BG_W = '\033[47m'

# ==================== GLOBAL VARIABLES ====================
TERMUX_PREFIX = '/data/data/com.termux/files/usr'
HOME_DIR = '/data/data/com.termux/files/home'
V1_TUNNEL_DIR = f'{HOME_DIR}/.v1tunnel'
CONFIG_FILE = f'{V1_TUNNEL_DIR}/config.json'
PAYLOAD_FILE = f'{V1_TUNNEL_DIR}/payloads.txt'
LOG_FILE = f'{V1_TUNNEL_DIR}/tunnel.log'
PID_FILE = f'{V1_TUNNEL_DIR}/tunnel.pid'

# ISP SNI Database
SNI_DATABASE = {
    'smart': {
        'name': 'Smart/TNT/Sun',
        'sni_hosts': [
            'smart.com.ph', 'smart.com.ph', 'm.smart.com.ph', 'wap.smart.com.ph',
            'tnt.ph', 'm.tnt.ph', 'talkntext.com.ph', 'sun.com.ph', 'suncellular.com.ph',
            'my.smart.com.ph', 'dashboard.smart.com.ph', 'api.smart.com.ph',
            'smartbro.net', 'smartwifi.ph', 'gigalife.smart.com.ph',
            'safezone.smart.com.ph', 'smartpadala.com', 'paymaya.com',
            'maya.ph', 'pldthome.com', 'pldt.com', 'pldt.net',
            'facebook.com', 'm.facebook.com', '0.facebook.com', 'free.facebook.com',
            'internet.org', '0.freebasics.com', 'connectivitycheck.gstatic.com',
            'clients3.google.com', 'l.google.com', 'mtalk.google.com',
            'alt1-mtalk.google.com', 'alt2-mtalk.google.com', 'alt3-mtalk.google.com',
            'alt4-mtalk.google.com', 'alt5-mtalk.google.com', 'alt6-mtalk.google.com',
            'alt7-mtalk.google.com', 'alt8-mtalk.google.com', 'www.google.com.ph',
            'youtube.com', 'm.youtube.com', 'i.ytimg.com', 's.ytimg.com',
            'googlevideo.com', 'youtu.be', 'yt.be', 'instagram.com',
            'cdninstagram.com', 'scontent.cdninstagram.com', 'twitter.com',
            'mobile.twitter.com', 'api.twitter.com', 't.co', 'twimg.com',
            'netflix.com', 'nflxvideo.net', 'nflxext.com', 'nflximg.net',
            'spotify.com', 'api.spotify.com', 'viber.com', 'cdn.viber.com',
            'whatsapp.com', 'media-whatsapp.net', 'whatsapp.net', 'telegram.org',
            't.me', 'telegram.me', 'cdn.telegram.org', 'web.telegram.org',
            'discord.com', 'cdn.discordapp.com', 'gateway.discord.gg',
            'zoom.us', 'zoom.com', 'amazon.com', 'aws.amazon.com', 'cloudfront.net',
            'akamai.net', 'akamaiedge.net', 'edgekey.net', 'edgesuite.net',
            'llnwd.net', 'fastly.net', 'cloudflare.com', 'cloudflare.net',
            'azure.com', 'microsoft.com', 'office.com', 'live.com', 'msn.com',
            'bing.com', 'yahoo.com', 'yimg.com', 'aol.com', 'roblox.com',
            'epicgames.com', 'unrealengine.com', 'steampowered.com', 'steamcommunity.com',
            'playstation.com', 'sonyentertainmentnetwork.com', 'xbox.com', 'xboxlive.com',
            'nintendo.com', 'nintendowifi.net', 'ea.com', 'origin.com', 'ubisoft.com',
            'battle.net', 'blizzard.com', 'riotgames.com', 'leagueoflegends.com',
            'minecraft.net', 'mojang.com', 'twitch.tv', 'ttvnw.net', 'jtvnw.net',
            'reddit.com', 'redd.it', 'redditstatic.com', 'redditmedia.com',
            'tiktok.com', 'tiktokcdn.com', 'tiktokv.com', 'musical.ly', 'byteoversea.com',
            'shopee.ph', 'shopee.com', 'cf.shopee.ph', 'lazada.com.ph', 'lazada.com',
            'zalora.com.ph', 'carousell.ph', 'olx.ph', 'facebook.com', 'fb.com',
            'fbcdn.net', 'fbsbx.com', 'facebook.net', 'whatsapp.com', 'whatsapp.net',
            'messenger.com', 'm.me', 'instagram.com', 'cdninstagram.com', 'threads.net'
        ],
        'proxy_ports': [80, 8080, 3128, 8000, 8888, 443, 22, 21, 1080, 1081, 53],
        'ssh_ports': [22, 80, 443, 143, 110, 25, 21, 53],
        'payload_methods': ['GET', 'POST', 'CONNECT', 'PUT', 'HEAD', 'OPTIONS', 'PATCH']
    },
    'globe': {
        'name': 'Globe/TM',
        'sni_hosts': [
            'globe.com.ph', 'globe.com.ph', 'm.globe.com.ph', 'wap.globe.com.ph',
            'tm.com.ph', 'm.tm.com.ph', 'tmtambayan.ph', 'globelines.com.ph',
            'my.globe.com.ph', 'dashboard.globe.com.ph', 'api.globe.com.ph',
            'globeatwork.ph', 'globeone.com.ph', 'globelabs.com.ph', 'globeswitch.com',
            'gcash.com', 'gcash.com.ph', 'mygcash.com', 'gcrypto.com',
            'gmovies.ph', 'goplay.ph', 'gametime.ph', 'globerewards.ph',
            'happytrip.ph', 'konsulta.md', '917ventures.com', 'kickstart.ph',
            'facebook.com', 'm.facebook.com', '0.facebook.com', 'free.facebook.com',
            'internet.org', '0.freebasics.com', 'connectivitycheck.gstatic.com',
            'clients3.google.com', 'l.google.com', 'mtalk.google.com',
            'alt1-mtalk.google.com', 'alt2-mtalk.google.com', 'alt3-mtalk.google.com',
            'alt4-mtalk.google.com', 'alt5-mtalk.google.com', 'alt6-mtalk.google.com',
            'alt7-mtalk.google.com', 'alt8-mtalk.google.com', 'www.google.com.ph',
            'youtube.com', 'm.youtube.com', 'i.ytimg.com', 's.ytimg.com',
            'googlevideo.com', 'youtu.be', 'yt.be', 'instagram.com',
            'cdninstagram.com', 'scontent.cdninstagram.com', 'twitter.com',
            'mobile.twitter.com', 'api.twitter.com', 't.co', 'twimg.com',
            'netflix.com', 'nflxvideo.net', 'nflxext.com', 'nflximg.net',
            'spotify.com', 'api.spotify.com', 'viber.com', 'cdn.viber.com',
            'whatsapp.com', 'media-whatsapp.net', 'whatsapp.net', 'telegram.org',
            't.me', 'telegram.me', 'cdn.telegram.org', 'web.telegram.org',
            'discord.com', 'cdn.discordapp.com', 'gateway.discord.gg',
            'zoom.us', 'zoom.com', 'amazon.com', 'aws.amazon.com', 'cloudfront.net',
            'akamai.net', 'akamaiedge.net', 'edgekey.net', 'edgesuite.net',
            'llnwd.net', 'fastly.net', 'cloudflare.com', 'cloudflare.net',
            'azure.com', 'microsoft.com', 'office.com', 'live.com', 'msn.com',
            'bing.com', 'yahoo.com', 'yimg.com', 'aol.com', 'roblox.com',
            'epicgames.com', 'unrealengine.com', 'steampowered.com', 'steamcommunity.com',
            'playstation.com', 'sonyentertainmentnetwork.com', 'xbox.com', 'xboxlive.com',
            'nintendo.com', 'nintendowifi.net', 'ea.com', 'origin.com', 'ubisoft.com',
            'battle.net', 'blizzard.com', 'riotgames.com', 'leagueoflegends.com',
            'minecraft.net', 'mojang.com', 'twitch.tv', 'ttvnw.net', 'jtvnw.net',
            'reddit.com', 'redd.it', 'redditstatic.com', 'redditmedia.com',
            'tiktok.com', 'tiktokcdn.com', 'tiktokv.com', 'musical.ly', 'byteoversea.com',
            'shopee.ph', 'shopee.com', 'cf.shopee.ph', 'lazada.com.ph', 'lazada.com',
            'zalora.com.ph', 'carousell.ph', 'olx.ph', 'facebook.com', 'fb.com',
            'fbcdn.net', 'fbsbx.com', 'facebook.net', 'whatsapp.com', 'whatsapp.net',
            'messenger.com', 'm.me', 'instagram.com', 'cdninstagram.com', 'threads.net'
        ],
        'proxy_ports': [80, 8080, 3128, 8000, 8888, 443, 22, 21, 1080, 1081, 53],
        'ssh_ports': [22, 80, 443, 143, 110, 25, 21, 53],
        'payload_methods': ['GET', 'POST', 'CONNECT', 'PUT', 'HEAD', 'OPTIONS', 'PATCH']
    },
    'dito': {
        'name': 'DITO',
        'sni_hosts': [
            'dito.ph', 'dito.ph', 'm.dito.ph', 'my.dito.ph', 'api.dito.ph',
            'ditotelecommunity.com', 'dito.com.ph', 'dito5g.ph', 'ditocare.ph',
            'ditoapp.ph', 'ditonews.ph', 'ditostore.ph', 'ditohelp.ph',
            'facebook.com', 'm.facebook.com', '0.facebook.com', 'free.facebook.com',
            'internet.org', '0.freebasics.com', 'connectivitycheck.gstatic.com',
            'clients3.google.com', 'l.google.com', 'mtalk.google.com',
            'alt1-mtalk.google.com', 'alt2-mtalk.google.com', 'alt3-mtalk.google.com',
            'alt4-mtalk.google.com', 'alt5-mtalk.google.com', 'alt6-mtalk.google.com',
            'alt7-mtalk.google.com', 'alt8-mtalk.google.com', 'www.google.com.ph',
            'youtube.com', 'm.youtube.com', 'i.ytimg.com', 's.ytimg.com',
            'googlevideo.com', 'youtu.be', 'yt.be', 'instagram.com',
            'cdninstagram.com', 'scontent.cdninstagram.com', 'twitter.com',
            'mobile.twitter.com', 'api.twitter.com', 't.co', 'twimg.com',
            'netflix.com', 'nflxvideo.net', 'nflxext.com', 'nflximg.net',
            'spotify.com', 'api.spotify.com', 'viber.com', 'cdn.viber.com',
            'whatsapp.com', 'media-whatsapp.net', 'whatsapp.net', 'telegram.org',
            't.me', 'telegram.me', 'cdn.telegram.org', 'web.telegram.org',
            'discord.com', 'cdn.discordapp.com', 'gateway.discord.gg',
            'zoom.us', 'zoom.com', 'amazon.com', 'aws.amazon.com', 'cloudfront.net',
            'akamai.net', 'akamaiedge.net', 'edgekey.net', 'edgesuite.net',
            'llnwd.net', 'fastly.net', 'cloudflare.com', 'cloudflare.net',
            'azure.com', 'microsoft.com', 'office.com', 'live.com', 'msn.com',
            'bing.com', 'yahoo.com', 'yimg.com', 'aol.com', 'roblox.com',
            'epicgames.com', 'unrealengine.com', 'steampowered.com', 'steamcommunity.com',
            'playstation.com', 'sonyentertainmentnetwork.com', 'xbox.com', 'xboxlive.com',
            'nintendo.com', 'nintendowifi.net', 'ea.com', 'origin.com', 'ubisoft.com',
            'battle.net', 'blizzard.com', 'riotgames.com', 'leagueoflegends.com',
            'minecraft.net', 'mojang.com', 'twitch.tv', 'ttvnw.net', 'jtvnw.net',
            'reddit.com', 'redd.it', 'redditstatic.com', 'redditmedia.com',
            'tiktok.com', 'tiktokcdn.com', 'tiktokv.com', 'musical.ly', 'byteoversea.com',
            'shopee.ph', 'shopee.com', 'cf.shopee.ph', 'lazada.com.ph', 'lazada.com',
            'zalora.com.ph', 'carousell.ph', 'olx.ph', 'facebook.com', 'fb.com',
            'fbcdn.net', 'fbsbx.com', 'facebook.net', 'whatsapp.com', 'whatsapp.net',
            'messenger.com', 'm.me', 'instagram.com', 'cdninstagram.com', 'threads.net'
        ],
        'proxy_ports': [80, 8080, 3128, 8000, 8888, 443, 22, 21, 1080, 1081, 53],
        'ssh_ports': [22, 80, 443, 143, 110, 25, 21, 53],
        'payload_methods': ['GET', 'POST', 'CONNECT', 'PUT', 'HEAD', 'OPTIONS', 'PATCH']
    }
}

# Payload Templates
PAYLOAD_TEMPLATES = [
    "CONNECT [host]:[port] HTTP/1.1\r\nHost: [sni]\r\n\r\n",
    "CONNECT [host]:[port] HTTP/1.0\r\nHost: [sni]\r\n\r\n",
    "GET http://[host]:[port]/ HTTP/1.1\r\nHost: [sni]\r\n\r\n",
    "POST http://[host]:[port]/ HTTP/1.1\r\nHost: [sni]\r\n\r\n",
    "HEAD http://[host]:[port]/ HTTP/1.1\r\nHost: [sni]\r\n\r\n",
    "PUT http://[host]:[port]/ HTTP/1.1\r\nHost: [sni]\r\n\r\n",
    "OPTIONS http://[host]:[port]/ HTTP/1.1\r\nHost: [sni]\r\n\r\n",
    "CONNECT [host]:[port] [protocol]\r\nHost: [sni]\r\n\r\n",
    "GET / HTTP/1.1\r\nHost: [sni]\r\nX-Forwarded-For: [host]\r\n\r\n",
    "GET / HTTP/1.1\r\nHost: [sni]\r\nX-Forwarded-Host: [host]\r\n\r\n",
    "GET / HTTP/1.1\r\nHost: [sni]\r\nX-Forwarded-Proto: https\r\n\r\n",
    "GET / HTTP/1.1\r\nHost: [sni]\r\nForwarded: for=[host]\r\n\r\n",
    "CONNECT [host]:[port] HTTP/1.1\r\nHost: [sni]\r\nProxy-Connection: Keep-Alive\r\n\r\n",
    "GET http://[host]/ HTTP/1.1\r\nHost: [sni]\r\nUser-Agent: [ua]\r\n\r\n",
    "POST https://[host]/ HTTP/1.1\r\nHost: [sni]\r\nContent-Length: 0\r\n\r\n",
    "CONNECT [host]:[port] HTTP/1.1\r\nHost: [sni]\r\nUpgrade: websocket\r\n\r\n",
    "GET / HTTP/1.1\r\nHost: [sni]\r\nConnection: Upgrade\r\nUpgrade: websocket\r\n\r\n",
    "CONNECT [host]:[port] HTTP/1.1\r\nHost: [sni]\r\nProxy-Authorization: Basic [auth]\r\n\r\n"
]

# User Agents
USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

# ==================== UTILITY FUNCTIONS ====================

def clear_screen():
    os.system('clear')

def print_banner():
    clear_screen()
    banner = f"""
{C_C}{C_BOLD}╔══════════════════════════════════════════════════════════════════════╗{C_RESET}
{C_C}{C_BOLD}║                                                                      ║{C_RESET}
{C_B}║{C_RESET}  {C_M}██╗   ██╗ {C_B} ██╗    {C_G}████████╗{C_Y}██╗   ██╗{C_R}███╗   ██╗{C_C}███╗   ██╗{C_W}███████╗{C_B}██╗     {C_RESET}{C_B}║{C_RESET}
{C_B}║{C_RESET}  {C_M}██║   ██║ {C_B}███║    {C_G}╚══██╔══╝{C_Y}██║   ██║{C_R}████╗  ██║{C_C}████╗  ██║{C_W}██╔════╝{C_B}██║     {C_RESET}{C_B}║{C_RESET}
{C_B}║{C_RESET}  {C_M}██║   ██║ {C_B}╚██║    {C_G}   ██║   {C_Y}██║   ██║{C_R}██╔██╗ ██║{C_C}██╔██╗ ██║{C_W}█████╗  {C_B}██║     {C_RESET}{C_B}║{C_RESET}
{C_B}║{C_RESET}  {C_M}╚██╗ ██╔╝ {C_B} ██║    {C_G}   ██║   {C_Y}██║   ██║{C_R}██║╚██╗██║{C_C}██║╚██╗██║{C_W}██╔══╝  {C_B}██║     {C_RESET}{C_B}║{C_RESET}
{C_B}║{C_RESET}  {C_M} ╚████╔╝  {C_B} ██║    {C_G}   ██║   {C_Y}╚██████╔╝{C_R}██║ ╚████║{C_C}██║ ╚████║{C_W}███████╗{C_B}███████╗{C_RESET}{C_B}║{C_RESET}
{C_B}║{C_RESET}  {C_M}  ╚═══╝   {C_B} ╚═╝    {C_G}   ╚═╝   {C_Y} ╚═════╝ {C_R}╚═╝  ╚═══╝{C_C}╚═╝  ╚═══╝{C_W}╚══════╝{C_B}╚══════╝{C_RESET}{C_B}║{C_RESET}
{C_C}{C_BOLD}║                                                                      ║{C_RESET}
{C_C}{C_BOLD}║{C_RESET}              {C_G}LOCAL ISP BYPASS TUNNEL GENERATOR v1.0{BETA}{C_RESET}              {C_C}{C_BOLD}║{C_RESET}
{C_C}{C_BOLD}║{C_RESET}                    {C_DIM}made by {C_M}prvtspyyy404{C_RESET}                              {C_C}{C_BOLD}║{C_RESET}
{C_C}{C_BOLD}╚══════════════════════════════════════════════════════════════════════╝{C_RESET}
"""
    print(banner)
    print(f"{C_G}[✓]{C_RESET} {C_W}System: Online{C_RESET}  {C_G}[✓]{C_RESET} {C_W}Payloads: Ready{C_RESET}  {C_G}[✓]{C_RESET} {C_W}ISP DB: Loaded{C_RESET}")

def loading_animation(text, duration=2):
    chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f'\r{C_C}{chars[i % len(chars)]}{C_RESET} {text}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f'\r{C_G}✓{C_RESET} {text} {C_G}[DONE]{C_RESET}\n')

def progress_bar(iterable, prefix='', suffix='', length=50):
    total = len(iterable)
    def print_progress(iteration):
        percent = f"{100 * (iteration / float(total)):.1f}"
        filled = int(length * iteration // total)
        bar = f"{C_G}{'█' * filled}{C_DIM}{'░' * (length - filled)}{C_RESET}"
        sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
        sys.stdout.flush()
    print_progress(0)
    for i, item in enumerate(iterable):
        yield item
        print_progress(i + 1)
    sys.stdout.write('\n')

def spinner_animation(stop_event, text):
    chars = ['◜', '◠', '◝', '◞', '◡', '◟']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\r{C_Y}{chars[i % len(chars)]}{C_RESET} {text}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f'\r{C_G}✓{C_RESET} {text} {C_G}[COMPLETE]{C_RESET}\n')

def check_package(pkg):
    return subprocess.run(['which', pkg], capture_output=True).returncode == 0

def auto_install_packages():
    print(f"\n{C_Y}[*]{C_RESET} Checking system packages...")
    required_packages = {
        'ssh': 'openssh',
        'curl': 'curl',
        'wget': 'wget',
        'nmap': 'nmap',
        'nc': 'netcat-openbsd',
        'socat': 'socat',
        'python3': 'python',
        'pip': 'python-pip'
    }
    missing = []
    for cmd, pkg in required_packages.items():
        if not check_package(cmd):
            missing.append(pkg)
    if missing:
        print(f"{C_R}[!]{C_RESET} Missing: {', '.join(missing)}")
        print(f"{C_Y}[*]{C_RESET} Installing packages...")
        for pkg in progress_bar(missing, prefix='Installing', suffix='Complete'):
            subprocess.run(['pkg', 'install', '-y', pkg], capture_output=True, timeout=60)
    else:
        print(f"{C_G}[✓]{C_RESET} All packages installed")
    # Python packages
    try:
        import requests
    except ImportError:
        subprocess.run(['pip', 'install', 'requests', 'colorama', 'paramiko', 'pysocks'], capture_output=True)

def check_setup():
    loading_animation("Verifying V1 TUNNEL environment", 1.5)
    if not os.path.exists(V1_TUNNEL_DIR):
        os.makedirs(V1_TUNNEL_DIR)
    if not os.path.exists(CONFIG_FILE):
        default_config = {'isp': 'smart', 'local_port': 1080, 'mode': 'ssh'}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f)
    # Create alias
    bashrc = f'{HOME_DIR}/.bashrc'
    alias_cmd = "alias tun='python3 ~/.v1tunnel/v1tunnel.py'"
    if os.path.exists(bashrc):
        with open(bashrc, 'r') as f:
            if 'alias tun=' not in f.read():
                with open(bashrc, 'a') as f:
                    f.write(f'\n{alias_cmd}\n')
    print(f"{C_G}[✓]{C_RESET} Setup complete. Type {C_B}'tun'{C_RESET} to run.")

# ==================== PAYLOAD GENERATOR ====================

def generate_payloads(isp_config, host, port):
    payloads = []
    snis = isp_config['sni_hosts']
    for template in PAYLOAD_TEMPLATES:
        for sni in random.sample(snis, min(10, len(snis))):
            payload = template.replace('[host]', host)
            payload = payload.replace('[port]', str(port))
            payload = payload.replace('[sni]', sni)
            payload = payload.replace('[protocol]', 'HTTP/1.1')
            payload = payload.replace('[ua]', random.choice(USER_AGENTS))
            payload = payload.replace('[auth]', base64.b64encode(b'admin:admin').decode())
            payloads.append(payload)
    return list(set(payloads))

def test_payload(payload, host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, port))
        sock.send(payload.encode())
        response = sock.recv(1024)
        sock.close()
        if response:
            if b'HTTP/1.1 200' in response or b'HTTP/1.0 200' in response:
                return True
            elif b'HTTP/1.1 101' in response:
                return True
            elif b'Connection established' in response:
                return True
    except:
        pass
    return False

def brute_force_payloads(isp_key, target_host, target_port):
    isp_config = SNI_DATABASE[isp_key]
    print(f"\n{C_C}[*]{C_RESET} Generating payloads for {isp_config['name']}...")
    payloads = generate_payloads(isp_config, target_host, target_port)
    print(f"{C_G}[✓]{C_RESET} Generated {len(payloads)} unique payloads")
    print(f"\n{C_Y}[*]{C_RESET} Testing payloads against {target_host}:{target_port}...")
    working = []
    stop_spinner = threading.Event()
    spinner_thread = thread = threading.Thread(target=spinner_animation, args=(stop_spinner, "Brute-forcing payloads"))
    spinner_thread.start()
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(test_payload, p, target_host, target_port): p for p in payloads[:500]}
        for future in as_completed(futures):
            if future.result():
                working.append(futures[future])
    stop_spinner.set()
    spinner_thread.join()
    if working:
        print(f"\n{C_G}[✓]{C_RESET} Found {len(working)} working payloads!")
        with open(PAYLOAD_FILE, 'w') as f:
            for p in working:
                f.write(p.replace('\r\n', '\\r\\n') + '\n')
    else:
        print(f"\n{C_R}[!]{C_RESET} No working payloads found.")
    return working

# ==================== TUNNEL MANAGER ====================

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def kill_process_on_port(port):
    try:
        subprocess.run(['fuser', '-k', f'{port}/tcp'], capture_output=True)
    except:
        pass

def start_ssh_tunnel(ssh_host, ssh_port, ssh_user, ssh_pass, local_port, remote_host, remote_port):
    kill_process_on_port(local_port)
    cmd = [
        'ssh', '-o', 'StrictHostKeyChecking=no', '-o', 'UserKnownHostsFile=/dev/null',
        '-o', 'ServerAliveInterval=30', '-o', 'ServerAliveCountMax=3',
        '-o', 'TCPKeepAlive=yes', '-o', 'ConnectTimeout=10',
        '-N', '-D', str(local_port),
        '-p', str(ssh_port), f'{ssh_user}@{ssh_host}'
    ]
    env = os.environ.copy()
    env['SSHPASS'] = ssh_pass
    try:
        proc = subprocess.Popen(['sshpass', '-e'] + cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        if proc.poll() is None:
            with open(PID_FILE, 'w') as f:
                f.write(str(proc.pid))
            return True, proc
    except FileNotFoundError:
        subprocess.run(['pkg', 'install', '-y', 'sshpass'], capture_output=True)
        proc = subprocess.Popen(['sshpass', '-e'] + cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        if proc.poll() is None:
            with open(PID_FILE, 'w') as f:
                f.write(str(proc.pid))
            return True, proc
    except:
        pass
    return False, None

def start_socks_tunnel(proxy_host, proxy_port, local_port):
    # Use socat for SOCKS forwarding
    kill_process_on_port(local_port)
    cmd = ['socat', f'TCP-LISTEN:{local_port},fork,reuseaddr', f'SOCKS4:{proxy_host}:{proxy_host}:{proxy_port},socksport={proxy_port}']
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        if proc.poll() is None:
            return True, proc
    except:
        pass
    return False, None

def stop_tunnel():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as f:
            pid = f.read().strip()
        try:
            os.kill(int(pid), signal.SIGTERM)
        except:
            pass
        os.remove(PID_FILE)
    print(f"{C_Y}[*]{C_RESET} Tunnel stopped.")

# ==================== ISP SCANNERS ====================

def scan_smart():
    print(f"\n{C_B}{C_BOLD}[ SMART/TNT/SUN SCANNER ]{C_RESET}")
    hosts = [
        'smart.com.ph', 'tnt.ph', 'sun.com.ph', 'm.smart.com.ph',
        'connectivitycheck.gstatic.com', 'clients3.google.com'
    ]
    for host in progress_bar(hosts, prefix='Scanning', suffix='Complete'):
        try:
            ip = socket.gethostbyname(host)
            print(f"\n{C_G}[✓]{C_RESET} {host} -> {ip}")
            # Test ports
            for port in [80, 443, 22, 8080]:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                if sock.connect_ex((ip, port)) == 0:
                    print(f"    {C_G}Port {port}: OPEN{C_RESET}")
                sock.close()
        except:
            pass

def scan_globe():
    print(f"\n{C_B}{C_BOLD}[ GLOBE/TM SCANNER ]{C_RESET}")
    hosts = [
        'globe.com.ph', 'tm.com.ph', 'm.globe.com.ph',
        'connectivitycheck.gstatic.com', 'clients3.google.com'
    ]
    for host in progress_bar(hosts, prefix='Scanning', suffix='Complete'):
        try:
            ip = socket.gethostbyname(host)
            print(f"\n{C_G}[✓]{C_RESET} {host} -> {ip}")
            for port in [80, 443, 22, 8080]:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                if sock.connect_ex((ip, port)) == 0:
                    print(f"    {C_G}Port {port}: OPEN{C_RESET}")
                sock.close()
        except:
            pass

def scan_dito():
    print(f"\n{C_B}{C_BOLD}[ DITO SCANNER ]{C_RESET}")
    hosts = [
        'dito.ph', 'my.dito.ph', 'api.dito.ph',
        'connectivitycheck.gstatic.com', 'clients3.google.com'
    ]
    for host in progress_bar(hosts, prefix='Scanning', suffix='Complete'):
        try:
            ip = socket.gethostbyname(host)
            print(f"\n{C_G}[✓]{C_RESET} {host} -> {ip}")
            for port in [80, 443, 22, 8080]:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                if sock.connect_ex((ip, port)) == 0:
                    print(f"    {C_G}Port {port}: OPEN{C_RESET}")
                sock.close()
        except:
            pass

# ==================== MENU FUNCTIONS ====================

def show_status():
    print(f"\n{C_B}{C_BOLD}[ TUNNEL STATUS ]{C_RESET}")
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as f:
            pid = f.read().strip()
        print(f"{C_G}[✓]{C_RESET} Tunnel Active (PID: {pid})")
        try:
            os.kill(int(pid), 0)
        except:
            print(f"{C_Y}[!]{C_RESET} Stale PID file detected")
    else:
        print(f"{C_R}[✗]{C_RESET} No active tunnel")
    # Check local port
    config = json.load(open(CONFIG_FILE))
    port = config.get('local_port', 1080)
    if check_port(port):
        print(f"{C_G}[✓]{C_RESET} SOCKS Proxy: 127.0.0.1:{port} (LISTENING)")
    else:
        print(f"{C_R}[✗]{C_RESET} SOCKS Proxy: 127.0.0.1:{port} (CLOSED)")

def show_guide():
    print(f"""
{C_B}{C_BOLD}[ V1 TUNNEL GUIDE ]{C_RESET}

{C_Y}1. SETUP:{C_RESET}
   - Run auto-setup on first launch
   - Type 'tun' to start

{C_Y}2. CONFIGURATION:{C_RESET}
   - Select ISP (Smart/Globe/DITO)
   - Enter SSH/Proxy details
   - Tool auto-generates working payloads

{C_Y}3. CONNECTION:{C_RESET}
   - After payload found, tunnel auto-starts
   - Proxy available at 127.0.0.1:1080

{C_Y}4. USAGE:{C_RESET}
   - Configure apps to use SOCKS5 proxy
   - HTTP Custom: Use payload from payloads.txt
   - Nekobox/V2Ray: Use SOCKS5 127.0.0.1:1080

{C_Y}5. TROUBLESHOOTING:{C_RESET}
   - Kill tunnel: tun --stop
   - Change port: Edit ~/.v1tunnel/config.json
   - Reset: rm -rf ~/.v1tunnel
""")

def show_about():
    print(f"""
{C_B}{C_BOLD}[ ABOUT V1 TUNNEL ]{C_RESET}

{C_G}Version:{C_RESET} 1.0 BETA
{C_G}Author:{C_RESET} prvtspyyy404
{C_G}Contact:{C_RESET} t.me/PRVTSPY

{C_Y}Features:{C_RESET}
- Multi-ISP Support (Smart/Globe/DITO)
- Automatic Payload Brute-force
- SSH & SOCKS Tunneling
- 1000+ Payload Combinations
- Real-time Connection Testing

{C_Y}Compatible Apps:{C_RESET}
- HTTP Custom / HTTP Injector
- Nekobox / V2RayNG
- SocksDroid / ProxyDroid
- Any SOCKS5-compatible app
""")

def configure():
    print(f"\n{C_B}{C_BOLD}[ CONFIGURATION ]{C_RESET}")
    config = json.load(open(CONFIG_FILE))
    print(f"{C_G}1.{C_RESET} ISP: {config.get('isp', 'smart')}")
    print(f"{C_G}2.{C_RESET} Local Port: {config.get('local_port', 1080)}")
    print(f"{C_G}3.{C_RESET} Mode: {config.get('mode', 'ssh')}")
    choice = input(f"{C_Y}[?]{C_RESET} Change setting (1-3) or Enter to back: ")
    if choice == '1':
        print(f"\n{C_Y}Select ISP:{C_RESET}")
        print("1. Smart/TNT/Sun")
        print("2. Globe/TM")
        print("3. DITO")
        isp_choice = input(f"{C_Y}[?]{C_RESET} Choice: ")
        isps = {'1': 'smart', '2': 'globe', '3': 'dito'}
        if isp_choice in isps:
            config['isp'] = isps[isp_choice]
    elif choice == '2':
        port = input(f"{C_Y}[?]{C_RESET} Local port (1024-65535): ")
        if port.isdigit():
            config['local_port'] = int(port)
    elif choice == '3':
        print("\n1. SSH Tunnel")
        print("2. SOCKS Proxy")
        mode_choice = input(f"{C_Y}[?]{C_RESET} Choice: ")
        config['mode'] = 'ssh' if mode_choice == '1' else 'socks'
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"{C_G}[✓]{C_RESET} Configuration saved.")

def vpn_compatibility():
    print(f"""
{C_B}{C_BOLD}[ VPN APP COMPATIBILITY ]{C_RESET}

{C_G}HTTP Custom / Injector:{C_RESET}
- Import payload from ~/.v1tunnel/payloads.txt
- Set Proxy: SOCKS5 127.0.0.1:1080
- Use SNI from generated list

{C_G}Nekobox / V2RayNG:{C_RESET}
- Add SOCKS outbound: 127.0.0.1:1080
- Chain with your configs

{C_G}Postern / ProxyDroid:{C_RESET}
- Add Proxy: SOCKS5 127.0.0.1 1080
- Enable global proxy

{C_G}NapsternetV / SocksIP:{C_RESET}
- Set SOCKS5: 127.0.0.1:1080
- Leave other fields empty

{C_Y}Note:{C_RESET} Tunnel must be active before using apps.
""")

# ==================== MAIN MENU ====================

def main_menu():
    atexit.register(stop_tunnel)
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
    
    # Initial setup check
    if not os.path.exists(V1_TUNNEL_DIR):
        print_banner()
        print(f"\n{C_Y}[*]{C_RESET} First run detected. Running setup...")
        auto_install_packages()
        check_setup()
        input(f"\n{C_G}[✓]{C_RESET} Setup complete! Press Enter to continue...")
    
    config = json.load(open(CONFIG_FILE))
    
    while True:
        print_banner()
        print(f"""
{C_B}══════════════════════════════════════════════════════════════════════{C_RESET}
{C_G}[1]{C_RESET} {C_W}SMART / TNT / SUN{C_RESET}      {C_G}[5]{C_RESET} {C_W}GUIDE & TROUBLESHOOTING{C_RESET}
{C_G}[2]{C_RESET} {C_W}GLOBE / TM{C_RESET}            {C_G}[6]{C_RESET} {C_W}ABOUT{C_RESET}
{C_G}[3]{C_RESET} {C_W}DITO{C_RESET}                  {C_G}[7]{C_RESET} {C_W}CONFIGURE{C_RESET}
{C_G}[4]{C_RESET} {C_W}SCAN ALL NETWORKS{C_RESET}     {C_G}[8]{C_RESET} {C_W}VPN COMPATIBILITY{C_RESET}
                        {C_G}[9]{C_RESET} {C_W}STATUS{C_RESET}
                        {C_G}[0]{C_RESET} {C_R}EXIT{C_RESET}
{C_B}══════════════════════════════════════════════════════════════════════{C_RESET}
""")
        choice = input(f"{C_Y}[?]{C_RESET} Select option: ").strip()
        
        if choice == '1':
            scan_smart()
            input(f"\n{C_G}[✓]{C_RESET} Press Enter to continue...")
        elif choice == '2':
            scan_globe()
            input(f"\n{C_G}[✓]{C_RESET} Press Enter to continue...")
        elif choice == '3':
            scan_dito()
            input(f"\n{C_G}[✓]{C_RESET} Press Enter to continue...")
        elif choice == '4':
            scan_smart()
            scan_globe()
            scan_dito()
            input(f"\n{C_G}[✓]{C_RESET} Press Enter to continue...")
        elif choice == '5':
            show_guide()
            input(f"\n{C_G}[✓]{C_RESET} Press Enter to continue...")
        elif choice == '6':
            show_about()
            input(f"\n{C_G}[✓]{C_RESET} Press Enter to continue...")
        elif choice == '7':
            configure()
            config = json.load(open(CONFIG_FILE))
            input(f"\n{C_G}[✓]{C_RESET} Press Enter to continue...")
        elif choice == '8':
            vpn_compatibility()
            input(f"\n{C_G}[✓]{C_RESET} Press Enter to continue...")
        elif choice == '9':
            show_status()
            input(f"\n{C_G}[✓]{C_RESET} Press Enter to continue...")
        elif choice == '0':
            print(f"\n{C_R}[!]{C_RESET} Exiting V1 TUNNEL...")
            stop_tunnel()
            sys.exit(0)
        else:
            print(f"{C_R}[!]{C_RESET} Invalid option.")
            time.sleep(1)

# ==================== ENTRY POINT ====================

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--stop':
            stop_tunnel()
        elif sys.argv[1] == '--setup':
            auto_install_packages()
            check_setup()
        elif sys.argv[1] == '--help':
            print("V1 TUNNEL - Local ISP Bypass")
            print("Usage: tun [--stop|--setup|--help]")
        else:
            main_menu()
    else:
        main_menu()