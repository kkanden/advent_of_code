library(stringi)
library(purrr)

str <- readLines("input.txt") |> paste(collapse = "")

mul <- function(x, y) x * y

pattern <- "mul\\(\\d{1,3},\\d{1,3}\\)"

muls <- stri_extract_all(str, regex = pattern)[[1]]

sapply(muls, function(x) eval(parse(text = x))) |> sum()

#####################

str_cleaned <- stri_extract_all(str,
  regex = "do\\(\\)|don't\\(\\)|mul\\(\\d{1,3},\\d{1,3}\\)"
)[[1]]

process_list <- function(vec) {
  acc <- c()
  state <- TRUE

  for (e in vec) {
    if (e == "do()") {
      state <- TRUE
    } else if (e == "don't()") {
      state <- FALSE
    } else if (state) {
      acc <- c(acc, e)
    }
  }
  return(acc)
}

process_list(str_cleaned) |>
  sapply(function(x) eval(parse(text = paste0(x)))) |>
  sum()
