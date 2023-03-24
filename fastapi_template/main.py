import logging.config

import uvicorn
from app.configs.settings import BASE_DIR
from app.configs.settings import ProjectSettings

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    uvicorn.run(
        "app.app:app",
        host=ProjectSettings.host,
        port=int(ProjectSettings.port),
        reload=True,
        # log_config=logging.config.fileConfig(
        #     f'{BASE_DIR}/fastapi_template/app/configs/logging.conf',
        #     disable_existing_loggers=False
        # )
    )
