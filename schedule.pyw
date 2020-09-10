#encoding utf-8

#__author__ = Jonas Duarte, duarte.jsystem@gmail.com
#Python3
__author__ = 'Jonas Duarte'


from model import GetInfo, Backend
from datetime import datetime
import time
import requests
import os
import PySimpleGUI as sg


class Schedule():
    def __init__(self):
        self.model = Backend()
        self.tray = sg.SystemTray()
        self.title = 'SESP Started'
        self.body = 'The SESP has been inicied'
        self.tray.notify(self.title, self.body)

    def _fusion_inventory_check(self, computer):
        try:
            print('\n\nChecking new Inventory solicitation...')
            next_fusion_inventory = datetime.strptime(computer['next_fusion_inventory'], '%Y-%m-%d %H:%M')
            if next_fusion_inventory <= datetime.now():
                self.title = 'Fusion iniciado'
                self.body = 'O fusion está realizando um novo inventário de software'
                self.tray.notify(self.title, self.body)
                self.model.force_inventory()
        except Exception as e:
            print(e)


    def _reboot_check(self, computer):
        try:
            print('\n\nChecking for reboot solicitation...')
            next_reboot = datetime.strptime(computer['next_reboot'], '%Y-%m-%d %H:%M')
            if next_reboot <= datetime.now():
                self.model.reboot()
        except Exception as e:
            print(e)


    def _shutdown_check(self, computer):
        try:
            print('\n\nChecking for shutdown solicitation...')
            next_shutdown = datetime.strptime(computer['next_shutdown'], '%Y-%m-%d %H:%M')
            if next_shutdown <= datetime.now():
                self.model.shutdown()
        except Exception as e:
            print(e)


    def start(self):
        try:
            
            while True:
                os.system('cls')
                check_frequency = GetInfo().get_check_frequency_of_schedule()
                
                self.model.get_data.get_computer()
                computer = self.model.get_data.get_sesp_computer()['sesp']['1']

                self._fusion_inventory_check(computer)
                self._reboot_check(computer)
                self._shutdown_check(computer)

                time.sleep(check_frequency)
        except Exception as e:
            if 'Failed to establish a new connection' in str(e):
                self.title = 'Falha ao se conectar à API'
                self.body = 'O SESP não conseguiu se conectar à API, entre em contato com o T.I.'
                self.tray.notify(self.title, self.body, icon=None)
                time.sleep(5)
                self.start()
            else:
                raise e


if __name__ == "__main__":
    try:
        Schedule().start()
    except Exception as e:
        raise e