# Info
This is the database meta table and contains 4 columns explained below.

## NAME
`TEXT`

This is the name of the database.

## DATA
`TEXT`

The creation date when the database has been initialised.

## VERSION
`INTEGER`

A simple integer to denote the database version.

## EDITABLE
`INTEGER`

This field should serve as a writing protection on the database.

* **-1**: reserved to sigID database. This is the primary way to distinguish a valid sigID database
* **0**: read-only database
* **1**: database can be edited with no restrictions
