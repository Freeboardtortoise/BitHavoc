module main
import parser

fn main() {
	println("this is a BitHavok... The language that likes binary")


	tokens := parser.parse("00000001 00000001 10000101 00000001 00000001 00000001")
	for token in tokens {
		println("type:${token.type}, token: ${token.token}")
	}
}
