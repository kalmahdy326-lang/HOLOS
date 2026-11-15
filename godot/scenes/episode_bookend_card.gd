extends Control
## Reusable, frame-driven HOLOS title and credit-roll card.
## All visible wording is supplied in shot.scene_config; defaults are placeholders.

var _shot_config: Dictionary = {}
var _scene_config: Dictionary = {}
var _card_mode := "title"
var _elapsed := 0.0
var _title_label: Label
var _subtitle_label: Label
var _credits_label: Label
var _fade_overlay: ColorRect
var _stars: Array[Dictionary] = []


func _ready() -> void:
    set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    mouse_filter = Control.MOUSE_FILTER_IGNORE
    _create_stars()
    _create_labels()
    _fade_overlay = ColorRect.new()
    _fade_overlay.color = Color(0.0, 0.0, 0.0, 0.0)
    _fade_overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
    _fade_overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    add_child(_fade_overlay)
    queue_redraw()


func _create_stars() -> void:
    var rng := RandomNumberGenerator.new()
    rng.seed = 20261115
    for _index in range(72):
        _stars.append({
            "x": rng.randf(),
            "y": rng.randf(),
            "radius": rng.randf_range(0.45, 1.3),
            "speed": rng.randf_range(0.001, 0.006),
            "phase": rng.randf_range(0.0, TAU),
            "twinkle": rng.randf_range(0.25, 0.75),
        })


func _new_label(font_size: int, color: Color) -> Label:
    var label := Label.new()
    label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
    label.add_theme_font_override("font", ThemeDB.fallback_font)
    label.add_theme_font_size_override("font_size", font_size)
    label.add_theme_color_override("font_color", color)
    label.add_theme_color_override("font_shadow_color", Color(0.0, 0.0, 0.0, 0.78))
    label.add_theme_constant_override("shadow_offset_x", 1)
    label.add_theme_constant_override("shadow_offset_y", 2)
    add_child(label)
    return label


func _create_labels() -> void:
    _title_label = _new_label(68, Color(0.91, 0.94, 1.0))
    _subtitle_label = _new_label(27, Color(0.65, 0.71, 0.83))
    _credits_label = _new_label(23, Color(0.82, 0.86, 0.93))
    _credits_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
    _credits_label.clip_text = true


func holos_apply_shot(config: Dictionary) -> void:
    _shot_config = config.duplicate(true)
    var candidate = _shot_config.get("scene_config", {})
    _scene_config = candidate if typeof(candidate) == TYPE_DICTIONARY else {}
    _card_mode = str(_scene_config.get("card_mode", "title"))
    if _card_mode not in ["title", "credits"]:
        _card_mode = "title"

    var screen := get_viewport_rect().size
    _title_label.text = str(_scene_config.get("series_title", "HOLOS"))
    if _card_mode == "title":
        _subtitle_label.text = str(_scene_config.get("episode_title", "Episode 1"))
        _title_label.add_theme_font_size_override("font_size", 68)
        _subtitle_label.add_theme_font_size_override("font_size", 27)
    else:
        _subtitle_label.text = str(_scene_config.get("credits_heading", "CREDITS"))
        _title_label.add_theme_font_size_override("font_size", 32)
        _subtitle_label.add_theme_font_size_override("font_size", 24)

    _title_label.position = Vector2(0.0, screen.y * 0.33 if _card_mode == "title" else 36.0)
    _title_label.size = Vector2(screen.x, 112.0 if _card_mode == "title" else 58.0)
    _title_label.pivot_offset = _title_label.size * 0.5
    _subtitle_label.position = Vector2(0.0, screen.y * (0.50 if _card_mode == "title" else 0.13))
    _subtitle_label.size = Vector2(screen.x, 64.0)

    var line_values = _scene_config.get("credit_lines", [])
    var credit_lines: Array[String] = []
    if typeof(line_values) == TYPE_ARRAY:
        for value in line_values:
            credit_lines.append(str(value))
    if credit_lines.is_empty():
        credit_lines.append("CREDITS PENDING APPROVAL")
    _credits_label.text = "\n".join(credit_lines)
    _credits_label.position = Vector2(72.0, screen.y + 34.0)
    _credits_label.size = Vector2(max(screen.x - 144.0, 160.0), max(credit_lines.size() * 42.0, 72.0))

    _title_label.visible = true
    _subtitle_label.visible = true
    _credits_label.visible = _card_mode == "credits"
    _elapsed = 0.0
    _apply_frame_state()
    queue_redraw()


func holos_set_frame(frame_index: int, fps: float) -> void:
    if fps <= 0.0:
        return
    var start_frame := int(_shot_config.get("start_frame", frame_index))
    _elapsed = max(float(frame_index - start_frame) / fps, 0.0)
    _apply_frame_state()
    queue_redraw()


func _apply_frame_state() -> void:
    var screen := get_viewport_rect().size
    var shot_start := int(_shot_config.get("start_frame", 0))
    var shot_end := int(_shot_config.get("end_frame", shot_start + 1))
    var fps: float = max(float(_shot_config.get("fps", 24.0)), 1.0)
    var duration: float = max(float(shot_end - shot_start) / fps, 1.0)
    var remaining: float = max(duration - _elapsed, 0.0)
    _fade_overlay.color = Color(0.0, 0.0, 0.0, 1.0 - clamp(remaining / 0.9, 0.0, 1.0))
    var enter_time: float = 0.7 if _card_mode == "credits" else 0.24
    var p: float = clamp(_elapsed / enter_time, 0.0, 1.0)
    var eased: float = p * p * (3.0 - 2.0 * p)

    if _card_mode == "title":
        var title_time: float = max(_elapsed - 2.0, 0.0)
        var title_p: float = clamp(title_time / 0.24, 0.0, 1.0)
        var title_eased: float = title_p * title_p * (3.0 - 2.0 * title_p)
        var snap: float = title_p
        var title_alpha: float = clamp(title_time / 0.08, 0.0, 1.0)
        _title_label.modulate = Color(1.0, 1.0, 1.0, title_alpha)
        _subtitle_label.modulate = Color(1.0, 1.0, 1.0, clamp((_elapsed - 3.0) / 0.5, 0.0, 1.0))
        _title_label.position.y = screen.y * 0.33 + (1.0 - snap) * 13.0
        _title_label.scale = Vector2.ONE * (1.08 - 0.08 * title_eased + 0.018 * sin(title_p * PI) * (1.0 - title_p))
        _credits_label.visible = false
    else:
        _title_label.modulate = Color(1.0, 1.0, 1.0, eased)
        _subtitle_label.modulate = Color(1.0, 1.0, 1.0, clamp((_elapsed - 0.45) / 0.5, 0.0, 1.0))
        _title_label.position.y = 30.0 + (1.0 - eased) * 8.0
        var credit_count: int = max(_credits_label.text.split("\n", false).size(), 1)
        var content_height: float = float(credit_count) * 42.0
        var outro_start: float = max(duration - 6.0, 0.0)
        var scroll_window: float = max(outro_start - 2.0, 1.0)
        var scroll_progress: float = clamp((_elapsed - 2.0) / scroll_window, 0.0, 1.0)
        var eased_scroll: float = scroll_progress * scroll_progress * (3.0 - 2.0 * scroll_progress)
        var start_y: float = screen.y + 24.0
        var target_y: float = screen.y * 0.60 - content_height * 0.5
        _credits_label.position.y = lerp(start_y, target_y, eased_scroll)
        var outro_progress: float = clamp((_elapsed - outro_start) / 2.0, 0.0, 1.0)
        var outro_eased: float = outro_progress * outro_progress * (3.0 - 2.0 * outro_progress)
        var credit_alpha: float = clamp((_elapsed - 1.8) / 0.5, 0.0, 1.0)
        credit_alpha *= 1.0 - clamp((_elapsed - outro_start) / 0.55, 0.0, 1.0)
        _credits_label.modulate = Color(1.0, 1.0, 1.0, credit_alpha)
        _title_label.position.y = lerp(_title_label.position.y, screen.y * 0.33, outro_eased)
        _title_label.size.y = lerp(58.0, 112.0, outro_eased)
        _title_label.add_theme_font_size_override("font_size", int(round(32.0 + 36.0 * outro_eased)))
        _subtitle_label.modulate = Color(1.0, 1.0, 1.0, (1.0 - outro_eased) * clamp((_elapsed - 0.45) / 0.5, 0.0, 1.0))


func _draw() -> void:
    var screen := get_viewport_rect().size
    draw_rect(Rect2(Vector2.ZERO, screen), Color(0.008, 0.012, 0.032), true)
    draw_circle(Vector2(screen.x * 0.74, screen.y * 0.48), screen.y * 0.43,
        Color(0.035, 0.055, 0.12, 0.38))
    draw_circle(Vector2(screen.x * 0.74, screen.y * 0.48), screen.y * 0.31,
        Color(0.018, 0.028, 0.067, 0.94))
    draw_circle(Vector2(screen.x * 0.74 - screen.y * 0.10, screen.y * 0.48 - screen.y * 0.08),
        screen.y * 0.28, Color(0.008, 0.012, 0.032, 0.72))

    for star in _stars:
        var x := fposmod(float(star["x"]) + _elapsed * float(star["speed"]), 1.0)
        var y := float(star["y"])
        var pulse := 0.18 + 0.18 * sin(_elapsed * float(star["twinkle"]) + float(star["phase"]))
        draw_circle(Vector2(x * screen.x, y * screen.y), float(star["radius"]),
            Color(0.65, 0.73, 0.88, pulse))

    var orbit_start: float = 6.0 if _card_mode == "title" else 0.0
    var orbit_duration: float = 4.0 if _card_mode == "title" else 1.4
    var reveal: float = clamp((_elapsed - orbit_start) / orbit_duration, 0.0, 1.0)
    var orbit_center := Vector2(screen.x * 0.74, screen.y * 0.48)
    draw_arc(orbit_center, screen.y * 0.34, -2.55, -2.55 + TAU * 0.72 * reveal,
        72, Color(0.37, 0.49, 0.68, 0.50), 1.25, true)
    draw_arc(orbit_center, screen.y * 0.38, 0.18, 2.1,
        72, Color(0.60, 0.38, 0.20, 0.18), 1.0, true)
    var shot_start := int(_shot_config.get("start_frame", 0))
    var shot_end := int(_shot_config.get("end_frame", shot_start + 1))
    var fps: float = max(float(_shot_config.get("fps", 24.0)), 1.0)
    var duration: float = max(float(shot_end - shot_start) / fps, 1.0)
    var credits_outro := _card_mode == "credits" and _elapsed >= duration - 6.0
    if _card_mode == "title" or credits_outro:
        var accent_progress: float = clamp((_elapsed - 3.58) / 0.42, 0.0, 1.0)
        if credits_outro:
            accent_progress = clamp((_elapsed - (duration - 5.0)) / 0.8, 0.0, 1.0)
        var accent_y: float = screen.y * (0.50 if credits_outro else 0.625)
        var accent_center := screen.x * 0.5
        draw_line(Vector2(accent_center - 92.0, accent_y),
            Vector2(accent_center - 92.0 + 184.0 * accent_progress, accent_y),
            Color(0.65, 0.40, 0.22, 0.82), 1.25, true)
