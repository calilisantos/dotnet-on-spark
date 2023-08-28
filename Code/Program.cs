using Microsoft.Spark.Sql;
using static Microsoft.Spark.Sql.Functions;

namespace FlowOfCash
{
    class Program
    {
        static void Main(string[] args)
        {
            // Create Spark session
            SparkSession spark =
                SparkSession
                    .Builder()
                    .AppName("flow_of_cash")
                    .GetOrCreate();

            // Create initial DataFrame
            string filePath = args[0];
            DataFrame dataFrame = spark.Read().Parquet(filePath);

            // Display initial DataFrame
            dataFrame.Show();
            //Create accurate DataFrame
            DataFrame acDataframe =
                dataFrame
                    .Select("date", "cash_flow", "accumulated_cash")
                    .WithColumn("date", DateFormat(Col("date"), "dd/MM/yyy"));

            // Display results
            acDataframe.Show();

            // Show the last value of accumulated cash
            acDataframe
                .OrderBy(Desc("date"))
                .Limit(1)
                .Show();

            // Stop Spark session
            spark.Stop();
        }
    }
}
