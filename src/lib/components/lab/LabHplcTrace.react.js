import React from 'react';
import PropTypes from 'prop-types';
import {wrapperClass} from '../../contract';

const W = 160;
const H = 100;
const LEFT = 12;
const RIGHT = 152;
const BASELINE = 80;
const AXIS = 86;
const TOP = 10;
const SAMPLES = 320;
const TICKS = 7;
// Ticks on the signal axis: the baseline, then quarters of the chart's height.
const SIGNAL_TICKS = 4;
const TICK_LENGTH = 3;
const DEFAULT_SIZE = 64;
const AXIS_OPACITY = 0.5;

// What elutes, by retention time (0 to 1 along the run), height (0 to 1 of the
// chart) and width. Real peaks tail: they fall away slower than they rise.
const PEAKS = [
    {rt: 0.05, height: 0.22, width: 0.010},
    {rt: 0.22, height: 0.42, width: 0.014},
    {rt: 0.38, height: 1.0, width: 0.016},
    {rt: 0.55, height: 0.62, width: 0.018},
    {rt: 0.72, height: 0.85, width: 0.013},
    {rt: 0.88, height: 0.3, width: 0.02},
];
const TAIL = 1.7;

// One loop at rate 1.0: the pen draws the run, the apex of each peak is marked
// as it passes, the finished trace stands, and then it wipes away from the
// left as the next injection goes in.
const PERIOD = 7;
const DRAW = 0.7;
const HOLD = 0.86;
const MARK_POP = 0.02;

const signal = (t) => PEAKS.reduce((sum, {rt, height, width}) => {
    const w = t > rt ? width * TAIL : width;
    return sum + height * Math.exp(-(((t - rt) / w) ** 2) / 2);
}, 0);

const xAt = (t) => LEFT + t * (RIGHT - LEFT);
const yAt = (v) => BASELINE - v * (BASELINE - TOP);

const POINTS = Array.from({length: SAMPLES + 1}, (_, i) => {
    const t = i / SAMPLES;
    return [xAt(t), yAt(signal(t))];
});

const TRACE = POINTS.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(2)} ${y.toFixed(2)}`).join('');

// The pen and the draw-on both travel the path by length, not by x: a tall peak
// adds length, so the pen reaches a late apex later than its place on the time
// axis suggests. Marks are timed by how far along the path each apex is.
const LENGTH_TO = POINTS.reduce((sums, [x, y], i) => {
    sums.push(i ? sums[i - 1] + Math.hypot(x - POINTS[i - 1][0], y - POINTS[i - 1][1]) : 0);
    return sums;
}, []);
const progressAt = (t) => LENGTH_TO[Math.round(t * SAMPLES)] / LENGTH_TO[SAMPLES];

const pct = (fraction) => Number((fraction * 100).toFixed(3));

const marks = PEAKS.map(({rt}, k) => {
    const seen = progressAt(rt) * DRAW;
    return `@keyframes dlc-hplc-mark-${k}{
0%,${pct(seen)}%{opacity:0;transform:scale(0)}
${pct(seen + MARK_POP)}%{opacity:1;transform:scale(1.7)}
${pct(seen + 2 * MARK_POP)}%{opacity:1;transform:scale(1)}
${pct(HOLD)}%{opacity:1;transform:scale(1)}
100%{opacity:0;transform:scale(1)}}`;
}).join('');

const CSS = `
@keyframes dlc-hplc-draw{0%{stroke-dashoffset:1}${pct(DRAW)}%{stroke-dashoffset:0}${pct(HOLD)}%{stroke-dashoffset:0}100%{stroke-dashoffset:-1}}
@keyframes dlc-hplc-pen{0%{offset-distance:0%;opacity:1}${pct(DRAW)}%{offset-distance:100%;opacity:1}${pct(DRAW + MARK_POP)}%{offset-distance:100%;opacity:0}100%{offset-distance:100%;opacity:0}}
${marks}
.dlc-hplc-trace{stroke-dasharray:1;stroke-dashoffset:1}
.dlc-hplc-pen{opacity:0;offset-rotate:0deg}
.dlc-hplc-mark{opacity:0;transform:scale(0);transform-box:fill-box;transform-origin:center}
`;

if (typeof document !== 'undefined' && !document.getElementById('dlc-hplctrace-style')) {
    const style = document.createElement('style');
    style.id = 'dlc-hplctrace-style';
    style.textContent = CSS;
    document.head.appendChild(style);
}

// The axes run a little past the data.
const PAD = 4;
const AXIS_X = LEFT - PAD / 2;
const FRAME = `M${AXIS_X} ${TOP - PAD}V${AXIS}H${RIGHT + PAD}`;
const TIME_TICKS = Array.from({length: TICKS}, (_, i) => {
    const x = xAt((i + 0.5) / TICKS);
    return `M${x.toFixed(2)} ${AXIS}v${TICK_LENGTH}`;
}).join('');
const SIGNAL_TICK_MARKS = Array.from({length: SIGNAL_TICKS + 1}, (_, i) => {
    const y = yAt(i / SIGNAL_TICKS);
    return `M${AXIS_X} ${y.toFixed(2)}h-${TICK_LENGTH}`;
}).join('');
const TICK_MARKS = TIME_TICKS + SIGNAL_TICK_MARKS;

/**
 * LabHplcTrace — the detector trace of an HPLC or UPLC run, the kind that
 * feeds a mass spectrometer: a pen draws the baseline across the retention
 * time axis, compounds elute as peaks of their own height, and each apex is
 * marked as it passes. Drawn as SVG and CSS; dlc.flicker.HplcTrace is the
 * 7x7 dot-matrix take on it.
 */
const LabHplcTrace = (props) => {
    const {id, className, style, size, color, on_opacity, rate, playing, aria_label} = props;
    const speed = rate > 0 ? rate : 1;
    const run = `${PERIOD / speed}s linear infinite`;
    const base = color || 'currentColor';
    const on = on_opacity ?? 1;
    const px = size ?? DEFAULT_SIZE;
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            <svg width={px} height={(px * H) / W} viewBox={`0 0 ${W} ${H}`} role="img"
                aria-label={aria_label || 'Loading'} style={{display: 'block'}}>
                <path d={FRAME + TICK_MARKS} fill="none" stroke={base} strokeOpacity={AXIS_OPACITY} strokeWidth={1.2}
                    strokeLinecap="round" strokeLinejoin="round" />
                <path className="dlc-hplc-trace" d={TRACE} pathLength={1} fill="none" stroke={base} strokeOpacity={on}
                    strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" style={{animation: `dlc-hplc-draw ${run}`}} />
                {PEAKS.map(({rt}, k) => (
                    <circle key={rt} className="dlc-hplc-mark" cx={xAt(rt)} cy={yAt(signal(rt))} r={2.4}
                        fill={base} fillOpacity={on} style={{animation: `dlc-hplc-mark-${k} ${run}`}} />
                ))}
                <circle className="dlc-hplc-pen" r={3} fill={base} fillOpacity={on}
                    style={{offsetPath: `path('${TRACE}')`, animation: `dlc-hplc-pen ${run}`}} />
            </svg>
        </div>
    );
};

LabHplcTrace.defaultProps = {};

LabHplcTrace.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,
    /**
     * CSS class applied to the outer wrapper.
     */
    className: PropTypes.string,
    /**
     * Inline styles applied to the outer wrapper.
     */
    style: PropTypes.object,
    /**
     * CSS pixel width (default 64); the height follows the chart.
     */
    size: PropTypes.number,
    /**
     * Color of the trace, the pen and the axes (default currentColor).
     */
    color: PropTypes.string,
    /**
     * Opacity of the trace, 0 to 1 (default 1).
     */
    on_opacity: PropTypes.number,
    /**
     * Accessible name, announced to assistive technology (default "Loading").
     */
    aria_label: PropTypes.string,
    /**
     * Relative tempo: 1.0 is this spinner's own tempo (a run in 7 seconds),
     * 2.0 twice as fast, 0.5 half.
     */
    rate: PropTypes.number,
    /**
     * Set to False to pause the animation.
     */
    playing: PropTypes.bool,
};

export default LabHplcTrace;
