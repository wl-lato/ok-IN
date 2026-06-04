if __name__ == '__main__':
    from src.config import config
    from ok import OK

    ok = OK(config)
    ok.start()
