from tinkoff.invest import Quotation


def Qt(obj: Quotation) -> float:
    return obj.units + obj.nano / 1e9
