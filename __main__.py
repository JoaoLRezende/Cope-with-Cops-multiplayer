def run_client():
    from curses import wrapper
    import client.main
    wrapper(client.main.main)

run_client()
