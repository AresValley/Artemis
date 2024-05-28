# Mode
This field reports the way how a signals has been decoded during the reception. The table contains 4 columns explained below.

## MOD_ID
`INTEGER` :material-key-outline:{ title="Primary key" } :material-upload-outline:{ title="Auto-increment" }

This is a unique identification number for each entry that is assigned during the creation of a new mode. It is auto-incrementing and is not replaced in the event of deletion.

## SIG_ID
`INTEGER` :material-axis-arrow:{ title="Foreign key" }

This is a direct reference to the specific signal associated with the modulation. It links to the primary key of the [Signals](db_signals.md) table that holds detailed information about the signals.

## VALUE
`TEXT`

The mode expressed as a string.

## DESCRIPTION
`TEXT`

The short description is used to explain the purpose of the mode and any other useful details.
