use std::fs;

fn extract_number(line: &str) -> i32 {
    let vec: Vec<char> = line.chars().filter(|x| x.is_numeric()).collect();

    let first = vec[0];
    let last = vec.last().unwrap_or(&first);

    format!("{}{}", first, last).parse().unwrap()
}

fn main() {
    let file_path = "data/day1.txt";
    let content = fs::read_to_string(file_path).unwrap();
    let result: i32 = content.lines().map(extract_number).sum();

    println!("{}", result)
}
