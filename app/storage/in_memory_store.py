import pandas as pd
from typing import Dict, List
from app.core.config import settings

class InMemoryStore:
    def __init__(self):
        self.store: Dict[str, pd.DataFrame] = {}
        # Pre-initialize dfs for allowed symbols
        for symbol in settings.ALLOWED_SYMBOLS:
            self.store[symbol] = pd.DataFrame(
                columns=["ts", "open", "high", "low", "close", "volume"]
            )
            # Ensure ts is datetime
            self.store[symbol]["ts"] = pd.to_datetime(self.store[symbol]["ts"], utc=True)

    def append_bars(self, symbol: str, bars_df: pd.DataFrame):
        """
        Append bars to the store for a given symbol.
        Trims to RETENTION_POINTS.
        """
        if symbol not in self.store:
            # If symbol is not in allowed list, ignore or raise.
            # For now, strict adherence to ALLOWED_SYMBOLS in init
            return 
            
        current_df = self.store[symbol]
        
        # Ensure incoming ts is proper type (if not already)
        if not pd.api.types.is_datetime64_any_dtype(bars_df["ts"]):
             bars_df["ts"] = pd.to_datetime(bars_df["ts"], utc=True)

        # Concat
        updated_df = pd.concat([current_df, bars_df])
        
        # Sort and Drop Duplicates (keep last)
        updated_df = updated_df.sort_values("ts").drop_duplicates(subset=["ts"], keep="last")
        
        # Trim
        if len(updated_df) > settings.RETENTION_POINTS:
            updated_df = updated_df.iloc[-settings.RETENTION_POINTS:]
            
        self.store[symbol] = updated_df

    def get_symbol_df(self, symbol: str) -> pd.DataFrame:
        """Returns a copy of the dataframe for the symbol."""
        return self.store.get(symbol, pd.DataFrame()).copy()

    def stats(self) -> Dict:
        """Returns counts and last timestamp for each symbol."""
        stats = {}
        total_rows = 0
        for symbol, df in self.store.items():
            count = len(df)
            last_ts = df["ts"].max().isoformat() if not df.empty else None
            stats[symbol] = {
                "count": count,
                "last_ts": last_ts
            }
            total_rows += count
        
        return {
            "total_rows": total_rows,
            "symbols": stats
        }

    def is_ready(self) -> Dict:
        """
        Returns readiness status.
        Ready if all ALLOWED_SYMBOLS exist and have >= MIN_POINTS_READY points.
        """
        missing_symbols = []
        not_enough_points = []
        
        for symbol in settings.ALLOWED_SYMBOLS:
            if symbol not in self.store:
                missing_symbols.append(symbol)
                continue
            
            if len(self.store[symbol]) < settings.MIN_POINTS_READY:
                not_enough_points.append({
                    "symbol": symbol, 
                    "count": len(self.store[symbol]),
                    "required": settings.MIN_POINTS_READY
                })
        
        is_ready = len(missing_symbols) == 0 and len(not_enough_points) == 0
        
        return {
            "ready": is_ready,
            "missing_symbols": missing_symbols,
            "not_enough_points": not_enough_points
        }

# Global instance
store = InMemoryStore()
