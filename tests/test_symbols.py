from config.symbols import symbols


def test_forex_symbols():
    assert "EURUSD" in symbols.forex
    assert "GBPUSD" in symbols.forex


def test_metals():
    assert "XAUUSD" in symbols.metals
    assert "XAGUSD" in symbols.metals


def test_energy():
    assert "USOIL" in symbols.energy
    assert "UKOIL" in symbols.energy


def test_indices():
    assert "US30" in symbols.indices


def test_all_symbols():
    total = (
        len(symbols.forex)
        + len(symbols.metals)
        + len(symbols.energy)
        + len(symbols.indices)
        + len(symbols.futures)
        + len(symbols.options)
        + len(symbols.bonds)
    )

    assert len(symbols.all_symbols) == total


def test_no_duplicate_symbols():
    assert len(symbols.all_symbols) == len(set(symbols.all_symbols))