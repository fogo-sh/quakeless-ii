package render

import "core:fmt"

debug_log :: proc(text: string, args: ..any) {
	fmt.printfln("\x1b[33m%s\x1b[0m", fmt.tprintf(text, ..args))
}
