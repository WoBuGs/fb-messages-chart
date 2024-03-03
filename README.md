# fb-messages-chart

This tool is designed to display the number of messages per participant of a Facebook Messenger or Instagram conversation with bar charts.

## Examples

```bash
# Filter on messages sent in 2024 only
python3 messages-chart.py messages/ -y 2024 -Y 2024
```

## Help message

```text
Usage: fb-messages-chart.py [-h] [-w width] [-m min_month] [-y min_year] [-M max_month] [-Y max_year] files [files ...]

Display statistics about a Messenger or Instagram conversation extract

Positional Arguments:
  files         path of the conversations (json format)

Options:
  -h, --help    show this help message and exit
  -w width      width of the rects (default=1)
  -m min_month  month of the start date (default=0)
  -y min_year   year of the start date (default=0)
  -M max_month  month of the end date (default=9999)
  -Y max_year   year of the end date (default=9999)
```
