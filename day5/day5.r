library(data.table)
data1 <- fread("input1.csv", col.names = c("first", "second"))
data2 <- fread("input2.csv", fill = TRUE)

is_valid_update <- function(queue, ruleset) {
  queue <- queue[!is.na(queue)]
  for (i in seq_along(queue)) {
    e <- queue[i]
    rules <- ruleset[first == e, second]
    if (length(rules) == 0) next
    for (rule in rules) {
      inds <- which(queue == rule)
      if (length(inds) == 0) next
      if (any(i > inds)) {
        return(FALSE)
      }
    }
  }
  return(TRUE)
}

get_middle_element <- function(vec) {
  vec <- vec[!is.na(vec)]
  return(vec[length(vec) %/% 2 + 1])
}

is_valid <- apply(data2, 1, is_valid_update, ruleset = data1)

apply(data2[is_valid], 1, get_middle_element) |>
  sum()

#####

reorder_queue <- function(queue, ruleset) {
  queue <- queue[!is.na(queue)]
  queue_new <- queue
  for (i in seq_along(queue)) {
    e <- queue[i]
    rules <- ruleset[first == e, second]
    if (length(rules) == 0) next
    for (rule in rules) {
      ind <- which(queue == rule)
      if (length(ind) == 0) next
      if (i > ind) {
        queue_new[i] <- queue[ind]
        queue_new[ind] <- queue[i]
        if (is_valid_update(queue_new, ruleset)) {
          return(queue_new)
        }
      }
    }
  }
}

apply(data2[!is_valid], 1, reorder_queue, ruleset = data1)
