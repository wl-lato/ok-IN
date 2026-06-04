if __name__ == '__main__':
    from src.config import config
    from ok import OK

    debug_config = dict(config)
    debug_config['debug'] = True
    ok = OK(debug_config)
    ok.start()
