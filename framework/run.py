from framework import build
from framework import load_dlc
from framework import load_src
import framework.library as library
import signal
import sys
import threading
from framework import check



def run():

    # 加载 扩展插件 并 执行服务发现
    load_dlc.run()
    load_src.run()


    # 构建 服务
    build.build()

    thread = None
    if library.loop_method is not None:
        thread = threading.Thread(target=library.loop_method)
        thread.start()

    def handle_exit(signum, frame):
        print("Exiting...")
        global thread
        if thread is not None:
            thread.join()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)

