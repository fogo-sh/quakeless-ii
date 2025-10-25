package render

import "base:runtime"

Init :: proc "c" () -> b32 {
	context = runtime.default_context()

	debug_log("Init")

	return true
}

Shutdown :: proc "c" () {
	context = runtime.default_context()

	debug_log("Shutdown")
}

PrepareForWindow :: proc "c" () -> i32 {
	context = runtime.default_context()

	debug_log("PrepareForWindow")

	return 0
}

InitContext :: proc "c" (sdl_window: rawptr) -> int {
	context = runtime.default_context()

	debug_log("InitContext")

	return 0
}

GetDrawableSize :: proc "c" (width: ^i32, height: ^i32) {
	context = runtime.default_context()

	debug_log("GetDrawableSize")
}

ShutdownContext :: proc "c" () {
	context = runtime.default_context()

	debug_log("ShutdownContext")
}

IsVSyncActive :: proc "c" () -> b32 {
	context = runtime.default_context()

	debug_log("IsVSyncActive")

	return false
}

BeginRegistration :: proc "c" (map_: cstring) {
	context = runtime.default_context()

	debug_log("BeginRegistration")
}

RegisterModel :: proc "c" (name: cstring) -> ^Model {
	context = runtime.default_context()

	debug_log("RegisterModel")

	return nil
}

RegisterSkin :: proc "c" (name: cstring) -> ^Image {
	context = runtime.default_context()

	debug_log("RegisterSkin")

	return nil
}

SetSky :: proc "c" (name: cstring, rotate: f32, axis: [^]f32) {
	context = runtime.default_context()

	debug_log("SetSky")
}

EndRegistration :: proc "c" () {
	context = runtime.default_context()

	debug_log("EndRegistration")
}

RenderFrame :: proc "c" (fd: ^Refdef) {
	context = runtime.default_context()

	debug_log("RenderFrame")
}

DrawFindPic :: proc "c" (name: cstring) -> ^Image {
	context = runtime.default_context()

	debug_log("DrawFindPic")

	return nil
}

DrawGetPicSize :: proc "c" (w: ^i32, h: ^i32, name: cstring) {
	context = runtime.default_context()

	debug_log("DrawGetPicSize")
}

DrawPicScaled :: proc "c" (x: i32, y: i32, pic: cstring, factor: f32) {
	context = runtime.default_context()

	debug_log("DrawPicScaled")
}

DrawStretchPic :: proc "c" (x: i32, y: i32, w: i32, h: i32, name: cstring) {
	context = runtime.default_context()

	debug_log("DrawStretchPic")
}

DrawCharScaled :: proc "c" (x: i32, y: i32, num: i32, scale: f32) {
	context = runtime.default_context()

	debug_log("DrawCharScaled")
}

DrawTileClear :: proc "c" (x: i32, y: i32, w: i32, h: i32, name: cstring) {
	context = runtime.default_context()

	debug_log("DrawTileClear")
}

DrawFill :: proc "c" (x: i32, y: i32, w: i32, h: i32, c: i32) {
	context = runtime.default_context()

	debug_log("DrawFill")
}

DrawFadeScreen :: proc "c" () {
	context = runtime.default_context()

	debug_log("DrawFadeScreen")
}

DrawStretchRaw :: proc "c" (
	x: i32,
	y: i32,
	w: i32,
	h: i32,
	cols: i32,
	rows: i32,
	data: [^]u8,
	bits: i32,
) {
	context = runtime.default_context()

	debug_log("DrawStretchRaw")
}

SetPalette :: proc "c" (palette: [^]u8) {
	context = runtime.default_context()

	debug_log("SetPalette")
}

BeginFrame :: proc "c" (camera_separation: f32) {
	context = runtime.default_context()

	debug_log("BeginFrame")
}

EndFrame :: proc "c" () {
	context = runtime.default_context()

	debug_log("EndFrame")
}

EndWorldRenderpass :: proc "c" () -> b32 {
	context = runtime.default_context()

	debug_log("EndWorldRenderpass")

	return false
}
