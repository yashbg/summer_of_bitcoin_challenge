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
    """Analyse the mempool and print the stats."""
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

def save_block_stats(block, total_fee, total_weight):
    with open('stats.txt', 'w') as file:
        file.write(f"Total fee: {total_fee} satoshis\n")
        file.write(f"Total weight: {total_weight}\n")
        file.write(f"Size of block: {len(block)} transactions\n")

def create_block(mempool):
    """Create and return a block from the mempool maximizing the fee to the miner and print its stats."""
    block = []
    curr_weight = 0
    curr_fee = 0
    for tx in mempool:
        if curr_weight + tx.weight > MAX_WEIGHT:
            break
        curr_weight += tx.weight
        curr_fee += tx.fee
        block.append(tx.txid)
    save_block_stats(block, curr_fee, curr_weight)

    print(f"Total fee: {curr_fee} satoshis")
    print(f"Total weight: {curr_weight}")
    print(f"Size of block: {len(block)} transactions")
    return block

def save_block_txids(block):
    """Save the transaction identifiers of the block in block.txt"""
    with open('block.txt', 'w') as file:
        for txid in block:
            file.write(txid)
            file.write('\n')

mempool = parse_mempool_csv()

analyse_mempool(mempool)
print()

sorted_mempool = sorted(mempool, key=lambda tx: tx.fee / tx.weight, reverse=True)

block = create_block(sorted_mempool)

save_block_txids(block)
