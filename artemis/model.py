from peewee import (
    SqliteDatabase, 
    Proxy, 
    Model, 
    TextField, 
    AutoField, 
    ForeignKeyField, 
    FloatField, 
    IntegerField
)

database: SqliteDatabase = Proxy()

class BaseModel(Model):
    class Meta:
        database = database


class Info(BaseModel):
    date = TextField(column_name='DATE', null=True)
    editable = IntegerField(column_name='EDITABLE', null=True)
    name = TextField(column_name='NAME', null=True)
    version = IntegerField(column_name='VERSION', null=True)

    class Meta:
        primary_key = False


class Signals(BaseModel):
    sig_id = AutoField(column_name='SIG_ID')
    description = TextField(column_name='DESCRIPTION', null=True)
    name = TextField(column_name='NAME', null=True)
    url = TextField(column_name='URL', null=True)
    since_version = IntegerField(column_name='SINCE_VERSION', null=True)


class Acf(BaseModel):
    acf_id = AutoField(column_name='ACF_ID')
    description = TextField(column_name='DESCRIPTION', null=True)
    sig = ForeignKeyField(Signals, column_name='SIG_ID', null=True, backref='acfs')
    value = FloatField(column_name='VALUE', null=True)


class Bandwidth(BaseModel):
    band_id = AutoField(column_name='BAND_ID')
    description = TextField(column_name='DESCRIPTION', null=True)
    sig = ForeignKeyField(Signals, column_name='SIG_ID', null=True, backref='bandwidths')
    value = IntegerField(column_name='VALUE', null=True)


class CategoryLabel(BaseModel):
    clb_id = AutoField(column_name='CLB_ID')
    value = TextField(column_name='VALUE', null=True)


class Category(BaseModel):
    cat_id = AutoField(column_name='CAT_ID')
    clb = ForeignKeyField(CategoryLabel, field='clb_id', column_name='CLB_ID', null=True, backref='categories_labels')
    sig = ForeignKeyField(Signals, column_name='SIG_ID', null=True, backref='categories_signals')


class Documents(BaseModel):
    doc_id = AutoField(column_name='DOC_ID')
    description = TextField(column_name='DESCRIPTION', null=True)
    extension = TextField(column_name='EXTENSION', null=True)
    name = TextField(column_name='NAME', null=True)
    preview = IntegerField(column_name='PREVIEW', null=True)
    sig = ForeignKeyField(Signals, column_name='SIG_ID', null=True, backref='documents')
    type = TextField(column_name='TYPE', null=True)


class Frequency(BaseModel):
    freq_id = AutoField(column_name='FREQ_ID')
    description = TextField(column_name='DESCRIPTION', null=True)
    sig = ForeignKeyField(Signals, column_name='SIG_ID', null=True, backref='frequencies')
    value = IntegerField(column_name='VALUE', null=True)


class Location(BaseModel):
    loc_id = AutoField(column_name='LOC_ID')
    description = TextField(column_name='DESCRIPTION', null=True)
    sig = ForeignKeyField(Signals, column_name='SIG_ID', null=True, backref='locations')
    value = TextField(column_name='VALUE', null=True)


class Mode(BaseModel):
    mod_id = AutoField(column_name='MOD_ID')
    description = TextField(column_name='DESCRIPTION', null=True)
    sig = ForeignKeyField(Signals, column_name='SIG_ID', null=True, backref='modes')
    value = TextField(column_name='VALUE', null=True)


class Modulation(BaseModel):
    mdl_id = AutoField(column_name='MDL_ID')
    description = TextField(column_name='DESCRIPTION', null=True)
    sig = ForeignKeyField(Signals, column_name='SIG_ID', null=True, backref='modulations')
    value = TextField(column_name='VALUE', null=True)
