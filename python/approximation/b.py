from pyspark.sql.types import * 

retimereason_values = [
StructField('PO', StringType(), True)
StructField('POItem', StringType(), True)
StructField('OldExFactDate', StringType(), True)
StructField('OldDeliveryData', StringType(), True)
StructField('NewExFactDate', StringType(), True)
StructField('NewDeliveryDate', StringType(), True)
StructField('Username', StringType(), True)
StructField('ChangedOn', StringType(), True)
StructField('ChangedAt', StringType(), True)
StructField('PoStatus', StringType(), True)
StructField('ReasonCode', StringType(), True)
StructField('REAS_CAT', StringType(), True)
StructField('RET_REAS', StringType(), True)
StructField('RET_TEXT', StringType(), True)
StructField('OldExFactDate2', StringType(), True)
StructField('OldDeliveryDate', StringType(), True)
StructField('NewExfactdate2', StringType(), True)
StructField('NewDeliveryDate2', StringType(), True)
StructField('Changedon2', StringType(), True)
]

retimereason_schema = (StructType(otd_string_values))
