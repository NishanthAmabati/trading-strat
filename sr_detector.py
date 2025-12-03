import logging
from dataclasses import dataclass
from typing import List, Literal, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

@dataclass
class Candle:
    open: float
    high: float
    low: float
    close: float


@dataclass
class Zone:
    price: float
    ztype: Literal["support", "resistance"]


class SRDetector:
    """
    Detects Support & Resistance using 4-5 candle price compression
    inside the last 240 candles.
    """

    def __init__(
        self,
        window: int = 5,
        compression_threshold: float = 50,
        breakout_threshold: float = 70,
        cluster_pct: float = 0.002
    ):
        """
        :param window: number of consecutive candles to detect compression
        :param compression_threshold: max allowed close-range inside window
        :param breakout_threshold: price movement after zone to classify zone
        :param cluster_pct: cluster levels within % distance
        """
        self.window = window
        self.compression_threshold = compression_threshold
        self.breakout_threshold = breakout_threshold
        self.cluster_pct = cluster_pct

    # ---------------------------------------------------------------
    # 1. Detect compression zones
    # ---------------------------------------------------------------
    def detect_compression_zones(self, candles: List[Candle]) -> List[Zone]:
        zones = []
        closes = [c.close for c in candles]

        # prevent index overflow (window + future candles)
        limit = len(candles) - self.window - 10

        for i in range(limit):
            win = closes[i:i+self.window]

            # CONDITION 1 → close range ≤ 50 points
            if max(win) - min(win) > self.compression_threshold:
                continue

            zone_price = sum(win) / self.window  # average close
            future = closes[i+self.window : i+self.window+10]

            up_move = max(future) - zone_price
            down_move = zone_price - min(future)

            # CLASSIFY SUPPORT OR RESISTANCE
            if up_move > self.breakout_threshold:
                zones.append(Zone(price=zone_price, ztype="support"))
            elif down_move > self.breakout_threshold:
                zones.append(Zone(price=zone_price, ztype="resistance"))

        logging.info(f"Detected {len(zones)} valid SR zones before clustering.")
        return zones

    # ---------------------------------------------------------------
    # 2. Cluster nearby levels (into 2–3 strong zones)
    # ---------------------------------------------------------------
    def cluster(self, levels: List[float]) -> List[float]:
        if not levels:
            return []

        clusters = []

        for lvl in sorted(levels):
            added = False
            for c in clusters:
                if abs(c[0] - lvl) / c[0] < self.cluster_pct:
                    c.append(lvl)
                    added = True
                    break
            if not added:
                clusters.append([lvl])

        # average each cluster
        final_levels = [sum(c) / len(c) for c in clusters]
        return sorted(final_levels)

    # ---------------------------------------------------------------
    # 3. Main function → returns Top 2–3 important zones
    # ---------------------------------------------------------------
    def get_sr(self, candles: List[Candle]) -> Tuple[List[float], List[float]]:
        if len(candles) < 240:
            raise ValueError("Need at least 240 candles.")

        candles = candles[-240:]  # use only last 240
        zones = self.detect_compression_zones(candles)

        support_levels = [z.price for z in zones if z.ztype == "support"]
        resistance_levels = [z.price for z in zones if z.ztype == "resistance"]

        clustered_support = self.cluster(support_levels)
        clustered_resistance = self.cluster(resistance_levels)

        # Return TOP 3
        return clustered_support[:3], clustered_resistance[:3]


# ---------------------------------------------------------------
# Helper Example
# ---------------------------------------------------------------
if __name__ == "__main__":
    # dummy test candles
    data = [
        Candle(100, 110, 95, 105),
        Candle(105, 112, 102, 108),
    ] * 150  # repeat to simulate 300 candles

    detector = SRDetector()
    s, r = detector.get_sr(data)

    print("Support:", s)
    print("Resistance:", r)
