from djitellopy import tello


def main():
    me = tello.Tello()
    me.connect()
    print(f"{me.get_battery()}%")


if __name__ == '__main__':
    main()
