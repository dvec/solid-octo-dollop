import logging

from controller import Controller

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Controller.run()
