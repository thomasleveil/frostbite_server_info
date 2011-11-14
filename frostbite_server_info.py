import json
import textwrap
import sys
from frostbite_server_info import getinfo

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
        Simple command line tool to query a frostbite server for basic info.
        Result is displayed formatted as json.
        Optionally can verify RCON password correctness.
        '''),
        epilog=textwrap.dedent('''\
        Examples
        --------

        $ frostbite_server_info.py 11.22.33.44 47000 --password=xxxxxxx --timeout=3
        {
            "password_accepted": true,
            "game": "BF3",
            "version": "883971",
            "serverInfo": {
                "targetScore": "100",
                "roundTime": "613627",
                "team4score": null,
                "level": "MP_003",
                "team2score": "0",
                "serverName": "Test server #1",
                "gamemode": "TeamDeathMatch0",
                "numPlayers": "0",
                "maxPlayers": "16",
                "serverUptime": "789299",
                "roundsTotal": "1",
                "hasPunkbuster": "true",
                "numTeams": "2",
                "hasPassword": "false",
                "team1score": "0",
                "team3score": null,
                "onlineState": "",
                "roundsPlayed": "0",
                "isRanked": "true"
            }
        }
        ''')
    )
    parser.add_argument('host', metavar='HOST', type=str, help='RCON IP address or hostname')
    parser.add_argument('port', metavar='PORT', type=int, help='RCON port')
    parser.add_argument('--password', '-p', metavar='PASSWORD', type=str,
                        help='RCON password if you want to check password correctness')
    parser.add_argument('--timeout', metavar='SECONDS', type=int, help='connection timeout')
    parser.add_argument('--debug', action='store_true', help='activate debug output')

    args = parser.parse_args()

    if args.debug:
        import logging
        logging.basicConfig(format='%(asctime)-15s %(name)15s %(levelname)-7s %(message)s')
        logging.getLogger().setLevel(logging.NOTSET)

    try:
        data = json.dumps(getinfo(args.host, args.port, password=args.password, timeout=args.timeout), indent=4)
        print data
        if 'error' in data:
            sys.exit(1)
        else:
            sys.exit(0)
    except Exception, err:
        sys.exit(1)

