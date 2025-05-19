# Uniswap V2 State Machine Implementation

## Core Functionality
The system will maintain and track Uniswap V2 pool states by implementing:

- A `V2State` class to represent pool state (reserves, tokens, fees)
- Event handling for mints, burns, and swaps that mutate pool state
- Historical state tracking using Polars DataFrames
- Import/export functionality to save and load states

Users will be able to:
1. Create pool states with initial parameters
2. Feed events to modify pool state
3. Track historical changes over time
4. Save/load progress to files
5. Query pool states and history
6. Calculate key metrics like prices and reserves

## Implementation Todo List

### 1. Core Classes
- [ ] Implement EventType enum (MINT, BURN, SWAP)
- [ ] Create V2State class
 - [ ] Add fields (token0, token1, reserves, fee_tier)
 - [ ] Add validation for inputs
 - [ ] Implement price calculation methods

### 2. Event Handling
- [ ] Create V2Event class/dataclass
- [ ] Implement mint logic
- [ ] Implement burn logic  
- [ ] Implement swap logic
- [ ] Add validation for impossible states

### 3. Historical Tracking
- [ ] Set up Polars DataFrame structure
- [ ] Implement event recording
- [ ] Add timestamp and block number tracking
- [ ] Create methods to query historical states

### 4. Data Persistence
- [ ] Implement save to parquet/CSV
- [ ] Implement load from parquet/CSV
- [ ] Add serialization for V2State
- [ ] Add validation for loaded data

### 5. Testing
- [ ] Unit tests for V2State
- [ ] Unit tests for event handling
- [ ] Integration tests for historical tracking
- [ ] Test data persistence
- [ ] Test edge cases and invalid inputs

### 6. Optimizations & Extras (Optional)
- [ ] Add batch event processing
- [ ] Implement state change notifications
- [ ] Add common query interface
- [ ] Add simulation mode
- [ ] Performance optimizations

## Notes
- Use native ints
- Consider adding logging
- Focus on correctness first, then optimization
- Document key methods and classes

## Future Thoughts
- Add a pool name field
- Consider actually recording the V2State, or a pointer to the State?, of each row in a column of the DataFrame. This would help with things like removing states. That said, `__eq__` for V2State just checks equality of all attributes so it might be redundant and inefficient for that specific purpose
- V2Pool needs a last_state: V2State that gets constantly recorded and tracked so that I can use it with update_state(last_state: V2State, event: V2Event)

```prompt

Hi Claude! I'm implementing a Uniswap v2 state machine in python, then eventually rust, for research and for general use, like routing. 

I have a class “V2State” that records a state of a V2 pool, eg token0 and token1, their amounts, and the fee level. Functions for mint, swap, and burn events will be accessible. Users will be able to feed an event to the api which would change the v2State according to the parameters. There will also be a historical V2Pool or something like that, which would be a Polars DataFrame with the timestamp, block number, values, and maybe the last column stores the V2State at each point in time. Users can import and export a collection of V2States to CSV or Parquet to restart or share progress with others.

I'm relatively new to coding so I'm using this as a chance to learn. Unless I ask you to, please don't use up your time/compute writing code for me -- I want to do it myself! I'm just goign to ask you questions, okay?
```