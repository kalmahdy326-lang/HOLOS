class_name HolosTimeline
extends RefCounted
## Deterministic consumer for HOLOS phoneme/viseme timelines.
##
## Loads and validates the JSON timeline committed by
## tools/process_holos_aligned_audio_v2.py, then answers one question:
## given an absolute time in seconds and a speaker, which viseme is active?
##
## state_at() is a pure function of time. It never reads the wall clock and
## never advances state on its own. This is what makes the timeline usable
## from the deterministic headless runner (holos_set_frame), where frame
## state must not depend on accumulated wall-clock delta. A real-time
## transport clock, if a rig needs one, belongs in that rig's adapter, not
## here.
##
## Validation mirrors the Python gate in the processor script (speakers,
## supported visemes, chronology, positive durations, SIL -> rest, no
## unapproved "But", required approved words). A timeline that failed the
## Python gate must also fail here; this class is defence in depth, not the
## authority. The audio-duration check is applied only when the caller
## supplies a measured duration, because the committed JSON does not carry
## one.

const SUPPORTED_VISEMES: Array[String] = ["rest", "closed", "open", "wide", "round", "teeth"]
const VALID_SPEAKERS: Array[String] = ["KEVIN", "KHALED"]
const CHRONOLOGY_EPSILON := 1e-6
const DURATION_EPSILON := 0.05
const REQUIRED_WORDS: Array[String] = [
	"tell", "interesting", "380,000", "kilometres", "away", "from", "you",
]

var validation_error: String = ""
var events: Array[Dictionary] = []
var _by_speaker: Dictionary = {}


static func from_file(path: String, audio_duration: float = -1.0) -> HolosTimeline:
	var timeline := HolosTimeline.new()
	if not FileAccess.file_exists(path):
		timeline.validation_error = "Timeline file not found: %s" % path
		return timeline
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		timeline.validation_error = "Timeline must be a JSON object."
		return timeline
	timeline._load(parsed, audio_duration)
	return timeline


static func from_dictionary(data: Dictionary, audio_duration: float = -1.0) -> HolosTimeline:
	var timeline := HolosTimeline.new()
	timeline._load(data, audio_duration)
	return timeline


func is_valid() -> bool:
	return validation_error.is_empty()


func _load(data: Dictionary, audio_duration: float) -> void:
	var raw_events = data.get("events", [])
	if typeof(raw_events) != TYPE_ARRAY or (raw_events as Array).is_empty():
		validation_error = "Timeline validation failed: no events"
		return
	var previous_start := -1.0
	var source_words: PackedStringArray = []
	for i in (raw_events as Array).size():
		var event: Variant = raw_events[i]
		var error := _validate_event(event, i, previous_start, audio_duration)
		if not error.is_empty():
			validation_error = error
			return
		previous_start = float(event["start"])
		var source_word: Variant = event.get("source_word")
		if source_word != null:
			source_words.append(str(source_word))
		events.append(event as Dictionary)
	var words := " ".join(source_words).to_lower()
	var but_regex := RegEx.new()
	but_regex.compile("\\bbut\\b")
	if but_regex.search(words) != null:
		validation_error = "Timeline validation failed: unapproved leading 'But' present"
		return
	for required in REQUIRED_WORDS:
		if not words.contains(required) and not words.contains(required.replace(",", "")):
			validation_error = "Timeline validation failed: missing approved word '%s'" % required
			return
	for speaker in VALID_SPEAKERS:
		var list: Array[Dictionary] = []
		for event in events:
			if str(event["speaker"]) == speaker:
				list.append(event)
		_by_speaker[speaker] = list


func _validate_event(event: Variant, index: int, previous_start: float, audio_duration: float) -> String:
	if typeof(event) != TYPE_DICTIONARY:
		return "Timeline validation failed at event %d: not an object" % index
	var speaker: Variant = event.get("speaker")
	if typeof(speaker) != TYPE_STRING or not VALID_SPEAKERS.has(speaker):
		return "Timeline validation failed at event %d: speaker %s" % [index, str(speaker)]
	if not event.has("start") or not event.has("end"):
		return "Timeline validation failed at event %d: missing start/end" % index
	var start_value: Variant = event["start"]
	var end_value: Variant = event["end"]
	if (typeof(start_value) != TYPE_FLOAT and typeof(start_value) != TYPE_INT) \
			or (typeof(end_value) != TYPE_FLOAT and typeof(end_value) != TYPE_INT):
		return "Timeline validation failed at event %d: invalid start/end" % index
	var start := float(start_value)
	var end := float(end_value)
	if not is_finite(start) or not is_finite(end):
		return "Timeline validation failed at event %d: non-finite time" % index
	if start < 0.0 or end <= start:
		return "Timeline validation failed at event %d: non-positive duration" % index
	if start < previous_start - CHRONOLOGY_EPSILON:
		return "Timeline validation failed at event %d: out of order" % index
	var viseme: Variant = event.get("viseme")
	if typeof(viseme) != TYPE_STRING or not SUPPORTED_VISEMES.has(viseme):
		return "Timeline validation failed at event %d: viseme %s" % [index, str(viseme)]
	if str(event.get("phoneme", "")) == "SIL" and viseme != "rest":
		return "Timeline validation failed at event %d: SIL must map to rest" % index
	if audio_duration > 0.0 and end > audio_duration + DURATION_EPSILON:
		return "Timeline validation failed at event %d: end %f exceeds audio duration %f" % [
			index, end, audio_duration,
		]
	return ""


## Viseme active for a speaker at an absolute time. Convenience wrapper for
## state_at(). Returns "rest" outside every event and inside reviewed gaps.
func viseme_at(time_seconds: float, speaker: String) -> String:
	return state_at(time_seconds, speaker)["viseme"]


## Full active event state for a speaker at an absolute time. Pure function
## of time. Returns {active, viseme, phoneme, source_word, confidence}.
func state_at(time_seconds: float, speaker: String) -> Dictionary:
	var inactive := {
		"active": false,
		"viseme": "rest",
		"phoneme": "SIL",
		"source_word": "",
		"confidence": 0.0,
	}
	var list: Array = _by_speaker.get(speaker, [])
	# Binary search: last event of this speaker with start <= time_seconds.
	var low := 0
	var high: int = list.size() - 1
	var candidate := -1
	while low <= high:
		var mid := (low + high) >> 1
		if float(list[mid]["start"]) <= time_seconds:
			candidate = mid
			low = mid + 1
		else:
			high = mid - 1
	if candidate < 0:
		return inactive
	var event: Dictionary = list[candidate]
	if time_seconds >= float(event["end"]):
		return inactive  # Inside a reviewed acoustic gap: mouth at rest.
	return {
		"active": true,
		"viseme": str(event["viseme"]),
		"phoneme": str(event.get("phoneme", "")),
		"source_word": str(event.get("source_word", "")),
		"confidence": float(event.get("confidence", 0.0)),
	}
