package render

import "core:fmt"
import "vendor:sdl3"

import "base:runtime"

@(export)
GetRefAPI :: proc "c" (ref_import: ^Ref_Import) -> ^Ref_Export {
	context = runtime.default_context()

	ri = ref_import^

	globals.apiversion = API_VERSION
	globals.framework_version = sdl3.VERSIONNUM_MAJOR(sdl3.GetVersion())

	globals.Init = Init
	globals.Shutdown = Shutdown
	globals.PrepareForWindow = PrepareForWindow

	globals.InitContext = InitContext

	globals.GetDrawableSize = GetDrawableSize

	globals.ShutdownContext = ShutdownContext

	globals.IsVSyncActive = IsVSyncActive

	globals.BeginRegistration = BeginRegistration
	globals.RegisterModel = RegisterModel
	globals.RegisterSkin = RegisterSkin
	globals.SetSky = SetSky
	globals.EndRegistration = EndRegistration
	globals.RenderFrame = RenderFrame
	globals.DrawFindPic = DrawFindPic
	globals.DrawGetPicSize = DrawGetPicSize
	globals.DrawPicScaled = DrawPicScaled
	globals.DrawStretchPic = DrawStretchPic
	globals.DrawCharScaled = DrawCharScaled
	globals.DrawTileClear = DrawTileClear
	globals.DrawFill = DrawFill
	globals.DrawFadeScreen = DrawFadeScreen

	globals.DrawStretchRaw = DrawStretchRaw

	globals.SetPalette = SetPalette
	globals.BeginFrame = BeginFrame
	globals.EndFrame = EndFrame
	globals.EndWorldRenderpass = EndWorldRenderpass

	return &globals
}
