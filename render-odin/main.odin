package game

import "base:runtime"

@(export)
GetRefAPI :: proc "c" (ref_import: ^Ref_Import) -> ^Ref_Export {
	context = runtime.default_context()

	ri = ref_import^

	return &globals
}
