import sys


def run_client():
    from curses import wrapper
    import client.main
    wrapper(client.main.main)

def run_server():
    import server.main
    server.main.main()


if "-s" in sys.argv or "--server" in sys.argv:
    run_server()
else:
    run_client()