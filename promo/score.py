"""Synthesized 30s score for the PJT Park Hill promo. Hits are locked to the video's scene cuts."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
import wave

SR = 48000
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(3)
L = np.zeros(N); R = np.zeros(N)

CUTS = [3.3, 8.3, 10.3, 12.9, 15.4, 18.5, 24.6]
T0, BEAT = 3.3, 0.5            # 120 BPM grid anchored on the first cut
BAR = 4 * BEAT


def hz(n):  # midi -> Hz
    return 440 * 2 ** ((n - 69) / 12)


def add(sig, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def env_adsr(n, a, d, s, r):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    sus = max(0, n - a - d - r)
    return np.concatenate([np.linspace(0, 1, a, False), np.linspace(1, s, d, False),
                           np.full(sus, s), np.linspace(s, 0, r)])[:n]


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'low', fs=SR, output='sos'), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'high', fs=SR, output='sos'), x)


def saw(f, n, detune=0.0):
    t = np.arange(n) / SR
    ph = (f * (1 + detune) * t + rng.random()) % 1
    return 2 * ph - 1


# ---------- instruments ----------
def pad(notes, dur, bright=1200):
    n = int(dur * SR); x = np.zeros(n)
    for m in notes:
        for d in (-0.006, 0, 0.007):
            x += saw(hz(m), n, d)
    x = lp(x / (3 * len(notes)), bright, 2)
    return x * env_adsr(n, 0.6, 0.4, 0.8, 0.9)


def pluck(m, dur=0.45, bright=3000):
    n = int(dur * SR); t = np.arange(n) / SR
    x = saw(hz(m), n) * 0.6 + np.sin(2 * np.pi * hz(m) * t) * 0.6
    x = lp(x, bright, 2)
    return x * np.exp(-t * 9) * np.minimum(1, t * 400)


def bell(m, dur=2.5):
    n = int(dur * SR); t = np.arange(n) / SR; f = hz(m)
    x = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3)
         + 0.25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 6))
    return x * np.exp(-t * 1.6) * np.minimum(1, t * 800)


def kick(g=1.0):
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 42 + 90 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(2.2 * np.sin(ph) * np.exp(-t * 7)) * g


def hat(open_=False):
    n = int((0.25 if open_ else 0.06) * SR); t = np.arange(n) / SR
    x = hp(rng.standard_normal(n), 7000, 4)
    return x * np.exp(-t * (14 if open_ else 70))


def impact(big=1.0):
    n = int(4.0 * SR); t = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t * 6)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.1)
    noise = lp(rng.standard_normal(n), 900) * np.exp(-t * 5) * 0.9
    crack = hp(rng.standard_normal(n), 2500) * np.exp(-t * 25) * 0.35
    return np.tanh((sub * 1.3 + noise + crack) * big)


def riser(dur, start_fc=300, end_fc=9000):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    # piecewise sweep of a bandpass-ish filter
    out = np.zeros(n); seg = int(0.05 * SR)
    for i in range(0, n, seg):
        p = i / n
        fc = start_fc * (end_fc / start_fc) ** p
        blk = x[max(0, i - 2048):i + seg]
        y = sosfilt(butter(2, [fc * 0.6, min(fc * 1.6, SR / 2 - 100)], 'band', fs=SR, output='sos'), blk)
        out[i:i + seg] = y[-len(out[i:i + seg]):]
    tone = np.sin(2 * np.pi * np.cumsum(hz(50) * 2 ** (3 * t / dur)) / SR) * 0.25
    return (out * 2 + tone) * (t / dur) ** 2.2


def whoosh(dur=0.9):
    n = int(dur * SR); t = np.arange(n) / SR
    x = lp(rng.standard_normal(n), 2500)
    return x * np.sin(np.pi * t / dur) ** 2


def tick():
    n = int(0.03 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 200)


# ---------- arrangement ----------
# intro drone + word bells
add(pad([38, 45, 50], 3.9, 600), 0.0, gain=0.55)
for t, m in [(0.55, 74), (1.17, 77), (1.79, 81)]:
    add(bell(m), t, pan=[-0.4, 0, 0.4][[74, 77, 81].index(m)], gain=0.22)
add(riser(1.0, 400, 6000), 2.3, gain=0.18)

# chord progression per bar: Dm, Bb, F, C (with bass root)
prog = [([50, 53, 57, 62], 38), ([46, 50, 53, 58], 34), ([45, 48, 53, 57], 41), ([43, 48, 52, 55], 36)]
bar_i = 0
t = T0
while t < 24.6 - 0.01:
    chord, root = prog[bar_i % 4]
    dur = min(BAR, 24.6 - t)
    section = 0 if t < 8.3 else 1 if t < 18.5 else 2
    add(pad(chord, dur + 0.8, [900, 1600, 2400][section]), t, gain=[0.35, 0.42, 0.5][section])
    # bass: 8ths pumping
    for k in range(8):
        tt = t + k * BEAT / 2
        if tt >= 24.45: break
        n = int(0.24 * SR); tb = np.arange(n) / SR
        b = lp(saw(hz(root), n), 400) * np.exp(-tb * 6)
        add(b, tt, gain=0.5 if section else 0.35)
    # arpeggio plucks (16ths from section 1)
    arp = chord + [chord[1] + 12, chord[2] + 12]
    step = BEAT / 2 if section == 0 else BEAT / 4
    k = 0
    while k * step < dur - 0.01:
        tt = t + k * step
        if tt >= 24.45: break
        m = arp[k % len(arp)] + 12
        add(pluck(m, bright=2200 + 1500 * section), tt, pan=0.35 * np.sin(k * 0.9), gain=0.16)
        k += 1
    # drums
    for b in range(4):
        tt = t + b * BEAT
        if tt >= 24.45: break
        add(kick(), tt, gain=0.55 if section else 0.4)
        if section >= 1:
            for s in range(2):
                add(hat(), tt + BEAT / 2 * s + BEAT / 4, pan=0.25, gain=0.12)
            if b % 2 == 1: add(hat(True), tt, pan=-0.2, gain=0.08)
    t += BAR; bar_i += 1

# impacts on scene cuts
for c in CUTS[:-1]:
    add(impact(0.9 if c in (3.3, 8.3, 18.5) else 0.6), c, gain=0.55 if c in (3.3, 8.3, 18.5) else 0.35)
    add(whoosh(0.8), c - 0.6, gain=0.25)

# counter ticks during stat count-ups
for a, b in [(10.35, 12.0), (13.0, 14.4), (15.5, 16.9)]:
    tt = a
    while tt < b:
        add(tick(), tt, pan=0.1, gain=0.07 * (1 - (tt - a) / (b - a)) + 0.02)
        tt += 0.05 + 0.12 * ((tt - a) / (b - a)) ** 2

# globe: shimmering bells on city pins
for tt, m in [(19.0, 74), (19.6, 76), (19.9, 81), (20.1, 79), (21.3, 86), (21.8, 81)]:
    add(bell(m, 2.0), tt, pan=float(rng.uniform(-.6, .6)), gain=0.14)

# final riser + drop-out + finale
add(riser(1.6, 250, 11000), 23.0, gain=0.35)
fin = 24.6
add(impact(1.2), fin, gain=0.8)
add(pad([38, 45, 50, 54, 57, 64], 5.4, 2600), fin, gain=0.6)  # D major (add9) — lift on the resolve
add(bell(86, 4), fin + 1.0, gain=0.18)          # "Raise with conviction." sweep
add(bell(81, 4), fin + 1.03, pan=-0.3, gain=0.12)
add(bell(90, 3), fin + 1.7, pan=0.3, gain=0.1)

# ---------- master ----------
mix = np.stack([L, R])
# plate-ish reverb: decaying stereo noise IR
ir_n = int(2.6 * SR); ti = np.arange(ir_n) / SR
irs = [lp(rng.standard_normal(ir_n), 5000) * np.exp(-ti * 2.6) for _ in range(2)]
wet = np.stack([fftconvolve(mix[i], irs[i])[:N] for i in range(2)])
wet /= np.abs(wet).max() + 1e-9
dry = mix / (np.abs(mix).max() + 1e-9)
out = dry * 0.85 + wet * 0.28
out = hp(out, 28)
# glue: soft saturation + fades
out = np.tanh(out * 1.6) / np.tanh(1.6)
fade = np.ones(N)
fi = int(0.25 * SR); fo = int(2.2 * SR)
fade[:fi] = np.linspace(0, 1, fi)
fade[-fo:] = np.linspace(1, 0, fo) ** 1.5
out *= fade
out = out / np.abs(out).max() * 0.89  # ~ -1 dBFS peak

pcm = (out.T * 32767).astype('<i2')
with wave.open('score.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('wrote score.wav', out.shape)
