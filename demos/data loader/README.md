## Data Loader prototype demo

Tool for loading and storing clinical trials data from Clinical Trials API v2.

Usage examples:
- Load NCT04590963 and store in the persistent vector store
```
python data_loader.py --nct_id NCT04590963
```
- Load latest 100 NCTs and store in the persistent vector store
```
python data_loader.py --nct_count 100
```
- Data reader is there just as a PoC
```
python data_reader.py
```
> Important: 
> * Python 3.9 - 3.11
> * Please observe required libs in requirements.txt