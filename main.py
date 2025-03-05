import time

from system_monitor import SystemMonitor
from monitor.cpu_load_monitor import CPULoadMonitor
from monitor.memory_monitor import MemoryMonitor

if __name__ == "__main__":
    system_monitor = SystemMonitor()
    system_monitor.add_monitor(CPULoadMonitor())
    system_monitor.add_monitor(MemoryMonitor())
    system_monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        system_monitor.stop()
