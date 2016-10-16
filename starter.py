import time
import argparse
from random import randint

from cmd2 import Cmd
from huuey import Huuey
from hue import Schedule, Command

huuey = Huuey()


class CommandLine(Cmd):
    prompt = '=>'

    def do_show(self, arg, opts):
        pass

    def do_bridges(self, line):
        """Get a list of bridges on the local network"""

        parser = argparse.ArgumentParser(description='Get a list of all bridges on your local network', prog="Bridges")

        args = parser.parse_args(line.split())

        print 'List of Bridges \n'
        print 'ID\tAddress'

        for index, device in enumerate(huuey.bridges):
            print u"{index}\t{device}".format(index=index+1, device=device['internalipaddress'])

    def do_lights(self, args):
        """ Get a list of all of the active lights """
        if not huuey.issetup():
            print 'This session is not paired! Pair to a bridge first before continuing'
            return

        if len(huuey.lights) > 0:
            print 'List of Lights \n'
            print 'ID\tUnique'

            for index, light in enumerate(huuey.lights):
                print u"{index}\t{unique}".format(index=index+1, unique=huuey.lights[light].uniqueid)

        else:
            if huuey.issetup():
                print 'No lights found on bridge'
            else:
                print 'Session not connected to bridge!'

    def do_groups(self, args):
        """ Get a list of all of the active groups """
        if not huuey.issetup():
            print 'This session is not paired! Pair to a bridge first before continuing'
            return

        if len(huuey.groups) > 0:
            print 'List of Groups \n'
            print 'ID\tName'

            for index, group in enumerate(huuey.groups):
                print u"{index}\t{name}".format(index=index+1, name=huuey.groups[group].name)

        else:
            if huuey.issetup():
                print 'No groups found on bridge'
            else:
                print 'Session not connected to bridge!'

    def do_schedules(self, args):
        if not huuey.issetup():
            print 'This session is not paired! Pair to a bridge first before continuing'
            return

        if len(huuey.schedules) > 0:
            print 'List of Schedules \n'
            print 'ID\tLocal Time\t\tName'

            for index, schedule in enumerate(huuey.schedules):
                print u"{index}\t{localtime}\t\t{name}".format(index=index, name=huuey.schedules[schedule].name, localtime=huuey.schedules[schedule].localtime)

        else:
            if huuey.issetup():
                print 'No groups found on bridge'
            else:
                print 'Session not connected to bridge!'

    def build_state(self, args):
        obj = {}

        for key in dir(args):
            if key in ['x', 'y']:
                continue

            manual_ignore = key in ['type', 'id']
            value = getattr(args, key)
            value_none = value is None

            if manual_ignore or key.startswith(('__', '_')) or value_none:
                continue

            if value:
                if key == 'status':
                    if value == 'on':
                        obj['on'] = True
                    else:
                        obj['on'] = False
                else:
                    obj[key] = value

        x = getattr(args, 'x')
        y = getattr(args, 'y')

        if x and y:
            obj['xy'] = [x, y]

        return obj

    def do_set(self, line):
        """
        Description:
            Set light or groups state

        Args:
            type: Specifies light or group for updating
            id: Target for changes
        """
        if not huuey.issetup():
            print 'This session is not paired! Pair to a bridge first before continuing'
            return

        parser = argparse.ArgumentParser(description='Set light or group(s) state', prog="set")

        parser.add_argument('type', choices=['light', 'group'], help="Targets either lights or groups")
        parser.add_argument('id', help='ID of {light, bridge}', type=str)

        parser.add_argument('--status', choices=['on', 'off'], type=str, help="Sets lights on or off")
        parser.add_argument('--bri', type=int, help="Sets brightness of lights")
        parser.add_argument('--hue', type=int, help="Sets hue of lights")
        parser.add_argument('--sat', type=int, help="Set saturation of lights")
        parser.add_argument('--ct', type=int, help="Sets Color temp ( The Mired Color temperature )")
        parser.add_argument('--alert', choices=["none", "select", "lselect"], type=str, help="Sets the alert effect")
        parser.add_argument('--effect', choices=["none", "colorloop"], type=str, help="Dynamic effect of light")
        parser.add_argument('--transitiontime', type=int, help="Sets time between color changes")
        parser.add_argument('--bri_inc', type=int, help="Increments brightness by...")
        parser.add_argument('--hue_inc', type=int, help="Increments hue by...")
        parser.add_argument('--ct_inc', type=int, help="Color Temp brightness by...")
        parser.add_argument('--colormode', choices=['hs', 'ct', 'xy'], type=str, help="Sets color mode")

        parser.add_argument('--x', type=int, help="Sets X in CIE color space (Y is required)")
        parser.add_argument('--y', type=int, help="Sets Y in CIE color space (X is required)")

        parser.add_argument('--rename', type=str, help="Sets lights new name")
        parser.add_argument('--delete', help="Deletes specified light or group (Overrides everything else)")

        args = parser.parse_args(line.split())

        state = self.build_state(args)

        if args.type == 'light':
            if args.id in huuey.lights:
                if args.delete:
                    huuey.lights[args.id].delete()
                else:
                    huuey.lights[args.id].setstate(state).update()
            else:
                print 'Light: {light} not found'.format(light=args.id)

        if args.type == 'group':
            if args.id in huuey.groups:
                if args.delete:
                    huuey.groups[args.id].delete()
                else:
                    huuey.groups[args.id].setstate(state).update()
            else:
                print 'Group: {light} not found'.format(group=args.id)

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
                if 'success' in request[0]:
                    data = request[0]['success']
                    break

            time.sleep(args.interval)

        if data is not None:
            huuey.set_auth(int(args.id) - 1, data['username'])

            print 'Bridge paired!'

    def do_listauth(self, line):
        """
        Description:
            Basic command to list authentication values
        """
        if not huuey.issetup():
            print 'This session is not paired! Pair to a bridge first before continuing'
            return
        print u"Token: {token}, Address: {address}".format(token=huuey.token, address=huuey.address)

    def do_test_schedule_creation(self, line):
        """
        Description:
            Creates new schedule with a random id
            Adds command to schedule which is set to activate every light
        """
        schedule = Schedule(parent=huuey, name='My New Schedule #' + randint(0, 10000), description='My New Description', localtime='W127/T23:00:00', status=True, autodelete=False)
        schedule.create_command(address="/groups/0/action", body={
            'on': True
        }, method="POST")

        schedule.create()

if __name__ == "__main__":
    CommandLine().cmdloop()