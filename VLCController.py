"""
Wrapper for VLC HTTP interface
"""
import xml.etree.ElementTree as ET
from enum import Enum
import requests
import logging


class VLCState(Enum):
    STOPPED = 1
    PAUSED = 2
    PLAYING = 3

class CommunicationFailureException(Exception):
    def __init(self, status_code: int):
        self.status_code = status_code


class VLCStatus:
    __slots__ = ["is_full_screen", "time", "filename", "state"]

    def __init__(self, xml: str):
        parser = ET.XMLParser(encoding="utf-8")
        root = ET.fromstring(xml, parser=parser)
        self.state = VLCState[root.find('state').text.upper()]
        if self.state == VLCState.STOPPED:
            return
        self.time = int(root.find('time').text)
        self.is_full_screen = root.find('fullscreen').text == 'true'
        self.filename = root.find("information").find('category').find('info').text


class VLCController:
    __slots__ = ["address", "password"]
    STATUS_URL = '/requests/status.xml'
    SEEK_COMMAND = 'seek&val='
    PAUSE_COMMAND = 'pl_pause'
    PLAY_COMMAND = 'pl_play'

    def __init__(self, address: str, password: str):
        self.address = address
        self.password = password

    def _do_request(self, url) -> VLCStatus:
        response = requests.get(url, auth=('', self.password))
        response.encoding = response.apparent_encoding
        if response.status_code != 200:
            logging.error(f"Unable to query {url} with error code {response.status_code}")
            raise CommunicationFailureException(response.status_code)
        logging.debug(f"Get status response from VLC: {response.text}")
        return VLCStatus(response.text)

    def get_status(self) -> VLCStatus:
        return self._do_request(f'{self.address}{self.STATUS_URL}')

    def seek(self, time_stamp: int):
        return self._do_request(f'{self.address}{self.STATUS_URL}?command={self.SEEK_COMMAND}{time_stamp}')

    def pause(self):
        return self._do_request(f'{self.address}{self.STATUS_URL}?command={self.PAUSE_COMMAND}')

    def play(self):
        return self._do_request(f'{self.address}{self.STATUS_URL}?command={self.PLAY_COMMAND}')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    controller = VLCController('http://127.0.0.1:8080', '1234')
    status = controller.get_status()
    print(status.time)

