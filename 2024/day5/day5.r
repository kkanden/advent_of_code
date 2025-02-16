library(data.table)
ruleset <- fread("input1.csv", col.names = c("first", "second"))
updates <- fread("input2.csv", fill = TRUE)

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

is_valid <- apply(updates, 1, is_valid_update, ruleset = ruleset)

apply(updates[is_valid], 1, get_middle_element) |>
  sum()

#####

max_second <- function(first_var, ruleset) {
  max(ruleset[first == first_var, second])
}

create_chain <- function(ruleset) {
  max_first <- max(ruleset[, first])
  chain <- c(max_first)
  next_node <- max_second(max_first, ruleset)
  while (!next_node %in% chain) {
    chain <- append(chain, next_node)
  }
}

reorder_queue <- function(queue, ruleset) {
}

apply(updates[!is_valid], 1, reorder_queue, ruleset = ruleset)
