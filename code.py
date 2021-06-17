MAX_WEIGHT = 4000000

class MempoolTransaction:
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        if parents == '':
            self.parents = []
        else:
            self.parents = [parent for parent in parents.strip().split(';')]

class Block:
    def __init__(self, txids, total_fee, total_weight):
        self.txids = txids
        self.fee = total_fee
        self.weight = total_weight

def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open('mempool.csv') as file:
        next(file) # skipping the first line of mempool.csv
        return [MempoolTransaction(*line.strip().split(',')) for line in file.readlines()]

def analyse_mempool(mempool):
    """Analyse the mempool and print its stats."""
    num_tx = len(mempool) # TOtal no. of transactions
    print('Total no. of transactions:', num_tx)

    num_with_parents = 0 # No. of transactions having atleast 1 parent transaction
    max_num_parents = 0 # Maximum no. of parent transactions of any transaction
    for tx in mempool:
        if len(tx.parents) > 0:
            num_with_parents += 1
        max_num_parents = max(max_num_parents, len(tx.parents))
    print("No. of transactions having atleast 1 parent transaction:", num_with_parents)
    print("Maximum no. of parent transactions of any transaction:", max_num_parents)

def create_children_dict(mempool):
    """Create and return a dictionary which contains the list of children of the transaction for every transaction in the mempool."""
    children_dict = {}
    for tx in mempool:
        children_dict[tx.txid] = []
    
    for tx in mempool:
        for parent in tx.parents:
            children_dict[parent].append(tx)
    return children_dict

def analyse_children_dict():
    """Analyse the children_dict and print its stats."""
    num_with_children = 0 # No. of transactions having atleast 1 child transaction
    max_num_children = 0 # Maximum no. of child transactions of any transaction
    for children in children_dict.values():
        if len(children) > 0:
            num_with_children += 1
        max_num_children = max(max_num_children, len(children))
    print("No. of transactions having atleast 1 child transaction:", num_with_children)
    print("Maximum no. of child transactions of any transaction:", max_num_children)

def create_valid_dict(mempool):
    """Create and return a dictionary which contains True if all of the parents of the transaction have been added to the block."""
    valid_dict = {}
    for tx in mempool:
        if len(tx.parents) == 0:
            valid_dict[tx.txid] = True
        else:
            valid_dict[tx.txid] = False
    return valid_dict

def create_is_added_dict(mempool):
    """Create and return a dictionary which contains True if the transaction has been added to the block."""
    is_added_dict = {}
    for tx in mempool:
        is_added_dict[tx.txid] = False
    return is_added_dict

def save_block_stats(block):
    """Save the stats of the block in stats.txt."""
    with open('stats.txt', 'w') as file:
        file.write(f"Total fee: {block.fee} satoshis\n")
        file.write(f"Total weight: {block.weight}\n")
        file.write(f"Size of block: {len(block.txids)} transactions\n")

def check_tx(tx, curr_weight, is_added_dict):
    """Check if a transaction can be added to the block."""
    if curr_weight + tx.weight > MAX_WEIGHT or is_added_dict[tx.txid] or not valid_dict[tx.txid]:
        return False
    return True

def update_children_validity(tx):
    """Update valid_dict for children of tx."""
    for child in children_dict[tx.txid]:
        for parent in child.parents:
            if not is_added_dict[parent]:
                break
        else:
            valid_dict[child.txid] = True

def add_tx(block, tx):
    """Add a transaction to the block and update the total weight and total fee corresponding to the block."""
    block.weight += tx.weight
    block.fee += tx.fee
    block.txids.append(tx.txid)
    
    is_added_dict[tx.txid] = True
    update_children_validity(tx)

def create_block(sorted_mempool):
    """Create and return a block from the mempool maximizing the fee to the miner and print its stats."""
    block = Block(txids=[], total_fee=0, total_weight=0)
    for i, tx in enumerate(sorted_mempool):
        if check_tx(tx, block.weight, is_added_dict):
            add_tx(block, tx)

            for tx2 in sorted_mempool[:i]:
                if check_tx(tx2, block.weight, is_added_dict):
                    add_tx(block, tx2)
    
    save_block_stats(block)
    print(f"Total fee: {block.fee} satoshis")
    print(f"Total weight: {block.weight}")
    print(f"Size of block: {len(block.txids)} transactions")
    return block

def save_block_txids():
    """Save the transaction identifiers of the block in block.txt."""
    with open('block.txt', 'w') as file:
        for txid in block.txids:
            file.write(txid)
            file.write('\n')

mempool = parse_mempool_csv()

analyse_mempool(mempool)
print()

children_dict = create_children_dict(mempool)
analyse_children_dict()
print()

valid_dict = create_valid_dict(mempool)
is_added_dict = create_is_added_dict(mempool)

sorted_mempool = sorted(mempool, key=lambda tx: tx.fee / tx.weight, reverse=True)

block = create_block(sorted_mempool)

save_block_txids()
