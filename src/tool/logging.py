import logging
import logging.config


def logging_init():
    """设置日志配置 - 仅记录到文件"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("chat.log", encoding="utf-8")
        ]
    )
    # 减少不必要的日志输出
    logging.getLogger().setLevel(logging.WARNING)
    logging.getLogger("src").setLevel(logging.INFO)

