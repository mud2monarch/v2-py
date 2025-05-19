# %%
from datetime import datetime
import polars as pl

# %%
NO_UPDATE_TX = "No Update Transaction Provided"
NO_UPDATE_TIME = datetime.min

# %%
class V2State:
    """ Immutable representation of an individual v2 pool state
    
    Represents the complete state of a Uniswap V2 pool at a specific point in time,
    including token reserves and last update information. Objects of this class
    are immutable to ensure state consistency.

    Attributes:
        token0_addr (str): Address of the first token in the pair. all lowercase.
        token0_decimals (int): Decimals for token0.
        token1_addr (str): Address of the second token in the pair. all lowercase.
        token1_decimals (int): Decimals for token1.
        pool_addr (str): Address of the V2 pool contract. all lowercase.
        k_invar (int): Constant product of the reserves
        reserve0 (int): Reserve of token0_addr
        reserve1 (int): Reserve of token1_addr
        update_tx (str): Transaction hash where this state was observed. all lowercase. Defaults NO_UPDATE_TX.
        update_time (datetime): Timestamp of `update_tx`. Defaults to 1/1/1970.
    """
    token0_addr: str
    token0_decimals: int
    token1_addr: str
    token1_decimals: int
    pool_addr: str
    k_invar: int
    reserve0: int
    reserve1: int
    update_tx: str
    update_time: datetime

    def __new__(cls,
            token0_addr: str,
            token0_decimals: int,
            token1_addr: str,
            token1_decimals: int,
            pool_addr: str,
            k_invar: int, #@dev TODO: are all of these required? If there is no k provided then we can calculate it for the user, no?
            reserve0: int,
            reserve1: int,
            update_tx: str = NO_UPDATE_TX,
            update_time: datetime = NO_UPDATE_TIME) -> 'V2State':
        
        """Create a new V2State instance.

        Args: See class documentation for parameter details.
        """
        
        obj = super().__new__(cls)
        obj.token0_addr = token0_addr.lower()
        obj.token0_decimals = token0_decimals
        obj.token1_addr = token1_addr.lower()
        obj.token1_decimals = token1_decimals
        obj.pool_addr = pool_addr.lower()
        obj.k_invar = k_invar
        obj.reserve0 = reserve0
        obj.reserve1 = reserve1
        obj.update_tx = update_tx.lower()
        obj.update_time = update_time

        return obj

    def __setattr__(self, name, value):
        """Implementation to enforce immutability"""
        if hasattr(self, name):
            raise AttributeError(f"Can't modify {name}. V2State are immutable.")

        super().__setattr__(name, value)
    
    def __repr__(self):
        """Return a string representation of V2State"""

        print(f"V2State. token0_addr={self.token0_addr}. token1_addr={self.token1_addr}. address={self.pool_addr}. reserve0={self.reserve0}. reserve1={self.reserve1}. invariant={self.k_invar}. last updated at tx {self.update_tx} at time {self.update_time}.")
    
    def __eq__(self, other):
        """Return True if all attributes are equal."""
    
        if not isinstance(other, V2State):
            return False
        
        return (self.token0_addr == other.token0_addr and
                self.token0_decimals == other.token0_decimals and
                self.token1_addr == other.token1_addr and
                self.token1_decimals == other.token1_decimals and
                self.pool_addr == other.pool_addr and
                self.k_invar == other.k_invar and
                self.reserve0 == other.reserve0 and
                self.reserve1 == other.reserve1 and
                self.update_time == other.update_time and
                self.update_tx == other.update_tx)
    
    def get_price(self) -> float:
        """pool price, token1 in terms of token0."""
        
        return self.reserve1 / self.reserve0
        

class V2Pool:
    """Immutable record of the history of a v2 pool. Thin wrapper on a Polars DataFrame.
    
    Represents a historical record of the various states of an arbitrary v2 pool.
    For example, you could record every post-transaction state of the WETH-USDC pool, recording a new state after every event.
    This class is a thin wrapper on top of a Polars DataFrame so that it's easy to analyze data with common ergonomics.
    You can export any individual row as a V2State, or a set of rows as a list of V2States.

    Immutable attributes:
        token0_addr (str): Address of the first token in the pair. all lowercase.
        token0_decimals (int): Decimals for token0.
        token1_addr (str): Address of the second token in the pair. all lowercase.
        token1_decimals (int): Decimals for token1.
        pool_addr (str): Address of the V2 pool contract. all lowercase.
        k_invar (int): Constant product of the reserves
    
    Mutable attributes:
        _df (pl.DataFrame): A Polars DataFrame that stores pool information such as reserves, pool price, etc.
        last_state (V2State): Most recent V2State added to _df
    """
    token0_addr: str
    token0_decimals: int
    token1_addr: str
    token1_decimals: int
    pool_addr: str
    k_invar: int

    _df: pl.DataFrame
    last_state: pl.DataFrame

    def __init__(self):
        """Barebones creation of V2Pool. Everything defaults to None or 0.
        
        Args: see class documentation.
        """

        self.pool_addr: str | None = None
        self.token0_addr: str | None = None
        self.token1_addr: str | None = None
        self.token1_decimals: int | None  = None
        self.pool_addr: str | None = None
        self.k_invar: int | None = None

        self._df = pl.DataFrame(schema= {
            'reserve0': pl.Decimal, # note that Polars' Decimal is unstable, and only 128 bit.
            'reserve1': pl.Decimal,
            'update_tx': pl.String,
            'update_time': pl.Datetime
        })
        self.last_state = self._df.clone()
    
    def __repr__(self):
        """Return a string representation of a V2Pool"""

        df_length: int = self._df.select(pl.len).item()

        print(f"This V2Pool represents {self.pool_addr}, which has {self.token0_addr} and {self.token1_addr}. It has {df_length} rows.")

    def get_dataframe(self) -> pl.DataFrame:
        """Simple return of the DataFrame holding mutable values.
        
        usage: If you need other object data, e.g., for joins, you should add it into your DataFrame with .with_columns()"""
        return self._df
    
    def add_state(self, new_state: V2State) -> V2State:
        """Adds a State to the end of the DataFrame
        
        args:
            new_state (V2State): the V2State that you want to add
        """
        
        data = {
            "reserve0": new_state.reserve0,
            "reserve_1": new_state.reserve1,
            "update_tx": new_state.update_tx,
            "update_time": new_state.update_time
        }
        
        self.last_state = pl.DataFrame(data)

        self._df = pl.concat(self._df, self.last_state)

        return new_state

class Event:
    """A superclass containing all possible Uniswap V2 "Pair" events.
    
    Subclasses of Event include MintEvent, BurnEvent, SwapEvent, and SyncEvent.
    """

class MintEvent(Event):
    """A representation of a Mint event in Uniswap V2.

    UniswapV2 `Mint` has signature `Mint(msg.sender, amount0, amount1)`.
    According to the mint() function in Uniswap V2, amount0 = balanceOf(token0) - reserve0, and
    likewise for amount1. Therefore, amount0/1 in the function signature are the difference between
    the pool balances of token0/1 and reserve0/1 at the time when mint() is called.

    Simply, they are the quantities of tokens added to the pools.

    attributes:
        sender (str): the minter of liquidity
        amount0 (int): the amount of token0 that was added to the pool
        amount1 (int): the amount of token1 that was added to the pool
    """
    sender: str
    amount0: int
    amount1: int

    def __init__(
            self: 'MintEvent',
            sender: str,
            amount0: int,
            amount1: int
    ):
        """Creates a new MintEvent from a sender and two amounts."""

        self.sender = sender.lower()
        self.amount0 = amount0
        self.amount1 = amount1
    
    # Ideally you'd be able to create a list of Mint events from a Polars DataFrame, a CSV, or a parquet. The CSV and parquet versions could just read into a DataFrame

class BurnEvent(Event):
    """A representation of a Burn event in Uniswap V2.

    

    attributes:
        
    """

class SwapEvent(Event):
    pass

class SyncEvent(Event):
    pass


# class CurrentV2State



