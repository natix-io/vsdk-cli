import logging

from vsdkx.core.runner import SimpleRunner

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
    SimpleRunner().run()