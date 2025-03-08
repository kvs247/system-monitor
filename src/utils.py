from src.dtypes import MetricUnit


def bytes_to_gib(bytes: float) -> float:
    return bytes / (1024**3)


def get_metric_unit_ylim(unit: MetricUnit) -> float:
    match unit:
        case MetricUnit.PERCENT:
            return 100.0
        case MetricUnit.GIB:
            return 32.0
        case MetricUnit.CELSCIUS:
            return 100.0
