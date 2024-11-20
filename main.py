# %%
from datetime import datetime

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
        token0 (str): Address of the first token in the pair. all lowercase.
        token1 (str): Address of the second token in the pair. all lowercase.
        pool_address (str): Address of the V2 pool contract. all lowercase.
        reserve0 (int): Current reserve of token0
        reserve1 (int): Current reserve of token1
        k_last (int): Constant product of the reserves
        update_tx (str): Transaction hash where this state was observed. Defaults NO_UPDATE_TX.
        update_time (datetime): Timestamp of `update_tx`. Defaults to 1/1/1970.
    """
    token0: str
    token1: str
    pool_address: str
    reserve0: int
    reserve1: int
    k_last: int
    update_tx: str
    update_time: datetime

    def __new__(cls,
            token0: str,
            token1: str,
            pool_address: str,
            reserve0: int,
            reserve1: int,
            k_last: int,
            update_tx: str = NO_UPDATE_TX,
            update_time: datetime = NO_UPDATE_TIME) -> 'V2State':
        
        """Create a new V2State instance.

        Args: See class documentation for parameter details.
        """
        
        obj = super().__new__(cls)
        obj.token0 = token0
        obj.token1 = token1
        obj.pool_address = pool_address
        obj.reserve0 = reserve0
        obj.reserve1 = reserve1
        obj.k_last = k_last
        obj.update_tx = update_tx
        obj.update_time = update_time

        return obj

# ##### CurrentV2State class #######################################################

# # CurrentV2State is an object representing the most "recent" v2 pool (i.e., with respect to the user of the API)
# # CurrentV2State are mutable.

# class CurrentV2State

# ##### V2Pool class #######################################################

# # V2Pool is an object that stores a history of many V2State

# class V2Pool


# %%


# %%



