from djitellopy import tello
from rich import print


def print_battery_drone(my_tello):
    bat = my_tello.get_battery()
    if bat >= 65:
        print(f"[bold green]Battery = {bat}%")
    elif bat >= 25:
        print(f"[bold yellow]Battery = {bat}%")
    else:
        print(f"[bold red]Battery = {bat}%")


def main():
    me = tello.Tello()
    me.connect()
    print_battery_drone(me)


if __name__ == '__main__':
    main()
