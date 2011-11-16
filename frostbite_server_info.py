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
        examples:
          frostbite_server_info.py 11.22.33.44 47000 --password=xxxxxxx --timeout=3
          frostbite_server_info.py 11.22.33.44 47000
          frostbite_server_info.py 11.22.33.44 47000 --format=xml
        ''')
    )
    parser.add_argument('host', metavar='HOST', type=str, help='RCON IP address or hostname')
    parser.add_argument('port', metavar='PORT', type=int, help='RCON port')
    parser.add_argument('--password', '-p', metavar='PASSWORD', type=str,
                        help='RCON password if you want to check password correctness')
    parser.add_argument('--format', metavar='FORMAT', type=str, choices=('json', 'xml', 'ini'), default='json', help='output format (json, xml, ini)')
    parser.add_argument('--timeout', metavar='SECONDS', type=int, help='connection timeout')
    parser.add_argument('--debug', action='store_true', help='activate debug output')

    args = parser.parse_args()

    if args.debug:
        import logging
        logging.basicConfig(format='%(asctime)-15s %(name)15s %(levelname)-7s %(message)s')
        logging.getLogger().setLevel(logging.NOTSET)

    try:
        data = getinfo(args.host, args.port, password=args.password, timeout=args.timeout)
        if args.format == 'json':
            print json.dumps(data, indent=4)
        elif args.format == 'xml':
            from frostbite_server_info.structured import dict2xml
            print dict2xml(data, pretty=True)
        elif args.format == 'ini':
            import ConfigParser, collections
            conf = ConfigParser.RawConfigParser()
            conf.add_section("general")
            for s in data:
                if hasattr(data[s], 'items'):
                    conf.add_section(s)
                    for k, v in data[s].items():
                        conf.set(s, k, v)
                else:
                    conf.set("general", s, data[s])
            from sys import stdout
            conf.write(stdout)
        else:
            raise ValueError("unsupported output format : %s" % args.format)

        if 'error' in data:
            sys.exit(1)
        else:
            sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(1)

