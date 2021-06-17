## Remaining steps (recursive)

1. **Recursively** check for children everytime a new tx is added

## Done (non-recursive)

- Compare child with the next tx instead of the current tx in `create_block()`  
    ```python
    if child.fee / child.weight >= tx.fee / tx.weight:
    ```

- swap the following lines in `create_block()`:
    ```python
    if child.txid not in block:
        if child.fee / child.weight >= tx.fee / tx.weight:
    ```
## Alternate method (seems better)

- Keep track of which txs can be added (in a list?) and update the list everytime a new tx is added to the block

## Other changes

- Add fee:weight ratio as an attribute in MempoolTransaction class