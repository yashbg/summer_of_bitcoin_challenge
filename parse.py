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
    with open('mempool.csv') as f:
        next(f) # skipping the first line of mempool.csv
        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])

mempool = parse_mempool_csv()

num_tx = len(mempool) # No. of transactions
print('No. of transactions:', num_tx)

num_with_parents = 0 # No. of transactions having atleast 1 parent transaction
max_num_parents = 0 # Maximum no. of parent transactions of any transaction
for tx in mempool:
    if len(tx.parents) > 0:
        num_with_parents += 1
    max_num_parents = max(max_num_parents, len(tx.parents))
print('No. of transactions having atleast 1 parent transaction:', num_with_parents)
print('Maximum no. of parent transactions of any transaction:', max_num_parents)