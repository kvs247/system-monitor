import time

from SystemMonitor import SystemMonitor

if __name__ == "__main__":
    system_monitor = SystemMonitor()
    system_monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        system_monitor.stop()
