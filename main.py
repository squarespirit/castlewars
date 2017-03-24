import sys
import socket
import pickle
import myprotocol
import re
from card_dealer import *
from player_turn import *


STARTING_RESOURCES = {
    'B': 2, 'b': 5,
    'S': 2, 'w': 5,
    'M': 2, 'c': 5,
    'C': 30, 'F': 10
}

# Number of cards in each player's hand
HAND_SIZE = 8

# Maximum number of cards that can be discarded at once
MAX_DISCARD = 3


def is_unique(lst: List) -> bool:
    """Return true if the list has unique elements."""
    return len(lst) == len(set(lst))


def grow_resources(player: Player) -> None:
    """
    Grow the resources of a player on their turn. (E.g. grow their bricks
    by the number of builders they have.)
    :param player: Player.
    """
    for worker, out_resource in [['B', 'b'], ['S', 'w'], ['M', 'c']]:
        player.resources[out_resource] += player.resources[worker]


def won(player1: Player, player2: Player) -> Player:
    """
    :param player1: A player.
    :param player2: Another player.
    :return: If either player has won, return that player. Else, return None.
    """
    # Win when your castle is at least this much
    CASTLE_WIN = 100

    if player1.resources['c'] >= CASTLE_WIN or player2.resources['c'] <= 0:
        return player1
    elif player2.resources['c'] >= CASTLE_WIN or player1.resources['c'] <= 0:
        return player2

    return None


class InputException(Exception):
    """Exception for bad user input."""
    pass


def print_castle_stats(you: Player, opponent: Player) -> None:
    """Print resource stats for both players' castles.
    :param you: Player representing you.
    :param opponent: Player representing your opponent.
    """
    boundary = '-------------+' + ' ' * 30 + '+-------------'
    fmt = '{1:>3} {0:8} |' + ' ' * 30 + '| {2:>3} {0:8}'
    resource_order = [['B', 'b'], ['S', 'w'], ['M', 'c'], ['C', 'F']]

    for resource_group in resource_order:
        print(boundary)
        for r in resource_group:
            print(fmt.format(
                resource_long[r], you.resources[r], opponent.resources[r]
            ))
    print(boundary)


def print_hand(player: Player, hand: List[Card]) -> None:
    """Print a hand of cards.
    :param player: Player. For checking whether the cards are playable.
    :param hand: List of cards.
    """
    def ok_if(condition: bool) -> str:
        """Return 'OK' character if the condition is True, '' if False."""
        if condition:
            return 'OK'
        return ''

    fmt = '{:2} {:1}) {:18} {:13} {}'
    print(fmt.format('', '', 'Card', 'Cost', 'Actions'))
    for i, card in enumerate(hand):
        print(fmt.format(
            ok_if(card.can_be_played(player)), i, card.name,
            card.cost_string(), card.action_string().capitalize()
        ))


def send_turn(sock: socket.socket, turn: PlayerTurn) -> None:
    """Send a player turn as a message over a socket."""
    myprotocol.send_message(sock, pickle.dumps(turn))


def recv_turn(sock: socket.socket) ->  PlayerTurn:
    """Receive another player's from a socket."""
    return pickle.loads(myprotocol.recv_message(sock))


def main():
    # Script name is always first argument
    if len(sys.argv) != 3:
        print('Castle Wars!')
        print('A clone of the game by Mads Lundemo https://m0rkeulv.com/')
        print()
        print('{} <ip> <port>'.format(sys.argv[0]))
        print('to connect as a client to someone else.')
        print()
        print('{} -l <port>'.format(sys.argv[0]))
        print('to listen on that port as a server.')
        exit(1)

    # Get ip, port, and listening or not from command line
    is_listen = False
    ip = None
    if sys.argv[1] == '-l':
        is_listen = True
    else:
        ip = sys.argv[1]
    port = int(sys.argv[2])

    # Create socket connection with other peer
    sock = None
    if is_listen:  # TCP server, listen for a connection
        print('Listening on port {}, waiting for connection...'.format(port))
        server_sock = socket.socket()
        # server_sock.bind((socket.gethostname(), port))
        server_sock.bind(('', port))
        server_sock.listen()
        # 'sock' is a *new* socket representing a connection with the client.
        sock, address = server_sock.accept()
        print('Accepted connection with {}:{}'.format(*address))

    else:  # TCP client, connect to the server
        print('Connecting to {}:{}...'.format(ip, port))
        sock = socket.socket()
        sock.connect((ip, port))
        print('Connected!')
    print()

    # Create players
    you = Player(STARTING_RESOURCES)
    opponent = Player(STARTING_RESOURCES)

    # Read cards and deal a hand
    dealer = read_cards('cards.txt')
    your_hand = dealer.deal_list(HAND_SIZE)

    # Listener goes first
    is_your_turn = is_listen

    while won(you, opponent) == None:
        # Print castle stats and your hand
        print_castle_stats(you, opponent)
        print()
        print_hand(you, your_hand)
        print()

        if is_your_turn:
            print('0-{} to play that card; d... (ex. d3, d246) to discard up to {} cards'.format(
                HAND_SIZE - 1, MAX_DISCARD
            ))

            # Get valid input
            result = input('Your turn: ')
            while True:
                try:
                    if result.startswith('d'):  # Discard turn
                        if not re.match('[0-' + str(HAND_SIZE - 1) + ']{1,3}', result[1:]):
                            raise InputException('That doesn\'t make sense.')
                        if not is_unique(result[1:]):
                            raise InputException('Discarded cards must be unique.')
                    else:  # Card turn
                        i = int(result)
                        if not 0 <= i < HAND_SIZE:
                            raise InputException('That\'s out of bounds.')
                        if not your_hand[i].can_be_played(you):
                            raise InputException('You can\'t play that card.')
                    break

                except ValueError:  # Failure to convert something to int
                    result = input('That doesn\'t make sense. ')

                except InputException as e:  # Some other bad input.
                    result = input('{} '.format(str(e)))

            print()

            # Parse input result and do turn
            turn = None
            if result.startswith('d'):  # Discard turn
                # Do the discard, and set turn
                cards_i = list(map(int, result[1:]))
                print('You discarded:')
                for i in cards_i:
                    print('\t{}'.format(your_hand[i]))
                # Set to-be-sent turn information
                turn = DiscardTurn([your_hand[i] for i in cards_i])
                print()

                # Get new cards
                print('You got new cards:')
                for i in cards_i:
                    new_card = dealer.deal()
                    print('\t{}'.format(new_card))
                    your_hand[i] = new_card

            else:  # Card turn
                card_i = int(result)
                # Play the card
                print('Played {}'.format(your_hand[card_i]))
                print()
                your_hand[card_i].play(you, opponent, True)
                # Set to-be-sent turn information
                turn = CardTurn(your_hand[card_i])

                # Get a new card
                new_card = dealer.deal()
                print('Got new card: {}'.format(new_card))
                your_hand[card_i] = new_card

            print()

            # Send turn info to other player
            send_turn(sock, turn)

        else:  # Other player's turn

            # Receive turn
            print('Waiting for opponent\'s move...')
            print()
            turn = recv_turn(sock)

            # Carry out the turn
            if isinstance(turn, CardTurn):
                print('Your opponent played: {}'.format(turn.card))
                turn.card.play(you, opponent, False)
            elif isinstance(turn, DiscardTurn):
                print('Your opponent discarded:')
                for card in turn.cards:
                    print('\t{}'.format(card))
                print()
                print('...and got {} new cards.'.format(len(turn.cards)))
            print()


        # Switch turns
        is_your_turn = not is_your_turn

        # Grow the current player's resources
        # This happens on every turn except the first player's first turn
        if is_your_turn:
            grow_resources(you)
        else:
            grow_resources(opponent)


    if won(you, opponent) == you:
        print('Congratulations, you won!')
    else:
        print('Your opponent won--better luck next time!')
    print()
    input('Press enter to exit. ')

# dealer = read_cards('cards.txt')
# for i in range(10):
#     card = dealer.deal()
#     print('{}) {:18} {:13} {}'.format(i, card.name, card.cost_string(), card.action_string().capitalize()))

main()