extends SceneTree
## Loads configured episode scenes as PackedScene resources without instantiating them.

const REPORT_MARKER := "HOLOS_SCENE_PREFLIGHT="
const RESOURCE_PREFIX := "res" + "://"


func _initialize() -> void:
    call_deferred("_run")


func _parse_args() -> Dictionary:
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


func _run() -> void:
    var args := _parse_args()
    if not args.has("manifest"):
        push_error("HOLOS scene preflight requires --manifest <path>.")
        quit(2)
        return
    var manifest_path: String = args["manifest"]
    if not FileAccess.file_exists(manifest_path):
        push_error("HOLOS scene preflight manifest not found: " + manifest_path)
        quit(2)
        return
    var parsed = JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
    if typeof(parsed) != TYPE_DICTIONARY or typeof(parsed.get("scenes")) != TYPE_ARRAY:
        push_error("HOLOS scene preflight manifest must contain a scenes array.")
        quit(2)
        return

    var checked: Array[Dictionary] = []
    var errors: Array[Dictionary] = []
    for value in parsed["scenes"]:
        var scene_path := str(value)
        var item := {"scene": scene_path, "valid": false, "error": ""}
        if not scene_path.begins_with(RESOURCE_PREFIX) or scene_path.length() <= 6:
            item["error"] = "not a valid Godot resource path"
        elif not ResourceLoader.exists(scene_path):
            item["error"] = "Godot ResourceLoader cannot find the resource"
        else:
            var resource = ResourceLoader.load(scene_path)
            if resource == null:
                item["error"] = "Godot failed to load the resource"
            elif not resource is PackedScene:
                item["error"] = "resource loaded but is not a PackedScene"
            else:
                item["valid"] = true
        checked.append(item)
        if not item["valid"]:
            errors.append(item)

    var report := {
        "valid": errors.is_empty(),
        "checked": checked,
        "errors": errors,
        "godot_version": Engine.get_version_info(),
    }
    print(REPORT_MARKER + JSON.stringify(report))
    quit(0 if errors.is_empty() else 1)
