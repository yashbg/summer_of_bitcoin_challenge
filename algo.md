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
