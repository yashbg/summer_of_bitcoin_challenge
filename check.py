import sys

MAX_WEIGHT = 4000000

class MempoolTransaction:
    """A class for the transactions of the mempool."""
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid # the transaction identifier
        self.fee = int(fee) # the transaction fee
        self.weight = int(weight) # the transaction weight
        
        # a list of the txids of the transaction’s unconfirmed parent transactions
        if parents == '':
            self.parents = []
        else:
            self.parents = [parent for parent in parents.strip().split(';')]

def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open('mempool.csv') as file:
        next(file) # skipping the first line of mempool.csv
        return [MempoolTransaction(*line.strip().split(',')) for line in file.readlines()]

def get_tx(mempool, txid):
    """Return the MempoolTransaction whose transaction identifier is txid."""
    for tx in mempool:
        if str(tx.txid) == str(txid):
            return tx
    print(f"txid {txid} not found")
    sys.exit()

if __name__ == '__main__':
    mempool = parse_mempool_csv()

    with open('block.txt') as file:
        block = file.read().splitlines()

    total_fee = 0
    total_weight = 0
    for i, txid in enumerate(block):
        tx = get_tx(mempool, txid)
        total_fee += tx.fee
        total_weight += tx.weight
        if len(tx.parents) > 0:
            for parent in tx.parents:
                if parent not in block[:i]:
                    print(f"Parent {parent} of {tx.txid} is not in block")
                    sys.exit()

    if total_weight > MAX_WEIGHT:
        print("Total weight exceeded")
        sys.exit()

    print('Correct')
    print(f"Total fee: {total_fee} satoshis")
    print(f"Total weight: {total_weight}")
    print(f"Size of block: {len(block)} transactions")
