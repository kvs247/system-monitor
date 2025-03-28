from src.config import Config
from src.metrics_registry.metrics_registry import MetricsRegistry
from src.monitor.cpu_load_monitor import CPULoadMonitor
from src.monitor.gpu_monitor import GPUMonitor
from src.monitor.memory_monitor import MemoryMonitor
from src.system_monitor import SystemMonitor
from src.visualization.plotter import Plotter

if __name__ == "__main__":
    config_data = Config().read_config_file()
    if config_data:
        MetricsRegistry().update_config(config_data.metrics)

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
