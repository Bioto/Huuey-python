import time
import argparse
from random import randint

from cmd2 import Cmd
from hue import Schedule


class CommandLine(Cmd):
    prompt = '=>'
    huuey = None

    def do_show(self, arg, opts):
        pass

    def do_bridges(self, line):
        """Get a list of bridges on the local network"""
        print('List of Bridges \n')
        print('ID\tAddress')

        for index, device in enumerate(self.huuey.bridges):
            print u"{index}\t{device}".format(index=index+1, device=device['internalipaddress'])

    def do_lights(self, line):
        """ Get a list of all of the active lights """
        if not self.huuey.issetup():
            print 'This session is not paired! Pair to a bridge first before continuing'
            return

        if len(self.huuey.lights) > 0:
            print 'List of Lights \n'
            print 'ID\tUnique'

            for index, light in enumerate(self.huuey.lights):
                print u"{index}\t{unique}".format(index=index+1, unique=self.huuey.lights[light].uniqueid)

        else:
            if self.huuey.issetup():
                print 'No lights found on bridge'
            else:
                print 'Session not connected to bridge!'

    def do_groups(self, line):
        """ Get a list of all of the active groups """
        if not self.huuey.issetup():
            print 'This session is not paired! Pair to a bridge first before continuing'
            return

        if len(self.huuey.groups) > 0:
            print 'List of Groups \n'
            print 'ID\tName'

            for index, group in enumerate(self.huuey.groups):
                print u"{index}\t{name}".format(index=index+1, name=self.huuey.groups[group].name)

        else:
            if self.huuey.issetup():
                print 'No groups found on bridge'
            else:
                print 'Session not connected to bridge!'

    def do_schedules(self, line):
        if not self.huuey.issetup():
            print 'This session is not paired! Pair to a bridge first before continuing'
            return

        if len(self.huuey.schedules) > 0:
            print 'List of Schedules \n'
            print 'ID\tLocal Time\t\tName'

            for index, schedule in enumerate(self.huuey.schedules):
                print u"{index}\t{localtime}\t\t{name}".format(index=index, name=self.huuey.schedules[schedule].name, localtime=self.huuey.schedules[schedule].localtime)

        else:
            if self.huuey.issetup():
                print 'No groups found on bridge'
            else:
                print 'Session not connected to bridge!'

    def do_scenes(self, line):
        """Get a list of scenes on the local network"""

        print 'List of Scenes \n'
        print 'ID\tName'

        for index, scene in enumerate(self.huuey.scenes):
            print u"{index}\t{unique}".format(index=index+1, unique=scene)

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

    def do_call(self, line):
        if not self.huuey.issetup():
            print 'This session is not paired! Pair to a bridge first before continuing'
            return

        parser = argparse.ArgumentParser(description='Set light or group(s) state', prog="set")

        parser.add_argument('type', choices=['scene'], help="Targets types")
        parser.add_argument('id', help='ID from command scenes}', type=int)

        args = parser.parse_args(line.split())

        if args.type == "scene":
            self.huuey.scenes[args.id].activate()

    def do_create(self, line):
        if not self.huuey.issetup():
            print 'This session is not paired! Pair to a bridge first before continuing'
            return

        parser = argparse.ArgumentParser(description='', prog="set")

        parser.add_argument('type', choices=['scene', 'group'], help="Target types")
        parser.add_argument('name', help='New Scene name}', type=str)
        parser.add_argument('lights', help='ID\'s of lights (ex.. 1,2,3)', type=str)

        # Scene Arguments
        parser.add_argument('--recycle', type=bool, help="Recycle lights?", default=False)

        args = parser.parse_args(line.split())

        if args.type == "scene":
            self.huuey.create_scene(name=args.name, lights=args.lights.split(','), recycle=args.recycle)
        elif args.type == "group":
            self.huuey.create_group(name=args.name, lights=args.lights.split(','))

    def do_set(self, line):
        """
        Description:
            Set light or groups state

        Args:
            type: Specifies light or group for updating
            id: Target for changes
        """
        if not self.huuey.issetup():
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
            if args.id in self.huuey.lights:
                if args.delete:
                    self.huuey.lights[args.id].delete()
                else:
                    self.huuey.lights[args.id].setstate(state).update()
            else:
                print 'Light: {light} not found'.format(light=args.id)

        if args.type == 'group':
            if args.id in self.huuey.groups:
                if args.delete:
                    self.huuey.groups[args.id].delete()
                else:
                    self.huuey.groups[args.id].setstate(state).update()
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
            request = self.huuey.pair(int(args.id) - 1)

            if request:
                if 'success' in request[0]:
                    data = request[0]['success']
                    break

            time.sleep(args.interval)

        if data is not None:
            self.huuey.set_auth(int(args.id) - 1, data['username'])

            print 'Bridge paired!'

    def do_listauth(self, line):
        """
        Description:
            Basic command to list authentication values
        """
        if not self.huuey.issetup():
            print 'This session is not paired! Pair to a bridge first before continuing'
            return
        print u"Token: {token}, Address: {address}".format(token=self.huuey.token, address=self.huuey.address)

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

    def do_test_group_removing_adding_lights(self, line):
        """
        Description:
            1. Removes the first light from the group object then updates the group on the bridge
            2. Adds the first light back to the group object then updates the group on the bridge
        """
        self.huuey.groups['1'].remove_light(1)
        self.huuey.groups['1'].object_update()

        print self.huuey.groups['1'].update()

        self.huuey.groups['1'].add_light(1)
        self.huuey.groups['1'].object_update()

        print self.huuey.groups['1'].update()
