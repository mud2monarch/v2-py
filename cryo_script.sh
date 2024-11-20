# WIP. this is just the cryo example script.
# uniswap v2 swaps
cryo logs \
    --label uniswap_v2_swaps \
    --blocks 10M: \
    --reorg-buffer 1000 \
    --subdirs datatype \
    --event-signature "Swap(address indexed sender, uint amount0In, uint amount1In, uint amount0Out, uint amount1Out, address indexed to)" \
    --topic0 0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822