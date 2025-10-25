package render

import "core:c"

Model :: struct {
	/*
	char		name[MAX_QPATH];

	int			registration_sequence;

	modtype_t	type;
	int			numframes;

	int			flags;

//
// volume occupied by the model graphics
//
	vec3_t		mins, maxs;
	float		radius;

//
// solid volume for clipping
//
	qboolean	clipbox;
	vec3_t		clipmins, clipmaxs;

//
// brush model
//
	int			firstmodelsurface, nummodelsurfaces;
	int			lightmap;		// only for submodels

	int			numsubmodels;
	struct model_s	*submodels;

	int			numplanes;
	cplane_t	*planes;

	int			numleafs;		// number of visible leafs, not counting 0
	mleaf_t		*leafs;

	int			numvertexes;
	mvertex_t	*vertexes;

	int			numedges;
	medge_t		*edges;

	int			numnodes;
	int			firstnode;
	mnode_t		*nodes;

	int			numtexinfo;
	mtexinfo_t	*texinfo;

	int			numsurfaces;
	msurface_t	*surfaces;

	int			numsurfedges;
	int			*surfedges;

	int			nummarksurfaces;
	msurface_t	**marksurfaces;

	dvis_t		*vis;

	byte		*lightdata;

	// for alias models and skins
	image_t		*skins[MAX_MD2SKINS];

	int			extradatasize;
	void		*extradata;

	// submodules
	vec3_t		origin;	// for sounds or lights

	/* octree  */
	bspxlightgrid_t *grid;
	*/
}

Image :: struct {
	/*
	char name[MAX_QPATH];               /* game path, including extension */
	imagetype_t type;
	int width, height;                  /* source image */
	int upload_width, upload_height;    /* after power of two and picmip */
	int registration_sequence;          /* 0 = free */
	struct msurface_s *texturechain;    /* for sort-by-texture world drawing */
	qvktexture_t vk_texture;            /* Vulkan texture handle */
	*/
}

Refdef :: struct {
	/*
	typedef struct {
	int			x, y, width, height; /* in virtual screen coordinates */
	float		fov_x, fov_y;
	float		vieworg[3];
	float		viewangles[3];
	float		blend[4]; /* rgba 0-1 full screen blend */
	float		time; /* time is used to auto animate */
	int			rdflags; /* RDF_UNDERWATER, etc */

	byte		*areabits; /* if not NULL, only areas with set bits will be drawn */

	lightstyle_t	*lightstyles; /* [MAX_LIGHTSTYLES] */

	int			num_entities;
	entity_t	*entities;

	int			num_dlights; // <= 32 (MAX_DLIGHTS)
	dlight_t	*dlights;

	int			num_particles;
	particle_t	*particles;
	*/
}

Cvar :: struct {
	/*
	char *name;
	char *string;
	char *latched_string; /* for CVAR_LATCH vars */
	int flags;
	qboolean modified; /* set each time the cvar is changed */
	float value;
	struct cvar_s *next;

	/* Added by YQ2. Must be at the end to preserve ABI. */
	char *default_string;
	*/
}

Ref_Restart :: enum i32 {
	UNDEF,
	NO,
	FULL,
	PARTIAL,
}

Ref_Import :: struct {
	Sys_Error:            proc "c" (err_level: int, str: cstring, rest: ..cstring),
	Cmd_AddCommand:       proc "c" (name: string, cmd: proc "c" ()),
	Cmd_RemoveCommand:    proc "c" (name: string),
	Cmd_Argc:             proc "c" () -> int,
	Cmd_Argv:             proc "c" (i: int) -> cstring,
	Cmd_ExecuteText:      proc "c" (exec_when: int, text: cstring),
	Com_VPrintf:          proc "c" (print_level: int, fmt: cstring, argptr: c.va_list),

	// files will be memory mapped read only
	// the returned buffer may be part of a larger pak file,
	// or a discrete file from anywhere in the quake search path
	// a -1 return means the file does not exist
	// NULL can be passed for buf to just determine existance
	FS_LoadFile:          proc "c" (name: cstring, buf: ^rawptr) -> int,
	FS_FreeFile:          proc "c" (buf: rawptr),

	// gamedir will be the current directory that generated
	// files should be stored to, ie: "f:\quake\id1"
	FS_Gamedir:           proc "c" () -> cstring,
	Cvar_Get:             proc "c" (name: cstring, value: cstring, flags: int) -> ^Cvar,
	Cvar_Set:             proc "c" (name: cstring, value: cstring) -> ^Cvar,
	Cvar_SetValue:        proc "c" (name: cstring, value: f32),
	Vid_GetModeInfo:      proc "c" (width: ^i32, height: ^i32, mode: int) -> b32,
	Vid_MenuInit:         proc "c" (),

	// called with image data of width*height pixel which comp bytes per pixel (must be 3 or 4 for RGB or RGBA)
	// expects the pixels data to be row-wise, starting at top left
	Vid_WriteScreenshot:  proc "c" (width: i32, height: i32, comp: i32, data: [^]u8),
	GLimp_InitGraphics:   proc "c" (fullscreen: i32, width: ^i32, height: ^i32) -> b32,
	GLimp_GetDesktopMode: proc "c" (width: ^i32, height: ^i32) -> b32,
	Vid_RequestRestart:   proc "c" (rs: Ref_Restart),
}

Ref_Export :: struct {
	apiversion:         i32,
	framework_version:  i32,
	Init:               proc "c" () -> b32,
	Shutdown:           proc "c" (),
	// called by GLimp_InitGraphics() before creating window,
	// returns flags for SDL window creation, returns -1 on error
	PrepareForWindow:   proc "c" () -> i32,

	// called by GLimp_InitGraphics() *after* creating window,
	// passing the SDL_Window* (void* so we don't spill SDL.h here)
	// (or SDL_Surface* for SDL1.2, another reason to use void*)
	// returns true (1) on success
	InitContext:        proc "c" (sdl_window: rawptr) -> int,

	// called by GLimp_InitGraphics() *after* creating render
	// context. Returns the actual drawable size in the width
	// and height variables. This may be different from the
	// window size due to high dpi awareness.
	GetDrawableSize:    proc "c" (width: ^i32, height: ^i32),

	// shuts down rendering (OpenGL) context.
	ShutdownContext:    proc "c" (),

	// returns true if vsync is active, else false
	IsVSyncActive:      proc "c" () -> b32,

	// All data that will be used in a level should be
	// registered before rendering any frames to prevent disk hits,
	// but they can still be registered at a later time
	// if necessary.
	//
	// EndRegistration will free any remaining data that wasn't registered.
	// Any model_s or skin_s pointers from before the BeginRegistration
	// are no longer valid after EndRegistration.
	//
	// Skins and images need to be differentiated, because skins
	// are flood filled to eliminate mip map edge errors, and pics have
	// an implicit "pics/" prepended to the name. (a pic name that starts with a
	// slash will not use the "pics/" prefix or the ".pcx" postfix)
	BeginRegistration:  proc "c" (map_: cstring),
	RegisterModel:      proc "c" (name: cstring) -> ^Model,
	RegisterSkin:       proc "c" (name: cstring) -> ^Image,
	SetSky:             proc "c" (name: cstring, rotate: f32, axis: [^]f32),
	EndRegistration:    proc "c" (),
	RenderFrame:        proc "c" (fd: ^Refdef),
	DrawFindPic:        proc "c" (name: cstring) -> ^Image,
	DrawGetPicSize:     proc "c" (w: ^i32, h: ^i32, name: cstring), // will return 0 0 if not found
	DrawPicScaled:      proc "c" (x: i32, y: i32, pic: cstring, factor: f32),
	DrawStretchPic:     proc "c" (x: i32, y: i32, w: i32, h: i32, name: cstring),
	DrawCharScaled:     proc "c" (x: i32, y: i32, num: i32, scale: f32),
	DrawTileClear:      proc "c" (x: i32, y: i32, w: i32, h: i32, name: cstring),
	DrawFill:           proc "c" (x: i32, y: i32, w: i32, h: i32, c: i32),
	DrawFadeScreen:     proc "c" (),

	// Draw images for cinematic rendering (which can have a different palette if bits equals to 8).
	DrawStretchRaw:     proc "c" (
		x: i32,
		y: i32,
		w: i32,
		h: i32,
		cols: i32,
		rows: i32,
		data: [^]u8,
		bits: i32,
	),

	// video mode and refresh state management entry points
	SetPalette:         proc "c" (palette: [^]u8), // NULL = game palette
	BeginFrame:         proc "c" (camera_separation: f32),
	EndFrame:           proc "c" (),
	EndWorldRenderpass: proc "c" () -> b32, // finish world rendering, apply postprocess and switch to UI render pass
}
