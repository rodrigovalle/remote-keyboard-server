""" Remote keyboard bluetooth server """

from bluetooth import *


# monkey patch to support context managers
def btsocket_enter(self):
    return self

def btsocket_exit(self, *args):
    self.close()

BluetoothSocket.__enter__ = btsocket_enter
BluetoothSocket.__exit__ = btsocket_exit


with BluetoothSocket(RFCOMM) as server_sock:
    server_sock.bind(("", PORT_ANY))
    server_sock.listen(1)

    host, port = server_sock.getsockname()
    uuid = "1aa3ab40-beb9-4a19-91de-a4cf9438c4df"

    advertise_service(
        server_sock,
        'rodrigos bluetooth service :D',
        service_id=uuid,
        service_classes=[SERIAL_PORT_CLASS],
        profiles=[SERIAL_PORT_PROFILE],
        provider='rodrigo',
        description='a really cool bluetooth service you should totes connect to'
    )

    print("waiting for connection on RFCOMM channel {}".format(port))

    client_sock, client_info = server_sock.accept()
    with client_sock:
        client_sock.send("HELLO")
        print("accepted connection from ", client_info)
