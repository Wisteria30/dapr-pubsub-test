import logging

import application
import config
import server

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    cfg = config.Config()
    print("Starting gRPC server...")
    logger.info("hoge hoge")
    server.serve()
    print("Starting http server...")
    application.start(cfg.HTTP_PORT, cfg.LOG_LEVEL)
