# Signals
This is the main table and contains 4 columns explained below.

## SIG_ID
`INTEGER` :material-key-outline:{ title="Primary key" } :material-upload-outline:{ title="Auto-increment" }

This is a unique identification number for each entry that is assigned during the creation of a signal. It is auto-incrementing and is not replaced in the event of signal deletion.

## NAME
`TEXT`

The name of the signal. A simple string that describes in short the analyzed signal. Special characters are allowed.

## DESCRIPTION
`TEXT`

The short description is used to explain the purpose of the signal and some other useful details.

!!! tip
    The DESCRIPTION field supports **Markdown**, a simple markup language for creating rich text using plain text. Headers, emphasis, lists, links, code blocks and many more features for advanced text formtting. [Markdown Basic Syntax :simple-markdown:](https://www.markdownguide.org/basic-syntax/)

## URL
`TEXT`

The sigidwiki (SigID) URL of the selected signal. This is a direct connection to the online database where further details of the signal are collected.

!!! info
    **Internal Use Only** This field is for the SigID database and not intended for user viewing or editing. Personal URLs can be stored in the signal description.
