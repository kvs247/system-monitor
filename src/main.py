from monitor.cpu_load_monitor import CPULoadMonitor
from monitor.memory_monitor import MemoryMonitor
from monitor.gpu_monitor import GPUMonitor
from src.visualization.plotter import Plotter
from system_monitor import SystemMonitor

if __name__ == "__main__":
    system_monitor = SystemMonitor()
    system_monitor.add_monitor(CPULoadMonitor())
    system_monitor.add_monitor(MemoryMonitor())
    system_monitor.add_monitor(GPUMonitor())
    system_monitor.start()

    plotter = Plotter(system_monitor)

    try:
        plotter.show()
    except KeyboardInterrupt:
        pass
    finally:
        system_monitor.stop()
        plotter.close()
