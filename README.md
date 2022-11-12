# cpx_utils

CLI tool for fetching information about servers and services from CPX API.

## Usage

There are two modes of operation:
- `snapshot` retrieves information one single time and writes to standard output as specified;
- `watch` continuously fetches information, locking and updating the screen as long as desired.

### Snapshot mode

It is ideal for integration with other tools or for obtaining a quick overview of CPX servers and services.

The output format can be configured for `table` (easy to view), `csv`, or `json`.

The level of detail can be `summary` in which only high level is displayed, or `full` in order to retrieve a full list of servers and services, as well as theirs details.

### Watch mode

It is useful for directly monitoring servers and services during debugging, deployment, or disaster recovery situation.

The displayed information can be `simple`, where only high level numbers are informed, of `complete` where a more columns, analysis, and alerts is provided.

## Next steps

1. Integration with statsd for enabling more thorough data collection and analysis.
2. Introduce retry/fallback mechanisms for the case CPX API is not available.
3. Improve appearance and features of watch mode.