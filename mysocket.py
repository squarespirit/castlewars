import socket
from typing import Tuple


# Links about TCP sockets:
# https://docs.python.org/3/howto/sockets.html
# https://wiki.python.org/moin/TcpCommunication


class MySocket:
    """
    Socket wrapper for socket.socket.

    Communicates with other MySockets using a simple protocal.
    Each message has a fixed-length header with the payload length in big-
    endian, followed by the payload.
    """
    # Length of fixed-length header
    HEADER_LENGTH = 4

    def __init__(self, sock: socket.socket = None):
        """
        Create a new socket wrapper.
        :param sock: socket.socket to wrap. If None, create a new underlying
            socket.
        """
        if sock is None:
            self.sock = socket.socket()
        else:
            self.sock = sock

    def bind(self, ip: str, port: int) -> None:
        """
        Bind to an address.
        :param ip: Ip address
        :param port: Port.
        """
        self.sock.bind((ip, port))

    def listen(self) -> None:
        """
        Enable the socket to act as a server and accept connections.
        """
        self.sock.listen()

    def accept(self) -> Tuple[MySocket, int, str]:
        """
        Accept a connection.
        :return mysock, ip, port.
            mysock: New connection as a MySocket.
        """
        sock, address = self.sock.accept()
        ip, port = address
        return MySocket(sock), ip, port

    def send_message(self, payload: bytes) -> None:
        """
        Send a message.
        :param payload: Payload to send.
        :raises:
            RuntimeError if the connection breaks.
            OverflowError if the message is too long.
        """
        self._send_bytes(len(payload).to_bytes(MySocket.HEADER_LENGTH, 'big'))
        self._send_bytes(payload)

    def _send_bytes(self, bytestr: bytes) -> None:
        """
        Send an entire bytestring.
        :param bytestr: Byte sequence to be sent.
        :raises: RuntimeError if the connection breaks.
        """
        sent = 0
        while sent < len(bytestr):
            send_amount = self.sock.send(bytestr[sent:])
            if send_amount == 0:
                raise RuntimeError('Socket connection broken')
            sent += send_amount

    def recv_message(self) -> bytes:
        """
        Receive a message.
        :return: The payload.
        :raises: RuntimeError if the connection breaks.
        """
        payload_length = int.from_bytes(
            self._recv_bytes(MySocket.HEADER_LENGTH), 'big'
        )
        return self._recv_bytes(payload_length)

    def _recv_bytes(self, length: int) -> bytes:
        """
        Receive a known-length bytestring.
        :param length: Length of bytestring.
        :return: Received bytestring.
        :raises: RuntimeError if the connection breaks.
        """
        data = b''
        while len(data) < length:
            temp = self.sock.recv(length - len(data))
            if temp == '':
                raise RuntimeError("Socket connection broken")
            data += temp
        return data
