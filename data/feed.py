"""
Market data feed - iterates bar-by-bar
"""
import pandas as pd
from typing import Iterator, Optional
from pathlib import Path
from datetime import datetime
from .bar import Bar


class MarketDataFeed:
   
    def __init__(self, csv_path: str, symbol: str):
        
        self.csv_path = Path(csv_path)
        self.symbol = symbol
        self.data: Optional[pd.DataFrame] = None
        self._current_index = 0
        
    def load(self):
        """Load CSV into memory"""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.csv_path}")
        
        self.data = pd.read_csv(self.csv_path)
        
        # Ensure timestamp column exists
        if 'timestamp' not in self.data.columns:
            raise ValueError("CSV must have 'timestamp' column")
        
        # Convert timestamp to datetime
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        
        # Sort by timestamp
        self.data = self.data.sort_values('timestamp').reset_index(drop=True)
        
        print(f"✅ Loaded {len(self.data)} bars from {self.csv_path}")
        
    def __iter__(self) -> Iterator[Bar]:
        """Iterator protocol"""
        if self.data is None:
            raise RuntimeError("Data not loaded. Call load() first.")
        
        self._current_index = 0
        return self
    
    def __next__(self) -> Bar:
        """Get next bar"""
        if self._current_index >= len(self.data):
            raise StopIteration
        
        row = self.data.iloc[self._current_index]
        self._current_index += 1
        
        return Bar(
            symbol=self.symbol,
            timestamp=row['timestamp'],
            open=float(row['open']),
            high=float(row['high']),
            low=float(row['low']),
            close=float(row['close']),
            
        )
    
    def __len__(self) -> int:
        """Total number of bars"""
        return len(self.data) if self.data is not None else 0