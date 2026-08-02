"""
UDUAK_QUANT_SYSTEM_PROJECT

File: analysis/order_block_detector.py

Description:
    Detects institutional Order Blocks.

Responsibilities:
    - Detect Bullish Order Blocks
    - Detect Bearish Order Blocks
    - Validate input
    - Return standardized Response objects

This module NEVER:
    - Reads MT5 data
    - Retrieves candles
    - Executes trades
    - Performs risk management
    - Detects BOS
    - Detects CHOCH
    - Detects Liquidity
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)

class OrderBlockDetector:
    """
    Detect institutional Order Blocks.

    Input:
        Candle data together with BOS information.

    Output:
        Standard Response object.
    """

    DEFAULT_LOOKBACK: int = 10
    VALID_DIRECTIONS = frozenset({"BULLISH", "BEARISH"})

    # =====================================================================
    # PRIVATE HELPERS
    # =====================================================================

    def _extract_candle_fields(
        self, candle: dict
    ) -> Optional[Tuple[float, float, float, float]]:
        """
        Extract and validate OHLC values from a candle.

        Returns:
            Tuple(open, close, high, low) if all fields present,
            or None if any required field is missing.
        """
        open_price = candle.get("open")
        close_price = candle.get("close")
        high = candle.get("high")
        low = candle.get("low")

        if (
            open_price is None
            or close_price is None
            or high is None
            or low is None
        ):
            return None

        return open_price, close_price, high, low

    # =====================================================================
    # PUBLIC METHODS
    # =====================================================================

    def detect(
        self,
        candles: List[dict],
        bos: dict,
    ) -> Response:

        # -------------------------------------------------------------
        # Validate candle input
        # -------------------------------------------------------------
        if not candles:
            logger.error("No candle data supplied.")
            return Response(
                success=False,
                message="No candle data supplied.",
                error="EMPTY_CANDLES",
                data=None,
            )

        if len(candles) < self.DEFAULT_LOOKBACK:
            logger.error(
                "At least %d candles are required.",
                self.DEFAULT_LOOKBACK,
            )
            return Response(
                success=False,
                message=f"At least {self.DEFAULT_LOOKBACK} candles are required.",
                error="INSUFFICIENT_CANDLES",
                data=None,
            )

        # -------------------------------------------------------------
        # Validate BOS
        # -------------------------------------------------------------
        if not bos:
            logger.error("No BOS data supplied.")
            return Response(
                success=False,
                message="No BOS data supplied.",
                error="EMPTY_BOS",
                data=None,
            )

        if not bos.get("bos"):
            logger.info("No BOS detected.")
            return Response(
                success=True,
                message="No BOS detected.",
                error=None,
                data={
                    "order_block_found": False,
                    "bullish_order_blocks": [],
                    "bearish_order_blocks": [],
                    "bullish_count": 0,
                    "bearish_count": 0,
                },
            )

        direction = bos.get("direction")

        if direction not in self.VALID_DIRECTIONS:
            logger.error("Invalid BOS direction: %s", direction)
            return Response(
                success=False,
                message="Invalid BOS direction.",
                error="INVALID_BOS_DIRECTION",
                data=None,
            )

        bullish_order_blocks: List[dict] = []
        bearish_order_blocks: List[dict] = []

        lookback = candles[-self.DEFAULT_LOOKBACK :]
        start_index = len(candles) - len(lookback)

        valid_candle_count = 0

        # -------------------------------------------------------------
        # Bullish Order Block Detection
        # -------------------------------------------------------------
        if direction == "BULLISH":

            for index in range(len(lookback) - 1, -1, -1):
                candle = lookback[index]
                fields = self._extract_candle_fields(candle)

                if fields is None:
                    continue

                valid_candle_count += 1
                open_price, close_price, high, low = fields

                if close_price < open_price:
                    # Group measurements for future extension
                    body_size = abs(close_price - open_price)

                    bullish_order_blocks.append(
                        {
                            "index": start_index + index,
                            "type": "BULLISH_ORDER_BLOCK",
                            "open": open_price,
                            "close": close_price,
                            "high": high,
                            "low": low,
                            "top": max(open_price, close_price),
                            "bottom": min(open_price, close_price),
                            "body_size": body_size,
                            "time": candle.get("time"),
                            "mitigated": False,
                        }
                    )
                    break

        # -------------------------------------------------------------
        # Bearish Order Block Detection
        # -------------------------------------------------------------
        elif direction == "BEARISH":

            for index in range(len(lookback) - 1, -1, -1):
                candle = lookback[index]
                fields = self._extract_candle_fields(candle)

                if fields is None:
                    continue

                valid_candle_count += 1
                open_price, close_price, high, low = fields

                if close_price > open_price:
                    # Group measurements for future extension
                    body_size = abs(close_price - open_price)

                    bearish_order_blocks.append(
                        {
                            "index": start_index + index,
                            "type": "BEARISH_ORDER_BLOCK",
                            "open": open_price,
                            "close": close_price,
                            "high": high,
                            "low": low,
                            "top": max(open_price, close_price),
                            "bottom": min(open_price, close_price),
                            "body_size": body_size,
                            "time": candle.get("time"),
                            "mitigated": False,
                        }
                    )
                    break

        if valid_candle_count == 0:
            logger.error("All candles in lookback are malformed.")
            return Response(
                success=False,
                message="Invalid candle data in lookback window.",
                error="INVALID_CANDLE_DATA",
                data=None,
            )

        # -------------------------------------------------------------
        # Order Block Summary
        # -------------------------------------------------------------
        order_block_found = bool(bullish_order_blocks or bearish_order_blocks)

        logger.info(
            "Order Block Detection | Bullish=%d Bearish=%d",
            len(bullish_order_blocks),
            len(bearish_order_blocks),
        )

        return Response(
            success=True,
            message="Order Block detected."
            if order_block_found
            else "No Order Block detected.",
            error=None,
            data={
                "order_block_found": order_block_found,
                "bullish_order_blocks": bullish_order_blocks,
                "bearish_order_blocks": bearish_order_blocks,
                "bullish_count": len(bullish_order_blocks),
                "bearish_count": len(bearish_order_blocks),
            },
        )