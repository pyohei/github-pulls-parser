# github-pulls-parser

This script enable to fetch GitHub pull request data and 

# Example

If you fetch cpython project, you run fetch script first.

```bash
python fetch.py --token yourtoken --owner pyohei --repo github-pulls-parser --start-page 1 --end-page 3
```

After this, you can get reviewers list.

```bash
python parser.py 
```

This return the below value(formatted by pprint).  

```python
{'approves': {'xxxx': 7,
              'yyyy': 7},
 'count': 100}
```
