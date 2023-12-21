import logging

import server

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print("Starting gRPC server...")
    logger.info("hoge hoge")
    server.serve()
