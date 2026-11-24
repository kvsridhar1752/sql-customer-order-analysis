# Generated SQL Analysis Results

The analysis was run on a SQLite database containing 800 customers, 20 products, and 5,000 orders.

## Overall KPIs

| Metric | Result |
|---|---:|
| Total orders | 5,000 |
| Active customers | 545 |
| Total revenue | EUR 968,983.84 |
| Average order value | EUR 193.80 |

## Customer value

| Customer type | Customers | Revenue (EUR) | Revenue share |
|---|---:|---:|---:|
| One-time customer | 97 | 21,890.40 | 2.26% |
| Repeat customer | 448 | 947,093.44 | 97.74% |

## Key insight

Repeat customers generate 97.74% of total revenue, even though they represent most but not all customers. This highlights the importance of customer retention, repeat-purchase campaigns, and loyalty-focused marketing.

The SQL analysis uses joins, aggregations, CTEs, case-based segmentation, and ranking logic to identify high-value customers, product performance, monthly trends, and repeat-purchase behavior.

Run the project locally with:

```bash
python data/generate_data.py
python analysis/run_sql_analysis.py
```
