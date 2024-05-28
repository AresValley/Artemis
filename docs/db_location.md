# Location
This is the location where the signal is distributed/received. Avoid the usage of the precise location of the TX station or very small town (very rare). It's a good habit to use **nations/continents** or special location (like `Worldwide`). The table contains 4 columns explained below.

## LOC_ID
`INTEGER` :material-key-outline:{ title="Primary key" } :material-upload-outline:{ title="Auto-increment" }

This is a unique identification number for each entry that is assigned during the creation of a new location. It is auto-incrementing and is not replaced in the event of deletion.

## SIG_ID
`INTEGER` :material-axis-arrow:{ title="Foreign key" }

This is a direct reference to the specific signal associated with the location. It links to the primary key of the [Signals](db_signals.md) table that holds detailed information about the signals.

## VALUE
`TEXT`

The location expressed as a string.

## DESCRIPTION
`TEXT`

The short description is used to explain further details about the location.
