import io
import wave
import numpy as np

# Pentatonic & Harmonic Scale Frequencies (Hz) for pleasant musical sonification
SCALES = {
    "C Major Pentatonic (Cosmic Harmony)": [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25, 783.99, 880.00],
    "A Minor Ambient (Deep Earth)": [220.00, 261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25, 783.99],
    "Lydian Space Synth (Orbital)": [261.63, 293.66, 329.63, 369.99, 392.00, 440.00, 493.88, 523.25, 587.33, 659.25],
    "Continuous Frequency Sweep (Telemetry)": None
}

def generate_jukebox_audio(values, scale_name="C Major Pentatonic (Cosmic Harmony)", note_duration=0.18, sample_rate=44100):
    """
    Converts a 1D array of Earth science telemetry values into a synthesized WAV audio stream
    for 'The Earth Information Jukebox'.
    """
    vals = np.array(values, dtype=float)
    v_min, v_max = np.min(vals), np.max(vals)
    if v_max - v_min == 0:
        norm = np.zeros_like(vals)
    else:
        norm = (vals - v_min) / (v_max - v_min)

    scale = SCALES.get(scale_name)
    audio_segments = []
    t_note = np.linspace(0, note_duration, int(sample_rate * note_duration), endpoint=False)

    # Smooth ADSR-like envelope to prevent clicks
    fade_len = int(sample_rate * 0.025)
    envelope = np.ones_like(t_note)
    if len(envelope) > 2 * fade_len:
        envelope[:fade_len] = np.linspace(0, 1, fade_len)
        envelope[-fade_len:] = np.linspace(1, 0, fade_len)

    for idx, n_val in enumerate(norm):
        if scale is None:
            freq = 220.0 + n_val * 660.0
        else:
            note_idx = int(round(n_val * (len(scale) - 1)))
            freq = scale[note_idx]

        # Rich additive synthesis (Fundamental + Octave + Fifth harmonic)
        wave_data = (
            0.60 * np.sin(2 * np.pi * freq * t_note) +
            0.25 * np.sin(2 * np.pi * (freq * 2.0) * t_note) +
            0.15 * np.sin(2 * np.pi * (freq * 1.5) * t_note)
        )
        wave_data *= envelope
        audio_segments.append(wave_data)

    full_wave = np.concatenate(audio_segments)
    # Normalize to 16-bit PCM
    max_amp = np.max(np.abs(full_wave))
    if max_amp > 0:
        full_wave = full_wave / max_amp * 0.85
    pcm_data = (full_wave * 32767).astype(np.int16)

    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_data.tobytes())

    wav_buffer.seek(0)
    return wav_buffer.read()
