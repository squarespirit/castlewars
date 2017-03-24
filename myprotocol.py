"""
Socket communication using a simple protocol.
Each message has a fixed-length header with the payload length in big-
endian, followed by the payload.
"""

import socket

# Links about TCP sockets:
# https://docs.python.org/3/howto/sockets.html
# https://wiki.python.org/moin/TcpCommunication

# Length of fixed-length header
HEADER_LENGTH = 4


def send_message(sock: socket.socket, payload: bytes) -> None:
    """
    Send a message.
    :param sock: Socket.
    :param payload: Payload to send.
    :raises:
        RuntimeError if the connection breaks.
        OverflowError if the message is too long.
    """
    _send_bytes(sock, len(payload).to_bytes(HEADER_LENGTH, 'big'))
    _send_bytes(sock, payload)


def _send_bytes(sock: socket.socket, bytestr: bytes) -> None:
    """
    Send an entire bytestring.
    :param sock: Socket.
    :param bytestr: Byte sequence to be sent.
    :raises: RuntimeError if the connection breaks.
    """
    sent = 0
    while sent < len(bytestr):
        send_amount = sock.send(bytestr[sent:])
        if send_amount == 0:
            raise RuntimeError('Socket connection broken')
        sent += send_amount


def recv_message(sock: socket.socket) -> bytes:
    """
    Receive a message.
    :param sock: Socket.
    :return: The payload.
    :raises: RuntimeError if the connection breaks.
    """
    payload_length = int.from_bytes(
        _recv_bytes(sock, HEADER_LENGTH), 'big'
    )
    return _recv_bytes(sock, payload_length)


def _recv_bytes(sock: socket.socket, length: int) -> bytes:
    """
    Receive a known-length bytestring.
    :param sock: Socket.
    :param length: Length of bytestring.
    :return: Received bytestring.
    :raises: RuntimeError if the connection breaks.
    """
    data = b''
    while len(data) < length:
        temp = sock.recv(length - len(data))
        if temp == '':
            raise RuntimeError("Socket connection broken")
        data += temp
    return data
