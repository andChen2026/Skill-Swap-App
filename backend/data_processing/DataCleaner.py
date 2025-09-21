import pandas as pd 
import kagglehub

# Download latest version
path = kagglehub.dataset_download("muhadel/hobbies")
df = pd.read_csv('data/hobbies.csv')

first_ten_rows = df.head(10)
print(first_ten_rows)

print("Path to dataset files:", path)