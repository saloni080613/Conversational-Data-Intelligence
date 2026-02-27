
import pandas as pd
from rag_engine import build_rag_index, retrieve_context

# Use a sample dataset for testing
url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/telco.csv'
df = pd.read_csv(url)
print(f'Loaded dataset: {df.shape}')

print('\n=== BUILDING INDEX ===')
sid = build_rag_index(df)
print(f'Index built. Session ID: {sid}')

print('\n=== RETRIEVAL TEST 1 ===')
ctx = retrieve_context('what is the churn rate?')
print(ctx)

print('\n=== RETRIEVAL TEST 2 ===')
ctx2 = retrieve_context('which contract type has most customers?')
print(ctx2)

print('\nDONE — paste this output in group chat')