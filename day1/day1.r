library(data.table)

data <- fread("input.csv", col.names = c("list1", "list2"))

data[, ":="(list1 = sort(list1), list2 = sort(list2))]
data[, ":="(distance = abs(list1 - list2))]

data[, sum(distance)]

similarity_fun <- function(x, list) {
  x * sum(x == list)
}

sapply(data[, list1], similarity_fun, list = data[,list2]) |> sum()
