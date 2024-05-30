# Modulation
Modulation refers to the method by which information is encoded into the main signal (carrier). This process involves altering various properties of the carrier signal, such as amplitude, frequency, or phase. Multiple modulation techniques can be employed, and a TX station has the capability to utilize different modulation schemes. The table contains 4 columns explained below.

## MDL_ID
`INTEGER` :material-key-outline:{ title="Primary key" } :material-upload-outline:{ title="Auto-increment" }

This is a unique identification number for each entry that is assigned during the creation of a new modulation. It is auto-incrementing and is not replaced in the event of deletion.

## SIG_ID
`INTEGER` :material-axis-arrow:{ title="Foreign key" }

This is a direct reference to the specific signal associated with the modulation. It links to the primary key of the [Signals](db_signals.md) table that holds detailed information about the signals.

## VALUE
`TEXT`

The modulation expressed as a string.

## DESCRIPTION
`TEXT`

The short description is used to explain the purpose of the modulation and any other useful details.
