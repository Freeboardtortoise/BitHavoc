module parser

// main parsor for the BitHovoc parser

struct Token {
pub:
  type string
	token string
}


pub fn parse(code string) []Token{
  //loop over letters

  len_byte := 8
  len_line := 5
  mut current_char := 0
  mut current_line := 0
  mut current_byte := 0
  mut tokens := []Token{}
  mut current_token := ""

  for mut letter in code.runes() {
    if letter.str() == "/n" || current_byte >= len_line {
      current_line++
      current_char = 0
      current_byte = 0
      tokens << Token{type: "NEWLINE", token: letter.str() }
      current_token = ""
    } else if letter == " " {
      current_byte++
      current_char = 0
      tokens << Token{type: "SPLIT", token: " " }
      tokens << Token{type: "BYTE", token: current_token}
      current_token = ""
    } else if current_char >= len_byte {
      current_byte++
      current_char = 0
      tokens << Token{type: "SPLIT", token: " " }
      tokens << Token{type: "BYTE", token: current_token}
      current_token = ""
    } else {
      current_char++
      current_token = current_token + letter.str()
    }
  }
  return tokens
}
