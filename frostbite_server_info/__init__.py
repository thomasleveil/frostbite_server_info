import logging
import socket
from frostbite_server_info.protocol import EncodeClientRequest, receivePacket, DecodePacket, generatePasswordHash, FrostbiteError

logger = logging.getLogger('bf3info')

def decode_frostbite2_server_info(data):
    """
    <serverName: string> <current playercount: integer> <max playercount: integer> <current gamemode: string>
    <current map: string> <roundsPlayed: integer> <roundsTotal: string> <scores: team scores>
    <onlineState: online state> <ranked: boolean> <punkBuster: boolean> <hasGamePassword: boolean>
    <serverUpTime: seconds> <roundTime: seconds>

    ['BigBrotherBot #2', '0', '16', 'ConquestLarge0', 'MP_012', '0', '2', '2', '300', '300', '0', '', 'true', 'true', 'false', '5148', '455']

    """
    numOfTeams = 0
    if data[7] != '':
        numOfTeams = int(data[7])

    response = {
        'serverName': data[0],
        'numPlayers': data[1],
        'maxPlayers': data[2],
        'gamemode': data[3],
        'level': data[4],
        'roundsPlayed': data[5],
        'roundsTotal': data[6],
        'numTeams': data[7],
        # depending on numTeams, there might be between 0 and 4 team scores here
        'team1score': None,
        'team2score': None,
        'team3score': None,
        'team4score': None,
        'targetScore': data[-7],
        'onlineState': data[-6],
        'isRanked': data[-5],
        'hasPunkbuster': data[-4],
        'hasPassword': data[-3],
        'serverUptime': data[-2],
        'roundTime': data[-1],
    }
    if numOfTeams >= 1:
        response['team1score'] = data[8]
    if numOfTeams >= 2:
        response['team2score'] = data[9]
    if numOfTeams >= 3:
        response['team3score'] = data[10]
    if numOfTeams == 4:
        response['team4score'] = data[11]
    return response

def decode_frostbite1_server_info(data):
    """query server info, update self.game and return query results
    Response: OK <serverName: string> <current playercount: integer> <max playercount: integer>
    <current gamemode: string> <current map: string> <roundsPlayed: integer>
    <roundsTotal: string> <scores: team scores> <onlineState: online state>
    """
    return {
        'serverName': data[0],
        'maxPlayers': data[2],
        'gamemode': data[3],
        'level': data[4],
        'roundsPlayed': data[5],
        'roundsTotal': data[6]
    }


def getinfo(host, port, password=None, timeout=None):
    info = {}
    def checkError(words):
        if words[0] != "OK":
            raise FrostbiteError(words[0])
    serverSocket = None
    try:
        socket.setdefaulttimeout(timeout)
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info("Connecting to %s:%s" % (host, port))
        serverSocket.connect( ( host, port ) )
        serverSocket.setblocking(1)
        receiveBuffer = ''
        logger.debug("connected to %s:%s" % (host, port))

        if password:
            # Retrieve this connection's 'salt' (magic value used when encoding password) from server
            request = EncodeClientRequest(["login.hashed"])
            logger.debug("sending %r" % request)
            serverSocket.send(request)
            getPasswordSaltResponse, receiveBuffer = receivePacket(serverSocket, receiveBuffer)
            isResponse, sequence, words = DecodePacket(getPasswordSaltResponse)[1:]
            logger.debug("received %r" % words)
            checkError(words)

            # Given the salt and the password, combine them and compute hash value
            salt = words[1].decode("hex")
            passwordHash = generatePasswordHash(salt, password)
            passwordHashHexString = passwordHash.encode("hex").upper()

            # Send password hash to server
            logger.info('Logging in with password')
            request = EncodeClientRequest(["login.hashed", passwordHashHexString])
            logger.debug("sending %r" % request)
            serverSocket.send(request)
            loginResponse, receiveBuffer = receivePacket(serverSocket, receiveBuffer)
            isResponse, sequence, words = DecodePacket(loginResponse)[1:]
            logger.debug("received %r" % words)
            if words[0] == 'OK':
                info['password_accepted'] = True
            elif words[0] == 'InvalidPasswordHash':
                info['password_accepted'] = False
            else:
                raise FrostbiteError(words[0])

        # requesting version
        request = EncodeClientRequest(("version",))
        logger.debug("sending %r" % request)
        serverSocket.send(request)
        response, receiveBuffer = receivePacket(serverSocket, receiveBuffer)
        isResponse, sequence, words = DecodePacket(response)[1:]
        logger.debug("received %r" % words)
        checkError(words)
        info['game'], info['version'] = words[1:]

        # requesting info
        request = EncodeClientRequest(("serverInfo",))
        logger.debug("sending %r" % request)
        serverSocket.send(request)
        response, receiveBuffer = receivePacket(serverSocket, receiveBuffer)
        isResponse, sequence, words = DecodePacket(response)[1:]
        logger.debug("received %r" % words)
        checkError(words)

        if info['game'] in ('BFBC2', 'MOH'):
            info['serverInfo'] = decode_frostbite1_server_info(words[1:])
        elif info['game'] in ('BF3'):
            info['serverInfo'] = decode_frostbite2_server_info(words[1:])
        else:
            info['serverInfo'] = words[1:]

    except FrostbiteError, err:
        info['error'] = err.message
    except socket.error, err:
        if hasattr(err, 'message'):
            info['error'] = 'Network error: %s' % err.message
        else:
            info['error'] = 'Network error: %s' % repr(err)
    except Exception, err:
        info['error'] = '%s: %s' % (type(err), err.message)
    finally:
        if serverSocket:
            serverSocket.close()
        logger.info('info: %r' % info)
        return info

