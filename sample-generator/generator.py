from datetime import datetime, timedelta
import numpy as np
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[3]").appName("sample_generator").getOrCreate()

def generate_cash_flow(accum_cash: int, initial_date: datetime, days_passed: int) -> list:
  INITIAL_CASH_IN = 1000
  INITIAL_CASH_OUT = 900  
  INITIAL_NET_CASH = INITIAL_CASH_IN - INITIAL_CASH_OUT

  values_list = [
    [
      INITIAL_CASH_IN,
      INITIAL_CASH_OUT,
      INITIAL_NET_CASH,
      accum_cash + INITIAL_NET_CASH,
      initial_date
    ]
  ]

  LOWER_RANDOM_VALUE = -200
  UPPER_RANDOM_VALUE = 500

  for day in range(days_passed -1):
    random_cash_in = np.random.randint(LOWER_RANDOM_VALUE, UPPER_RANDOM_VALUE)
    random_cash_out = np.random.randint(LOWER_RANDOM_VALUE, UPPER_RANDOM_VALUE)

    new_cash_in = INITIAL_CASH_IN + random_cash_in
    new_cash_out = INITIAL_CASH_OUT + random_cash_out
    net_cash = new_cash_in - new_cash_out
    initial_date = initial_date + timedelta(days=1)

    new_row = [
      new_cash_in,
      new_cash_out,
      net_cash,
      values_list[day][3] + net_cash,
      initial_date
    ]

    values_list.append(new_row)

  return values_list


INITIAL_ACCUM_CASH = 0
INITIAL_DAY = datetime.now()
NUMBER_OF_DAYS = 3600

values = generate_cash_flow(INITIAL_ACCUM_CASH, INITIAL_DAY, NUMBER_OF_DAYS)

columns = ["cash_in", "cash_out", "cash_flow","accumulated_cash", "date"]

df = spark.createDataFrame(values, columns)

df.show(10)

df.write.parquet("data/cash_flow.parquet")
