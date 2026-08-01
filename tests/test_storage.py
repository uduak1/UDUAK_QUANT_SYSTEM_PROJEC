from config.storage import initialize_storage
from config.storage import storage


def test_storage_initialization():
    initialize_storage()

    assert storage.data_dir.exists()
    assert storage.historical_data_dir.exists()
    assert storage.backtests_dir.exists()
    assert storage.database_dir.exists()
    assert storage.logs_dir.exists()
    assert storage.reports_dir.exists()
    assert storage.exports_dir.exists()
    assert storage.cache_dir.exists()
    assert storage.models_dir.exists()


def test_database_file_location():
    assert storage.database_file.name == "uduak_quant.db"
    assert storage.database_file.parent == storage.database_dir