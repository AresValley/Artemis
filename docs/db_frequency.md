# Frequency
The table contains 4 columns explained below.

## FREQ_ID
`INTEGER` :material-key-outline:{ title="Primary key" } :material-upload-outline:{ title="Auto-increment" }

This is a unique identification number for each entry that is assigned during the creation of a new frequency. It is auto-incrementing and is not replaced in the event of deletion.

## SIG_ID
`INTEGER` :material-axis-arrow:{ title="Foreign key" }

This is a direct reference to the specific signal associated with the frequency. It links to the primary key of the [Signals](db_signals.md) table that holds detailed information about the signals.

## VALUE
`INTEGER`

The freqeuncy in Hz expressed as an integer.

## DESCRIPTION
`TEXT`

The short description is used to explain the purpose of the bandwidth and any other useful details.
