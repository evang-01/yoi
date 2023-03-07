#!/usr/bin/python3
from sys import argv
import requests
import socket


def main():
    if len(argv) < 2:
        print('\033[31;1mERROR: No arguments\033[0m')
        exit(1)
    host = argv[1]
    addr = socket.gethostbyname(host)
    data = requests.get(url=f'http://ip-api.com/json/{addr}').json()
    for k, v in data.items():
        print(f'{k} : {v}')


if __name__ == '__main__':
    main()
