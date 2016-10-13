import time
import argparse

from cmd2 import Cmd
from huuey import Huuey


huuey = Huuey()


class CommandLine(Cmd):
    def do_show(self, arg, opts):
        pass

    prompt = '=>'

    @staticmethod
    def do_bridges(self, line):
        """Get a list of bridges on the local network"""

        parser = argparse.ArgumentParser(description='Get a list of all bridges on your local network', prog="list")

        args = parser.parse_args(line.split())

        print 'List of Bridges \n'
        print 'ID\tAddress'

        for index, device in enumerate(huuey.bridges):
            print u"{index}\t{device}".format(index=index+1, device=device['internalipaddress'])

    @staticmethod
    def do_pair(self, line):
        """
        Description:
            Pair this shell session to the bridge

        Required Args:
            id: ID of bridge to pair to from command: bridges

        Optional Args:
            -t, --timeout:  Amount of time to wait before stopping the
                            pairing process if button not pressed

            -i, --interval: Amount of seconds to wait before trying to
                            pair with the bridge
        """

        parser = argparse.ArgumentParser(description='Pair this session to a bridge.', prog="pair")

        parser.add_argument('id', help='ID of bridge from list command', type=int)
        parser.add_argument('-t', '--timeout', help='Amount of seconds before bridge stops trying to pair', default=30,
                            type=int)
        parser.add_argument('-i', '--interval', help='Amount of seconds to wait before trying to pair', default=3,
                            type=int)

        args = parser.parse_args(line.split())

        print 'Please press the blue button on the bridge...'
        data = None

        end_time = time.time() + args.timeout

        while True and time.time() < end_time:
            request = huuey.pair(int(args.id) - 1)

            if request:
                if 'error' not in request[0]:
                    data = request[0]
                    break
            print args.interval
            time.sleep(args.interval)

        print data


if __name__ == "__main__":
    CommandLine().cmdloop()