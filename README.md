# fb-messages-chart

This tool is designed to display the number of messages per participant of a Facebook Messenger or Instagram conversation with bar charts.

## Help

Display statistics about a Messenger or Instagram conversations extract

```bash
$: fb-messages-chart.py --help

Usage: fb-messages-chart.py [-h] [-w width] [-m min_month] [-y min_year] [-M max_month] [-Y max_year] files [files ...]

Display statistics about a Messenger or Instagram conversation extract

Positional Arguments:
  files         path of the conversations (json format)

Options:
  -h, --help    show this help message and exit
  -w width      width of the rects
  -m min_month  month of the start date
  -y min_year   year of the start date
  -M max_month  month of the end date
  -Y max_year   year of the end date
```
