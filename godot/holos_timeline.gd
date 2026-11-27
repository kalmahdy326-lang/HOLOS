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
## Validation mirrors the Python gate for structure and, when present,
## speaker-tagged words in approved_transcript. Legacy fixture documents with
## no approved_transcript retain the opening-exchange safeguards. Canonical
## full-episode cast IDs are provisional until the original screenplay is
## confirmed. The audio-duration check is applied only when supplied.

const SUPPORTED_VISEMES: Array[String] = ["rest", "closed", "open", "wide", "round", "teeth"]
const VALID_SPEAKERS: Array[String] = ["KEVIN", "KHALED", "ORBIT", "THE_MOON"]
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
	if data.has("schema_version") and data.get("schema_version") != 1:
		validation_error = "Timeline validation failed: unsupported schema_version"
		return
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
	if data.has("approved_transcript"):
		var expected_pairs := _approved_word_speaker_pairs(data["approved_transcript"])
		if not validation_error.is_empty():
			return
		var observed_pairs := _event_word_speaker_pairs(raw_events as Array)
		if observed_pairs != expected_pairs:
			var mismatch := 0
			while mismatch < mini(observed_pairs.size(), expected_pairs.size()) and observed_pairs[mismatch] == expected_pairs[mismatch]:
				mismatch += 1
			var observed_context: Array = observed_pairs.slice(mismatch, mini(mismatch + 3, observed_pairs.size()))
			var expected_context: Array = expected_pairs.slice(mismatch, mini(mismatch + 3, expected_pairs.size()))
			validation_error = "Timeline validation failed: approved_transcript mismatch at token %d (observed %d, expected %d): %s vs %s" % [
				mismatch, observed_pairs.size(), expected_pairs.size(), str(observed_context), str(expected_context),
			]
			return
	else:
		# Opening-only fixtures predate canonical transcript metadata.
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


func _normalize_speaker(value: String) -> String:
	var normalized := " ".join(value.strip_edges().to_upper().replace("_", " ").split(" ", false))
	return "THE_MOON" if normalized == "THE MOON" else normalized


func _word_tokens(text: String) -> Array[String]:
	var result: Array[String] = []
	var normalized := text.to_lower().replace("’", "'")
	var regex := RegEx.new()
	regex.compile("\\d{1,3}(?:,\\d{3})+|[A-Za-z]+(?:'[A-Za-z]+)?|\\d+")
	for item in regex.search_all(normalized):
		result.append(item.get_string().replace(",", ""))
	return result


func _approved_word_speaker_pairs(transcript: Variant) -> Array:
	var pairs: Array = []
	if typeof(transcript) != TYPE_ARRAY:
		validation_error = "Timeline validation failed: approved_transcript must be an array"
		return pairs
	for turn in transcript as Array:
		if typeof(turn) != TYPE_DICTIONARY or not turn.has("speaker") or not turn.has("text"):
			validation_error = "Timeline validation failed: malformed approved_transcript turn"
			return []
		var speaker := _normalize_speaker(str(turn["speaker"]))
		if not VALID_SPEAKERS.has(speaker):
			validation_error = "Timeline validation failed: unsupported transcript speaker %s" % speaker
			return []
		for token in _word_tokens(str(turn["text"])):
			pairs.append([speaker, token])
	return pairs


func _event_word_speaker_pairs(raw_events: Array) -> Array:
	var pairs: Array = []
	var previous_acoustic_key := ""
	var previous_speaker := ""
	var previous_word := ""
	for raw_event in raw_events:
		var event: Dictionary = raw_event
		var source_word: Variant = event.get("source_word")
		if source_word == null:
			previous_acoustic_key = ""
			previous_speaker = ""
			previous_word = ""
			continue
		var speaker := _normalize_speaker(str(event.get("speaker", "")))
		var acoustic_key := ""
		if event.has("acoustic_word_start") and event.has("acoustic_word_end"):
			acoustic_key = "%s|%s" % [str(event["acoustic_word_start"]), str(event["acoustic_word_end"])]
		if not acoustic_key.is_empty() and acoustic_key == previous_acoustic_key:
			if speaker != previous_speaker:
				validation_error = "Timeline validation failed: speaker changes inside one acoustic word"
				return []
			if str(source_word).to_lower() != previous_word.to_lower():
				validation_error = "Timeline validation failed: source_word changes inside one acoustic word"
				return []
			continue
		for token in _word_tokens(str(source_word)):
			pairs.append([speaker, token])
		previous_acoustic_key = acoustic_key
		previous_speaker = speaker
		previous_word = str(source_word)
	return pairs


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
