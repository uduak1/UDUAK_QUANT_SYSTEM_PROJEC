# Dependency Graph

- **modules** : 177
- **errors** : 0
- **warnings** : 357
- **valid** : True

## Modules

### analysis.balanced_price_range_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.bos_analyzer
- __future__
- analysis.market_structure_analyzer
- core.base_analyzer
- pandas
- typing

### analysis.bos_detector
- __future__
- models.response
- monitoring.logger
- typing

### analysis.breaker_block_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.candle_analyzer
- __future__
- models.response
- monitoring.logger

### analysis.candle_patterns
- dataclasses
- typing

### analysis.choch_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.choch_detector
- __future__
- models.response
- monitoring.logger
- typing

### analysis.cumulative_delta_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.dealing_range_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.delta_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.displacement_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.equilibrium_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.fair_value_gap_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.fvg_analyzer
- __future__
- models.response
- monitoring.logger
- typing

### analysis.fvg_detector
- __future__
- models.response
- monitoring.logger
- typing

### analysis.fvg_filter
- __future__
- models.response
- monitoring.logger
- typing

### analysis.imbalance_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.inducement_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.liquidity_analyzer
- __future__
- typing

### analysis.liquidity_detector
- __future__
- models.response
- monitoring.logger
- typing

### analysis.liquidity_pool_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.liquidity_sweep_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.liquidity_sweep_detector
- __future__
- models.response
- monitoring.logger
- typing

### analysis.market_structure
- __future__
- models.response
- monitoring.logger
- typing

### analysis.market_structure_analyzer
- __future__
- core.base_analyzer
- dataclasses
- pandas
- typing

### analysis.mitigation_block_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.news_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.order_block_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.order_block_detector
- __future__
- models.response
- monitoring.logger
- typing

### analysis.premium_discount_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.session_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.swing_detector
- dataclasses
- typing

### analysis.trend_alignment_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.volatility_analyzer
- __future__
- core.base_analyzer
- typing

### analysis.volume_analyzer
- __future__
- core.base_analyzer
- typing

### config.__init__
- No dependencies

### config.logging
- config.storage
- dataclasses
- pathlib

### config.mt5
- __future__
- dataclasses
- pathlib
- typing

### config.risk
- __future__
- dataclasses

### config.scoring
- dataclasses
- typing

### config.settings
- dataclasses
- pathlib
- typing

### config.storage
- config.settings
- dataclasses
- pathlib

### config.symbols
- dataclasses
- typing

### config.tests.test_timeframes
- config.timeframes

### config.timeframes
- dataclasses
- typing

### config.trading
- __future__
- dataclasses
- enum

### core.__init__
- No dependencies

### core.analyzer_manager
- __future__
- core.analyzer_registry
- core.analyzer_result
- core.base_analyzer
- datetime
- typing

### core.analyzer_registry
- __future__
- core.analyzer_result
- core.base_analyzer
- logging
- time
- traceback
- typing

### core.analyzer_result
- __future__
- dataclasses
- datetime
- typing

### core.application
- __future__

### core.base_analyzer
- __future__
- abc
- typing

### core.decision_engine
- config.scoring
- core.scoring_models
- dataclasses
- typing

### core.scoring.__init__
- No dependencies

### core.scoring_models
- config.scoring
- dataclasses
- typing

### core.service_locator
- __future__
- services.account_service
- services.configuration_service
- services.database_service
- services.maintenance_service
- services.market_service
- services.performance_service
- services.signal_service
- services.storage_service
- services.trade_service

### core.signal_engine
- core.analyzer_registry
- core.decision_engine
- core.signal_models
- core.strategy_registry
- typing

### core.signal_models
- __future__
- core.analyzer_result
- dataclasses
- datetime
- enum
- typing

### core.strategy_registry
- dataclasses
- typing

### data.account_data
- MetaTrader5
- __future__
- models.response
- monitoring.logger

### data.candle_data
- MetaTrader5
- __future__
- models.response
- monitoring.logger
- typing

### data.market_data
- MetaTrader5
- __future__
- models.response
- monitoring.logger

### data.mt5_connection
- MetaTrader5
- __future__
- config.mt5
- monitoring.logger

### data.symbol_data
- MetaTrader5
- __future__
- models.response
- monitoring.logger

### data.terminal_data
- MetaTrader5
- __future__
- monitoring.logger

### database.backup
- __future__
- config.storage
- datetime
- monitoring.logger
- pathlib
- shutil

### database.database
- __future__
- config.storage
- monitoring.logger
- pathlib
- sqlite3
- typing

### database.health
- __future__
- database.database
- database.maintenance
- datetime
- monitoring.logger
- typing

### database.maintenance
- __future__
- database.database
- datetime
- monitoring.logger
- typing

### database.migrations
- __future__
- collections.abc
- database.database
- monitoring.logger

### database.repositories.market_repository
- __future__
- database.database
- monitoring.logger
- typing

### database.repositories.performance_repository
- __future__
- database.database
- monitoring.logger
- typing

### database.repositories.position_repository
- __future__
- database.database
- monitoring.logger
- typing

### database.repositories.signal_repository
- __future__
- database.database
- monitoring.logger
- typing

### database.repositories.trade_repository
- __future__
- database.database
- monitoring.logger
- typing

### database.schema
- __future__
- database.database
- monitoring.logger

### database.services.database_service
- __future__
- database.repositories.market_repository
- database.repositories.performance_repository
- database.repositories.position_repository
- database.repositories.signal_repository
- database.repositories.trade_repository
- monitoring.logger
- typing

### fix_signal_engine
- pathlib
- shutil

### main
- core.application

### models.response
- __future__
- dataclasses
- typing

### models.signal
- __future__
- dataclasses
- enum

### monitoring.__init__
- No dependencies

### monitoring.logger
- __future__
- config.logging
- logging
- logging.handlers

### rename_project_structure
- pathlib
- shutil

### services.account_service
- __future__
- data.account_data
- models.response
- monitoring.logger

### services.configuration_service
- __future__
- config.settings
- monitoring.logger

### services.database_service
- __future__
- database.database
- monitoring.logger

### services.maintenance_service
- __future__
- database.maintenance
- monitoring.logger
- typing

### services.market_service
- __future__
- database.repositories.market_repository
- monitoring.logger
- typing

### services.performance_service
- __future__
- collections
- datetime
- monitoring.logger
- typing

### services.signal_service
- __future__
- database.repositories.signal_repository
- monitoring.logger
- typing

### services.storage_service
- __future__
- monitoring.logger
- storage

### services.trade_service
- __future__
- database.repositories.trade_repository
- monitoring.logger
- typing

### tests.__init__
- No dependencies

### tests.test_account_data
- data.account_data
- models.response
- types
- unittest.mock

### tests.test_analyzer_registry
- core.analyzer_registry
- core.analyzer_result
- core.base_analyzer
- pytest

### tests.test_analyzer_result
- core.analyzer_result
- datetime

### tests.test_application
- core.application

### tests.test_base_analyzer
- core.base_analyzer
- pytest

### tests.test_bos_detector
- analysis.bos_detector

### tests.test_candle_analyzer
- analysis.candle_analyzer
- models.response

### tests.test_candle_data
- data.candle_data
- models.response
- types
- unittest.mock

### tests.test_candle_patterns
- analysis.candle_patterns

### tests.test_choch_detector
- analysis.choch_detector

### tests.test_decision_engine
- core.decision_engine
- pytest

### tests.test_fvg_analyzer
- analysis.fvg_analyzer
- analysis.fvg_detector
- pytest

### tests.test_fvg_detector
- analysis.fvg_detector

### tests.test_fvg_filter
- analysis.fvg_filter
- pytest

### tests.test_liquidity_analyzer
- analysis.liquidity_analyzer
- pytest
- unittest.mock

### tests.test_liquidity_detector
- analysis.liquidity_detector

### tests.test_liquidity_sweep_detector
- analysis.liquidity_sweep_detector

### tests.test_logger
- os
- sys

### tests.test_logging_config
- config.logging
- monitoring.logger

### tests.test_main
- main
- unittest.mock

### tests.test_market_data
- data.market_data
- models.response
- pytest
- types
- unittest.mock

### tests.test_market_structure
- analysis.market_structure

### tests.test_mt5_config
- config.mt5
- pathlib

### tests.test_mt5_connection
- data.mt5_connection
- unittest.mock

### tests.test_order_block_detector
- analysis.order_block_detector
- pytest

### tests.test_risk
- config.risk

### tests.test_scoring
- config.scoring
- pytest

### tests.test_scoring_models
- config.scoring
- core.scoring_models
- pytest

### tests.test_settings
- config.settings

### tests.test_signal
- models.signal
- pytest

### tests.test_signal_engine
- core.signal_engine
- core.signal_models
- pytest

### tests.test_storage
- config.storage

### tests.test_strategy_registry
- core.strategy_registry

### tests.test_swing_detector
- analysis.swing_detector

### tests.test_symbols
- config.symbols

### tests.test_terminal_data
- data.terminal_data
- types
- unittest.mock

### tests.test_timeframes
- config.timeframes

### tests.test_trading
- config.trading

### tools.__init__
- No dependencies

### tools.apply_patch
- pathlib
- shutil
- sys

### tools.fix_analyzer_registry_phase8
- pathlib

### tools.fix_filesystem_scanner_asdict
- pathlib
- re
- shutil

### tools.fix_parser_shared_list_bug
- pathlib
- re

### tools.fix_python_scanner_statistics
- pathlib
- shutil

### tools.fix_scanner_indentation
- pathlib
- shutil

### tools.fix_storage
- pathlib
- subprocess
- sys

### tools.inspect_scoring_models
- ast
- pathlib

### tools.modernization.config
- __future__
- dataclasses
- logging
- pathlib
- typing

### tools.modernization.python_scanner.architecture_analyzer
- __future__
- collections
- pathlib
- tools.modernization.python_scanner.dependency_graph
- tools.modernization.python_scanner.project_parser
- typing

### tools.modernization.python_scanner.ast_loader
- __future__
- argparse
- ast
- dataclasses
- logging
- pathlib
- tokenize
- typing

### tools.modernization.python_scanner.circular_dependency_detector
- __future__
- pathlib
- tools.modernization.python_scanner.dependency_graph
- tools.modernization.python_scanner.project_parser
- typing

### tools.modernization.python_scanner.class_parser
- __future__
- ast
- pathlib
- tools.modernization.python_scanner.ast_loader
- tools.modernization.python_scanner.function_parser
- tools.modernization.python_scanner.models
- typing

### tools.modernization.python_scanner.class_parser_repair
- __future__
- ast
- pathlib
- tools.modernization.python_scanner.ast_loader
- tools.modernization.python_scanner.class_parser

### tools.modernization.python_scanner.dashboard_builder
- __future__
- json
- pathlib
- tools.modernization.python_scanner.architecture_analyzer
- tools.modernization.python_scanner.circular_dependency_detector
- tools.modernization.python_scanner.dependency_graph
- tools.modernization.python_scanner.models
- tools.modernization.python_scanner.modernization_recommender
- tools.modernization.python_scanner.project_health_score
- tools.modernization.python_scanner.project_parser

### tools.modernization.python_scanner.dependency_graph
- __future__
- collections
- pathlib
- tools.modernization.python_scanner.models
- tools.modernization.python_scanner.project_parser
- typing

### tools.modernization.python_scanner.dependency_report
- __future__
- json
- pathlib
- tools.modernization.python_scanner.dependency_graph
- tools.modernization.python_scanner.dependency_validator
- tools.modernization.python_scanner.project_parser

### tools.modernization.python_scanner.dependency_validator
- __future__
- pathlib
- tools.modernization.python_scanner.dependency_graph
- tools.modernization.python_scanner.project_parser
- typing

### tools.modernization.python_scanner.function_parser
- __future__
- ast
- pathlib
- tools.modernization.python_scanner.ast_loader
- tools.modernization.python_scanner.models
- typing

### tools.modernization.python_scanner.html_dashboard_generator
- __future__
- html
- pathlib
- typing

### tools.modernization.python_scanner.import_parser
- __future__
- ast
- pathlib
- tools.modernization.python_scanner.ast_loader
- tools.modernization.python_scanner.models
- typing

### tools.modernization.python_scanner.models
- __future__
- dataclasses
- pathlib
- typing

### tools.modernization.python_scanner.modernization_recommender
- __future__
- pathlib
- tools.modernization.python_scanner.architecture_analyzer
- tools.modernization.python_scanner.dependency_graph
- tools.modernization.python_scanner.models
- tools.modernization.python_scanner.project_parser
- typing

### tools.modernization.python_scanner.module_parser
- __future__
- ast
- pathlib
- tools.modernization.python_scanner.ast_loader
- tools.modernization.python_scanner.class_parser
- tools.modernization.python_scanner.function_parser
- tools.modernization.python_scanner.import_parser
- tools.modernization.python_scanner.models

### tools.modernization.python_scanner.parser_accuracy_report
- __future__
- json
- pathlib
- tools.modernization.python_scanner.parser_regression_tests

### tools.modernization.python_scanner.parser_regression_tests
- __future__
- dataclasses
- pathlib
- tools.modernization.python_scanner.ast_loader
- tools.modernization.python_scanner.class_parser
- tools.modernization.python_scanner.function_parser
- tools.modernization.python_scanner.import_parser
- tools.modernization.python_scanner.module_parser
- tools.modernization.python_scanner.project_parser
- typing

### tools.modernization.python_scanner.project_health_score
- __future__
- pathlib
- tools.modernization.python_scanner.architecture_analyzer
- tools.modernization.python_scanner.dependency_graph
- tools.modernization.python_scanner.models
- tools.modernization.python_scanner.modernization_recommender
- tools.modernization.python_scanner.project_parser

### tools.modernization.python_scanner.project_parser
- __future__
- pathlib
- tools.modernization.python_scanner.models
- tools.modernization.python_scanner.module_parser

### tools.modernization.python_scanner.report_generator
- __future__
- json
- pathlib
- tools.modernization.python_scanner.models
- tools.modernization.python_scanner.project_parser
- typing

### tools.modernization.python_scanner.scanner
- __future__
- logging
- pathlib
- tools.modernization.python_scanner.project_parser
- tools.modernization.python_scanner.report_generator

### tools.modernization.python_scanner.validation
- __future__
- dataclasses
- pathlib
- tools.modernization.python_scanner.models
- tools.modernization.python_scanner.project_parser
- typing

### tools.modernization.scanner.filesystem_scanner
- __future__
- dataclasses
- json
- logging
- pathlib
- tools.modernization.config
- typing

### tools.patch_analyzer_registry_execute
- pathlib
- re

### tools.patch_analyzer_registry_option1
- pathlib

### tools.patch_analyzer_registry_phase1
- pathlib
- re
- shutil

### tools.patch_decision_engine_return
- pathlib

### tools.patch_scoring_models
- pathlib
- shutil
- sys

### tools.patch_signal_engine_phase4
- pathlib
- shutil

### tools.patch_signal_engine_phase6
- pathlib
- shutil

### tools.patch_signal_engine_phase7
- pathlib

### tools.patch_test_decision_engine
- pathlib

### tools.project_organizer
- pathlib
- shutil

### utils.__init__
- No dependencies

