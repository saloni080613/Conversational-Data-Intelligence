# save as test2_visualizer.py
import pandas as pd
from visualizer import auto_chart

# Fake data to test chart generation
s = pd.Series([42.7, 11.2, 2.8],
              index=["Month-to-month","One year","Two year"])
s.index.name = "Contract"

fig = auto_chart("churn rate by contract", s, pd.DataFrame())
print("Chart generated:", fig is not None)  # Expected: True

# Test with single number
fig2 = auto_chart("total customers", 7043, pd.DataFrame())
print("Chart from number:", fig2 is not None)  # Expected: True

# Test with DataFrame
df = pd.DataFrame({"Contract":["M2M","1yr"],"Churn":[42.7,11.2]})
fig3 = auto_chart("churn by contract", df, df)
print("Chart from df:", fig3 is not None)     # Expected: True

print("visualizer.py OK")