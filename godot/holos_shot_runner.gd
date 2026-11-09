extends SceneTree
## Generic HOLOS shot runner.
##
## A character/shot scene may implement:
##   holos_apply_shot(config: Dictionary) -> void
##   holos_set_frame(frame_index: int, fps: float) -> void
##
## The runner owns deterministic frame stepping and PNG capture. It does not
## define character animation, dialogue timing, or scene composition.

var _config: Dictionary = {}
var _output_dir: String = ""
var _instance: Node
var _debug_label: Label


func _initialize() -> void:
    call_deferred("_run")


func _fail(message: String, exit_code: int = 1) -> void:
    push_error("HOLOS: " + message)
    quit(exit_code)


func _parse_user_args() -> Dictionary:
    var args := OS.get_cmdline_user_args()
    var parsed := {}
    var index := 0
    while index < args.size():
        var key := args[index]
        if not key.begins_with("--") or index + 1 >= args.size():
            return {}
        parsed[key.trim_prefix("--")] = args[index + 1]
        index += 2
    return parsed




func _setup_debug_overlay() -> void:
    if str(_config.get("mode", "production")) != "debug":
        return
    if not bool(_config.get("debug_overlay", false)):
        return

    var layer := CanvasLayer.new()
    layer.layer = 100
    var panel := PanelContainer.new()
    panel.position = Vector2(12, 12)

    var style := StyleBoxFlat.new()
    style.bg_color = Color(0.02, 0.02, 0.02, 0.82)
    style.content_margin_left = 9.0
    style.content_margin_right = 9.0
    style.content_margin_top = 6.0
    style.content_margin_bottom = 6.0
    panel.add_theme_stylebox_override("panel", style)

    _debug_label = Label.new()
    _debug_label.add_theme_color_override("font_color", Color(1.0, 1.0, 1.0))
    _debug_label.add_theme_font_size_override("font_size", 12)
    panel.add_child(_debug_label)
    layer.add_child(panel)
    get_root().add_child(layer)

func _run() -> void:
    var args := _parse_user_args()
    if not args.has("config") or not args.has("output"):
        _fail("Usage: -- --config <shot.json> --output <directory>")
        return

    var config_path: String = args["config"]
    _output_dir = args["output"]
    if not FileAccess.file_exists(config_path):
        _fail("Shot configuration not found: " + config_path)
        return

    var parsed_json = JSON.parse_string(FileAccess.get_file_as_string(config_path))
    if typeof(parsed_json) != TYPE_DICTIONARY:
        _fail("Shot configuration must be a JSON object.")
        return
    _config = parsed_json

    var scene_path := str(_config.get("scene", ""))
    var start_frame := int(_config.get("start_frame", -1))
    var end_frame := int(_config.get("end_frame", -1))
    var fps := float(_config.get("fps", 0.0))
    var width := int(_config.get("width", 0))
    var height := int(_config.get("height", 0))

    if scene_path.is_empty() or not ResourceLoader.exists(scene_path):
        _fail("Configured scene does not exist: " + scene_path)
        return
    if start_frame < 0 or end_frame <= start_frame or fps <= 0.0:
        _fail("Invalid frame range or frame rate.")
        return
    if width <= 0 or height <= 0:
        _fail("Output width and height must be positive.")
        return

    get_root().size = Vector2i(width, height)
    var packed := load(scene_path) as PackedScene
    if packed == null:
        _fail("Could not load PackedScene: " + scene_path)
        return

    _instance = packed.instantiate()
    get_root().add_child(_instance)
    if _instance.has_method("holos_apply_shot"):
        _instance.call("holos_apply_shot", _config)
    _setup_debug_overlay()

    var directory := DirAccess.make_dir_recursive_absolute(_output_dir)
    if directory != OK and directory != ERR_ALREADY_EXISTS:
        _fail("Could not create output directory: " + _output_dir)
        return

    for frame_index in range(start_frame, end_frame):
        if _debug_label != null:
            _debug_label.text = "HOLOS DEBUG  |  %s  |  frame %d" % [
                str(_config.get("shot_id", "unknown")),
                frame_index
            ]
        if _instance.has_method("holos_set_frame"):
            _instance.call("holos_set_frame", frame_index, fps)
        await process_frame
        await process_frame

        var image := get_root().get_texture().get_image()
        if image == null or image.is_empty():
            _fail("Viewport returned an empty image at frame %d." % frame_index)
            return

        var frame_name := "frame_%06d.png" % (frame_index - start_frame)
        var save_error := image.save_png(_output_dir.path_join(frame_name))
        if save_error != OK:
            _fail("Could not save frame: " + frame_name)
            return

    print("HOLOS_RENDER_COMPLETE frames=%d output=%s" % [
        end_frame - start_frame,
        _output_dir
    ])
    quit(0)
