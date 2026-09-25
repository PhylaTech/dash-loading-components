/**
 * The common contract every dlc component honours on top of its upstream
 * props:
 *
 *   rate     relative tempo, 1.0 = this spinner's own tempo (what upstream
 *            does with its tempo prop left alone). Translated here into the
 *            family's native unit. Left undefined, upstream keeps its tempo.
 *   playing  false freezes the spinner where it is. Mapped to the family's
 *            own pause prop where it has one; the wrapper is also given a
 *            `dlc-paused` class that freezes CSS animations, and SMIL loaders
 *            are paused through usePlaying(). Never hides the spinner: the
 *            hide/show props (visible, loading, enabled) stay upstream's.
 *
 * A native tempo or play prop passed alongside wins: the caller asked for
 * that exact value.
 */

// The period each spinner runs at with its tempo prop omitted, i.e. what
// rate 1.0 must reproduce, in the family's native unit. Transcribed from:
//   loading-dev          SPINNER_MOTION (dist/motion.d.ts), ms
//   ldrs                 applyDefaultProps in dist/elements/<name>.js, seconds
//   react-epic-spinners  per-component animationDuration default, ms
//   premium-react-loaders  the "normal" token, 1s for every loader, ms
import {useEffect} from 'react';

const PERIOD = {
    loading_dev: {
        Arc: 800, Atom: 1000, Blocks: 1300, BouncingDots: 500, Cascade: 1500,
        CircularDots: 800, Classic: 1200, ClassicV2: 800, Clock: 1200, Comet: 700,
        Compass: 500, Dual: 1000, Eclipse: 1200, Flip: 1200, Gather: 1600,
        Leap: 1800, LinearDots: 900, Loading: 1000, Morph: 1200, Orbit: 750,
        Pulse: 1200, Radar: 1500, Ring: 800, Ripple: 1200, Slide: 2400,
        Snake: 1400, Swirl: 1200, Trace: 1200, Wave: 900,
    },
    ldrs: {
        DotPulse: 1.3, DotWave: 1.0, Helix: 2.5, Hourglass: 1.75, Infinity: 1.3,
        Jelly: 0.9, LineSpinner: 1.0, Mirage: 2.5, Orbit: 1.5, Ping: 2.0,
        Quantum: 1.75, Ring: 2.0,
    },
    epic: {
        AtomSpinner: 1000, FlowerSpinner: 2500, HollowDotsSpinner: 1000,
        OrbitSpinner: 1000, RadarSpinner: 2000, SemipolarSpinner: 2000,
        SpringSpinner: 3000, TrinityRingsSpinner: 1500,
    },
};
const PREMIUM_PERIOD = 1000;
// The one premium loader without `speed`: a one-shot draw timed by `duration`.
const CHECKMARK = {prop: 'duration', of: (rate) => 500 / rate};

// How each family spells tempo, and how `rate` maps onto it.
const TEMPO = {
    loading_dev: {prop: 'duration', of: (rate, spinner) => PERIOD.loading_dev[spinner] / rate},
    ldrs: {prop: 'speed', of: (rate, spinner) => PERIOD.ldrs[spinner] / rate},
    epic: {prop: 'animationDuration', of: (rate, spinner) => PERIOD.epic[spinner] / rate},
    premium: {prop: 'speed', of: (rate) => PREMIUM_PERIOD / rate},
    m3: {prop: 'speed', of: (rate) => rate},
    spinners: {prop: 'speedMultiplier', of: (rate) => rate},
    spinners_react: {prop: 'speed', of: (rate) => 100 * rate},
    // speedPlus is an integer offset in [-5, 5], 0 = normal.
    indicators: {prop: 'speedPlus', of: (rate) => Math.max(-5, Math.min(5, Math.round((rate - 1) * 5)))},
    loader_spinner: null,
};

// How each family spells "paused", where it has a word for it that pauses
// rather than unmounts.
const PLAY = {
    loading_dev: {prop: 'playState', of: (playing) => (playing ? 'running' : 'paused')},
    m3: {prop: 'paused', of: (playing) => !playing},
    spinners_react: {prop: 'still', of: (playing) => !playing},
};

// premium-react-loaders resolves its speed tokens to CSS times ("1s") and
// four loaders then parseInt that as milliseconds, so "normal" became a 1ms
// loop. Every loader reads a number correctly; hand it nothing else.
const PREMIUM_TOKEN_MS = {slow: 2000, normal: 1000, fast: 500};

export function premiumSpeed(speed) {
    return typeof speed === 'number' ? speed : PREMIUM_TOKEN_MS[speed] || PREMIUM_TOKEN_MS.normal;
}

/**
 * Native props implied by `rate` and `playing`, to spread onto the upstream
 * component after its explicit props. A native prop the caller set is
 * returned as-is so it wins.
 */
export function contract(family, spinner, props) {
    const out = {};
    const tempo = family === 'premium' && spinner === 'SuccessCheckmark' ? CHECKMARK : TEMPO[family];
    if (tempo) {
        if (props[tempo.prop] !== undefined) {
            out[tempo.prop] = props[tempo.prop];
        } else if (props.rate !== undefined && props.rate !== null) {
            out[tempo.prop] = tempo.of(props.rate, spinner);
        }
    }
    const play = PLAY[family];
    if (play) {
        if (props[play.prop] !== undefined) {
            out[play.prop] = props[play.prop];
        } else if (props.playing !== undefined && props.playing !== null) {
            out[play.prop] = play.of(props.playing);
        }
    }
    if (family === 'premium' && tempo !== CHECKMARK) {
        // Always a number: with nothing set, upstream's own "normal" token
        // would hit the parseInt bug below.
        out.speed = premiumSpeed(out.speed);
    }
    return out;
}

/**
 * Pause/resume SMIL animations under `ref` (react-loader-spinner animates
 * with <animate>, which CSS cannot freeze).
 */
export function usePlaying(ref, playing) {
    useEffect(() => {
        if (!ref.current) return;
        ref.current.querySelectorAll('svg').forEach((svg) => {
            if (playing === false) svg.pauseAnimations(); else svg.unpauseAnimations();
        });
    });
}

/** Wrapper class list: the caller's plus `dlc-paused` while not playing. */
export function wrapperClass(className, playing) {
    return [className, playing === false ? 'dlc-paused' : ''].filter(Boolean).join(' ') || undefined;
}

// One stylesheet for the pause class, injected once. Covers families with no
// pause prop of their own (ldrs, react-loading-indicators, react-epic-spinners).
if (typeof document !== 'undefined' && !document.getElementById('dlc-contract-style')) {
    const style = document.createElement('style');
    style.id = 'dlc-contract-style';
    style.textContent = '.dlc-paused, .dlc-paused *, .dlc-paused *::before, .dlc-paused *::after { animation-play-state: paused !important; }';
    document.head.appendChild(style);
}
