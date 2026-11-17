class_name HolosEpisodeAudioTransport
extends Node
## Shared audio transport for future Episode 1 director/actor adapters.
##
## Attach one AudioStreamPlayer as the child named "DialoguePlayer" and assign
## its stream from the production scene. All actors must query this same
## transport; do not start independent clocks or advance viseme time with
## accumulated _process(delta).
##
## This is integration scaffolding only. It does not select a review WAV,
## provide actor rigs, or claim that production playback has been validated.

signal transport_started
signal transport_paused
signal transport_stopped
signal transport_seeked(position_seconds: float)

@export var dialogue_player_path: NodePath = ^"DialoguePlayer"
@export_range(0.0, 250.0, 1.0) var sync_tolerance_ms: float = 80.0

var _player: AudioStreamPlayer
var _has_started := false


func _ready() -> void:
	_player = get_node_or_null(dialogue_player_path) as AudioStreamPlayer
	if _player == null:
		push_error("HolosEpisodeAudioTransport requires an AudioStreamPlayer at %s" % dialogue_player_path)


func is_ready() -> bool:
	return _player != null and _player.stream != null


func play_from_start() -> void:
	if not is_ready():
		push_error("Cannot start HOLOS dialogue transport: player or stream is missing")
		return
	_player.stop()
	_player.play(0.0)
	_has_started = true
	transport_started.emit()


func pause_transport() -> void:
	if _player == null or not _player.playing:
		return
	_player.stream_paused = true
	transport_paused.emit()


func resume_transport() -> void:
	if _player == null or not _has_started or not _player.stream_paused:
		return
	_player.stream_paused = false
	transport_started.emit()


func stop_transport() -> void:
	if _player == null:
		return
	_player.stop()
	_has_started = false
	transport_stopped.emit()


func seek_transport(position_seconds: float) -> void:
	if _player == null or _player.stream == null:
		return
	var safe_position := maxf(0.0, position_seconds)
	_player.seek(safe_position)
	transport_seeked.emit(safe_position)


## Best available estimate of the shared playback position. Call this from
## every actor adapter in the same frame. AudioServer timing correction keeps
## the value tied to the active output mix rather than a separate delta clock.
func get_transport_seconds() -> float:
	if _player == null or not _has_started:
		return 0.0
	if _player.stream_paused:
		return _player.get_playback_position()
	return maxf(
		0.0,
		_player.get_playback_position()
		+ AudioServer.get_time_since_last_mix()
		- AudioServer.get_output_latency()
	)


func get_sync_tolerance_seconds() -> float:
	return sync_tolerance_ms / 1000.0


func is_playing() -> bool:
	return _player != null and _player.playing and not _player.stream_paused
