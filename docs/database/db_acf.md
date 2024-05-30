# ACF
The table contains 4 columns explained below.

!!! example
    A technical explanation on how autocorrelation function works along with a practical example is reported [HERE](../acf_analysis.md)

## ACF_ID
`INTEGER` :material-key-outline:{ title="Primary key" } :material-upload-outline:{ title="Auto-increment" }

This is a unique identification number for each entry that is assigned during the creation of a new ACF. It is auto-incrementing and is not replaced in the event of deletion.

## SIG_ID
`INTEGER` :material-axis-arrow:{ title="Foreign key" }

This is a direct reference to the specific signal associated with the ACF. It links to the primary key of the [Signals](db_signals.md) table that holds detailed information about the signals.

## VALUE
`FLOAT`

The autocorrelation time expressed in ms.

## DESCRIPTION
`TEXT`

The short description is used to explain the details about the autocorrelation value, e.g. `Frame`, `Superframe`, etc.
