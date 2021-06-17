MAX_WEIGHT = 4000000

class MempoolTransaction():
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        if parents == '':
            self.parents = []
        else:
            self.parents = [parent for parent in parents.strip().split(';')]

def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open('mempool.csv') as file:
        next(file) # skipping the first line of mempool.csv
        return([MempoolTransaction(*line.strip().split(',')) for line in file.readlines()])

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

def print_mempool(mempool):
    """Print the mempool."""
    for tx in mempool:
        print(tx.txid, tx.fee, tx.weight, tx.parents)

def create_children_dict(mempool):
    """Creates and returns a dictionary which contains the list of children of the transaction for every transaction in the mempool."""
    children_dict = {}
    for tx in mempool:
        children_dict[tx.txid] = []
    for tx in mempool:
        for parent in tx.parents:
            children_dict[parent].append(tx)
    return children_dict

def analyse_children_dict(children_dict):
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
    valid_dict = {}
    for tx in mempool:
        if len(tx.parents) == 0:
            valid_dict[tx.txid] = True
        else:
            valid_dict[tx.txid] = False
    return valid_dict

def save_block_stats(block, total_fee, total_weight):
    """Save the stats of the block in stats.txt."""
    with open('stats.txt', 'w') as file:
        file.write(f"Total fee: {total_fee} satoshis\n")
        file.write(f"Total weight: {total_weight}\n")
        file.write(f"Size of block: {len(block)} transactions\n")

def check_tx(block, tx, curr_weight):
    """Check if a transaction can be added to the block."""
    if curr_weight + tx.weight > MAX_WEIGHT:
        return False
    for parent in tx.parents:
        if parent not in block:
            return False
    return True

def add_tx(block, tx, curr_weight, curr_fee):
    curr_weight += tx.weight
    curr_fee += tx.fee
    block.append(tx.txid)
    return curr_weight, curr_fee

def create_block(sorted_mempool, children_dict, valid_dict):
    """Create and return a block from the mempool maximizing the fee to the miner and print its stats."""
    is_added = [False] * len(sorted_mempool)
    block = []
    curr_weight = 0
    curr_fee = 0
    for i, tx in enumerate(sorted_mempool):
        if check_tx(block, tx, curr_weight):
            curr_weight, curr_fee = add_tx(block, tx, curr_weight, curr_fee)
            is_added[i] = True
            for child in children_dict[tx.txid]:
                valid_dict[child.txid] = True
            for j, tx2 in enumerate(sorted_mempool[:i]):
                if not is_added[j] and valid_dict[tx2.txid]:
                    if check_tx(block, tx2, curr_weight):
                        curr_weight, curr_fee = add_tx(block, tx2, curr_weight, curr_fee)
                        is_added[j] = True
                        for child2 in children_dict[tx2.txid]:
                            valid_dict[child2.txid] = True

    save_block_stats(block, curr_fee, curr_weight)
    print(f"Total fee: {curr_fee} satoshis")
    print(f"Total weight: {curr_weight}")
    print(f"Size of block: {len(block)} transactions")
    return block, curr_fee, curr_weight

def save_block_txids(block):
    """Save the transaction identifiers of the block in block.txt."""
    with open('block.txt', 'w') as file:
        for txid in block:
            file.write(txid)
            file.write('\n')

mempool = parse_mempool_csv()

analyse_mempool(mempool)
print()

children_dict = create_children_dict(mempool)
analyse_children_dict(children_dict)
print()

valid_dict = create_valid_dict(mempool)

sorted_mempool = sorted(mempool, key=lambda tx: tx.fee / tx.weight, reverse=True)

block, total_fee, total_weight = create_block(sorted_mempool, children_dict, valid_dict)

save_block_txids(block)
