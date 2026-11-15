extends SceneTree
## Headless self-test for holos_timeline.gd.
##
## Run from the repository root:
##   godot --headless --path godot --script res://test_scenes/timeline_selftest.gd
##
## Exit 0: all checks passed. Exit 1: at least one check failed.
## Requires no assets, no audio, and no network.

const HolosTimelineScript = preload("res://holos_timeline.gd")

var _failures: Array[String] = []


func _initialize() -> void:
	call_deferred("_run")


func _check(name: String, condition: bool, detail: String = "") -> void:
	var detail_suffix := (" -- " + detail) if not detail.is_empty() else ""
	print("  [%s] %s%s" % ["PASS" if condition else "FAIL", name, detail_suffix])
	if not condition:
		_failures.append(name)


func _base_events() -> Array:
	return [
		{"speaker": "KEVIN", "start": 0.0, "end": 0.1, "phoneme": "T", "viseme": "wide", "source_word": "Tell"},
		{"speaker": "KEVIN", "start": 0.1, "end": 0.2, "phoneme": "M", "viseme": "closed", "source_word": "me"},
		{"speaker": "KHALED", "start": 0.3, "end": 0.5, "phoneme": "B", "viseme": "closed", "source_word": "Because"},
		{"speaker": "KHALED", "start": 0.5, "end": 0.6, "phoneme": "SIL", "viseme": "rest", "source_word": null},
		{"speaker": "KHALED", "start": 0.6, "end": 0.9, "phoneme": "EH", "viseme": "open", "source_word": "380,000"},
		{"speaker": "KEVIN", "start": 0.9, "end": 1.1, "phoneme": "IH", "viseme": "wide", "source_word": "kilometres"},
		{"speaker": "KEVIN", "start": 1.1, "end": 1.3, "phoneme": "AO", "viseme": "round", "source_word": "away"},
		{"speaker": "KEVIN", "start": 1.3, "end": 1.5, "phoneme": "F", "viseme": "teeth", "source_word": "from"},
		{"speaker": "KEVIN", "start": 1.5, "end": 1.7, "phoneme": "UW", "viseme": "round", "source_word": "you"},
		{"speaker": "KEVIN", "start": 1.7, "end": 2.0, "phoneme": "IH", "viseme": "wide", "source_word": "interesting"},
	]


func _run() -> void:
	print("HOLOS timeline self-test")
	_test_valid_timeline()
	_test_rejections()
	_test_state_at()
	_test_handoff_timelines()
	print()
	if not _failures.is_empty():
		print("SELF-TEST FAIL: %d check(s) failed: %s" % [_failures.size(), str(_failures)])
		quit(1)
		return
	print("SELF-TEST PASS: all checks passed")
	quit(0)


func _test_valid_timeline() -> void:
	var timeline = HolosTimelineScript.from_dictionary({"schema_version": 1, "events": _base_events()}, 3.0)
	_check("valid timeline accepted", timeline.is_valid(), timeline.validation_error)
	_check("all events retained", timeline.events.size() == 10, str(timeline.events.size()))

	var path := "user://holos_timeline_selftest.json"
	var file := FileAccess.open(path, FileAccess.WRITE)
	file.store_string(JSON.stringify({"events": _base_events()}))
	file.close()
	var versioned = HolosTimelineScript.from_dictionary({"schema_version": 1, "events": _base_events()}, 3.0)
	_check("versioned processor output accepted", versioned.is_valid(), versioned.validation_error)
	_check("unsupported schema version rejected",
		not HolosTimelineScript.from_dictionary({"schema_version": 99, "events": _base_events()}).is_valid())
	var loaded = HolosTimelineScript.from_file(path, 3.0)
	_check("timeline loads from file", loaded.is_valid(), loaded.validation_error)
	_check("missing file reported", not HolosTimelineScript.from_file("user://does_not_exist.json").is_valid())


func _test_rejections() -> void:
	var cases: Array = [
		["out-of-order rejected", func(): return _mutated(func(e: Array):
			e[1]["start"] = 0.05)],
		["bad viseme rejected", func(): return _mutated(func(e: Array):
			e[2]["viseme"] = "jawdrop")],
		["non-positive duration rejected", func(): return _mutated(func(e: Array):
			e[0]["end"] = 0.0)],
		["SIL not rest rejected", func(): return _mutated(func(e: Array):
			e[3]["viseme"] = "open")],
		["bad speaker rejected", func(): return _mutated(func(e: Array):
			e[2]["speaker"] = "NARRATOR")],
		["unapproved 'But' rejected", func(): return _mutated(func(e: Array):
			e[0]["source_word"] = "But")],
		["missing required word rejected", func(): return _mutated(func(e: Array):
			e[8]["source_word"] = "toward")],
		["event beyond audio duration rejected", func(): return _mutated(func(e: Array):
			e[9]["end"] = 2.2)],
	]
	for case in cases:
		var timeline = case[1].call()
		_check(case[0], not timeline.is_valid(), timeline.validation_error)


func _mutated(mutator: Callable):
	var events: Array = _base_events()
	events[9]["end"] = 2.0  # keep the last event inside the 2.0 s duration for mutations
	mutator.call(events)
	return HolosTimelineScript.from_dictionary({"events": events}, 2.0)


func _test_state_at() -> void:
	var timeline = HolosTimelineScript.from_dictionary({"events": _base_events()}, 3.0)
	if not timeline.is_valid():
		_check("state_at precondition: valid timeline", false, timeline.validation_error)
		return
	var s: Dictionary
	s = timeline.state_at(0.05, "KEVIN")
	_check("inside event: active with event viseme", s["active"] and s["viseme"] == "wide")
	s = timeline.state_at(0.25, "KEVIN")
	_check("inside acoustic gap: rest", not s["active"] and s["viseme"] == "rest")
	s = timeline.state_at(0.4, "KHALED")
	_check("speaker filter: KHALED event found", s["active"] and s["viseme"] == "closed")
	s = timeline.state_at(0.55, "KHALED")
	_check("SIL event: rest viseme", s["active"] and s["viseme"] == "rest")
	s = timeline.state_at(0.05, "KHALED")
	_check("wrong speaker: rest before their first event", not s["active"])
	s = timeline.state_at(5.0, "KEVIN")
	_check("after last event: rest", not s["active"])
	s = timeline.state_at(-0.5, "KEVIN")
	_check("before first event: rest", not s["active"])
	_check("viseme_at convenience matches", timeline.viseme_at(0.7, "KHALED") == "open")


func _test_handoff_timelines() -> void:
	var repo_root := ProjectSettings.globalize_path("res://").path_join("..").simplify_path()
	var absolute_path := repo_root.path_join("handoffs/milestone-5-1-2026-11-15/HOLOS_Milestone51_WhisperX_Acoustic_Phoneme_Timeline_Aligned.json")
	var relative_path := repo_root.path_join("handoffs/milestone-5-1-2026-11-15/HOLOS_Milestone51_FourTurn_Review_Phoneme_Timeline_Relative.json")
	_check("absolute handoff timeline exists", FileAccess.file_exists(absolute_path), absolute_path)
	_check("relative handoff timeline exists", FileAccess.file_exists(relative_path), relative_path)
	if not FileAccess.file_exists(absolute_path) or not FileAccess.file_exists(relative_path):
		return
	var absolute_data = JSON.parse_string(FileAccess.get_file_as_string(absolute_path))
	var relative_data = JSON.parse_string(FileAccess.get_file_as_string(relative_path))
	_check("absolute handoff JSON parses", typeof(absolute_data) == TYPE_DICTIONARY)
	_check("relative handoff JSON parses", typeof(relative_data) == TYPE_DICTIONARY)
	if typeof(absolute_data) != TYPE_DICTIONARY or typeof(relative_data) != TYPE_DICTIONARY:
		return
	var absolute_timeline = HolosTimelineScript.from_dictionary(absolute_data, 914.880)
	var relative_timeline = HolosTimelineScript.from_dictionary(relative_data, 16.825)
	_check("absolute handoff timeline accepted", absolute_timeline.is_valid(), absolute_timeline.validation_error)
	_check("relative handoff timeline accepted", relative_timeline.is_valid(), relative_timeline.validation_error)
	_check("absolute event count is 189", absolute_timeline.events.size() == 189, str(absolute_timeline.events.size()))
	_check("relative event count is 189", relative_timeline.events.size() == 189, str(relative_timeline.events.size()))
	_check("both handoff timelines record two ASR normalizations",
		absolute_data.get("asr_normalizations", []).size() == 2
		and relative_data.get("asr_normalizations", []).size() == 2)
	var offset_mismatches := 0
	var absolute_events: Array = absolute_data.get("events", [])
	var relative_events: Array = relative_data.get("events", [])
	if absolute_events.size() == relative_events.size():
		for i in absolute_events.size():
			if abs(float(absolute_events[i]["start"]) - 0.091 - float(relative_events[i]["start"])) > 0.000001:
				offset_mismatches += 1
			if abs(float(absolute_events[i]["end"]) - 0.091 - float(relative_events[i]["end"])) > 0.000001:
				offset_mismatches += 1
	else:
		offset_mismatches = 1
	_check("relative event times use the documented 0.091 s offset", offset_mismatches == 0, str(offset_mismatches))
	_check("timeline source hashes agree",
		absolute_data.get("source_mp3_sha256", "") == relative_data.get("source_mp3_sha256", ""))
