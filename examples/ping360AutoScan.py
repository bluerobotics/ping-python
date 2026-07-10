from brping import definitions
from brping import Ping360
import time
import argparse

from builtins import input

## Parse Command line options
############################

parser = argparse.ArgumentParser(description="Ping360 auto scan example")
parser.add_argument('--device', action="store", required=False, type=str, help="Ping device port. E.g: /dev/ttyUSB0")
parser.add_argument('--baudrate', action="store", type=int, default=2000000, help="Ping device baudrate. E.g: 2000000")
parser.add_argument('--udp', action="store", required=False, type=str, help="Ping UDP server. E.g: 192.168.2.2:9092")
args = parser.parse_args()
if args.device is None and args.udp is None:
    parser.print_help()
    exit(1)

# Make a new Ping360
myPing360 = Ping360()
if args.device is not None:
    myPing360.connect_serial(args.device, args.baudrate)
elif args.udp is not None:
    (host, port) = args.udp.split(':')
    myPing360.connect_udp(host, int(port))

if myPing360.initialize() is False:
    print("Failed to initialize Ping!")
    exit(1)

print("------------------------------------")
print("Ping360 auto scan..")
print("Press CTRL+C to exit")
print("------------------------------------")

input("Press Enter to continue...")

try:
    myPing360.control_auto_transmit(
        mode = 1,
        gain_setting = 0,
        transmit_duration = 80,
        sample_period = 80,
        transmit_frequency = 750,
        number_of_samples = 1024,
        start_angle = 0,
        stop_angle = 399,
        num_steps = 1,
        delay = 0
    )

    # Print a compact summary of each received profile.
    for n in range(400):
        message = myPing360.wait_message([definitions.PING360_AUTO_DEVICE_DATA])
        if message is None:
            print("Timed out waiting for a Ping360 profile.")
            break

        angle = message.angle
        # data contains raw return-strength samples ordered nearest-to-farthest.
        data = message.data
        print(
            f"Angle: {angle} gradians, samples: {len(data)}, "
            f"preview: {list(data[:8])}"
        )
        time.sleep(0.001)
except KeyboardInterrupt:
    print("\nScan interrupted.")
finally:
    print("Stopping auto scan and disabling the motor...")
    try:
        if args.device is not None:
            # A serial break stops auto-transmit and starts device autobaud.
            myPing360.iodev.send_break()
            time.sleep(0.001)
            myPing360.iodev.write(b"U")
    finally:
        myPing360.control_motor_off()
