extends Node2D

var _frame_index := 0


func holos_apply_shot(config: Dictionary) -> void:
    _frame_index = int(config.get("start_frame", 0))
    queue_redraw()


func holos_set_frame(frame_index: int, _fps: float) -> void:
    _frame_index = frame_index
    queue_redraw()


func _draw() -> void:
    var phase := float(_frame_index % 24) / 24.0
    draw_rect(Rect2(Vector2.ZERO, Vector2(320, 180)), Color(0.035, 0.045, 0.07))
    draw_circle(Vector2(40.0 + phase * 220.0, 90.0), 18.0, Color(0.95, 0.62, 0.22))
    draw_string(
        ThemeDB.fallback_font,
        Vector2(12, 24),
        "HOLOS ADAPTER TEST  FRAME %d" % _frame_index,
        HORIZONTAL_ALIGNMENT_LEFT,
        -1,
        10,
        Color(0.85, 0.9, 1.0)
    )
