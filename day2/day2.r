library(data.table)

data <- fread("input.csv", fill = TRUE)

is_safe <- function(report) {
  is_sorted <- !is.unsorted(report, strictly = TRUE) | !is.unsorted(-report, strictly = TRUE)

  lagged <- c(NA, report)

  distance <- abs(c(report, NA) - lagged)

  is_safe <- is_sorted && max(distance, na.rm = TRUE) %between% c(1, 3)

  return(is_safe)
}

is_safe_removed <- function(report) {
  if (is_safe(report)) {
    return(TRUE)
  }

  for (i in seq_along(report)) {
    if (is_safe(report[-i])) {
      return(TRUE)
    }
  }
  return(FALSE)
}

apply(t(data), 2, function(x) is_safe_removed(x[!is.na(x)])) |> sum()
