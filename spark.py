%spark
val data = Seq(1, 2, 3, 4, 5)
val rdd = sc.parallelize(data)
rdd.collect()
