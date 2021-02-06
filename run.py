"""
@Author: Kowaine
@Description: 周期性运行
@Date: 2021-02-06 12:02:05
@LastEditTime: 2021-02-06 12:25:53
"""

import update, sys

INTERVAL =  600

if __name__ == "__main__":
    import time
    sys.stdout.write("".join(["Interval: ", str(INTERVAL), "s\n"]))
    while True:
        try:
            update.run()
            sys.stdout.write("".join([update.get_formatted_time(), " OK\n"]))
        except Exception:
            sys.stderr.write("".join([update.get_formatted_time(), " ERROR\n"]))
        finally:
            try:
                time.sleep(INTERVAL)
            except KeyboardInterrupt:
                sys.stdout.write("".join([update.get_formatted_time(), " STOP\n"]))
                sys.exit(0)
