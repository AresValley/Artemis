# Category
The primary function of this table is to facilitate the classification of the signal by assigning it to its appropriate family or category. Can be used with any tag. The table contains 3 columns explained below.

## CAT_ID
`INTEGER` :material-key-outline:{ title="Primary key" } :material-upload-outline:{ title="Auto-increment" }

This is a unique identification number for each entry that is assigned during the creation of a new category/tag. It is auto-incrementing and is not replaced in the event of deletion.

## SIG_ID
`INTEGER` :material-axis-arrow:{ title="Foreign key" }

This is a direct reference to the specific signal associated with the category. It links to the primary key of the [Signals](db_signals.md) table that holds detailed information about the signals.

## CLB_ID
`INTEGER` :material-axis-arrow:{ title="Foreign key" }

This is a direct reference to the specific **category label** associated with the category. It links to the primary key of the [Category Label](db_cat_label.md) table that holds the name of the category.
