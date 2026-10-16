import React from 'react';
import PropTypes from 'prop-types';
import {wrapperClass} from '../../contract';

// A 96-well microplate to SBS proportions, in millimetres: 127.76 x 85.48 with
// wells on a 9mm pitch, A1 at top left and that corner cut off.
const ROWS = 8;
const COLS = 12;
const WELLS = ROWS * COLS;
const PITCH = 9;
const WELL_R = 3.2;
const PLATE_W = 127.8;
const PLATE_H = 85.5;
const FIRST_X = 14.4;
const FIRST_Y = 11.2;
const CHAMFER = 7;
const CORNER = 3;
// Headroom above the plate for the pipette head.
const HEAD = 14;
const VIEWBOX = `0 ${-HEAD} ${PLATE_W} ${PLATE_H + HEAD}`;
const DEFAULT_SIZE = 64;
const OFF_OPACITY = 0.16;
const PLATE_OPACITY = 0.5;
const HALO = 1.4;

// One loop at rate 1.0, on one clock for the whole plate: wells fill in plate
// order, one every STEP seconds, the plate stands full for HOLD, then empties
// in the same order, a well every DRAIN_STEP and each taking DRAIN seconds. The
// pipette is back at A1 only once the last well is empty and the plate has sat
// bare for a beat, so one plate is never filling while another empties.
const STEP = 0.09;
const HOLD = 1.2;
const DRAIN_STEP = 0.025;
const DRAIN = 0.5;
const BARE = 0.4;
const POP = 0.14;
// Where in the pop a well overshoots its full size.
const POP_PEAK = 0.6;
const FILLED_AT = WELLS * STEP;
const DRAINING_FROM = FILLED_AT + HOLD;
const PERIOD = DRAINING_FROM + (WELLS - 1) * DRAIN_STEP + DRAIN + BARE;

const pct = (seconds) => Number(((seconds / PERIOD) * 100).toFixed(3));
const at = (i) => [FIRST_X + (i % COLS) * PITCH, FIRST_Y + Math.floor(i / COLS) * PITCH];

// The pipette head sits over each well in turn (jumping, like a flip-dot), and
// is gone for the hold and the drain.
const HEAD_STOPS = Array.from({length: WELLS}, (_, i) => {
    const [x, y] = at(i);
    return `${pct(i * STEP)}%{transform:translate(${x}px,${y}px);opacity:1;animation-timing-function:step-end}`;
}).join('');

// Each well has its own keyframes on the shared clock: empty until the pipette
// gets to it, a pop to full, full until its turn to drain, then empty again.
const WELL_FILLS = Array.from({length: WELLS}, (_, i) => {
    const poured = i * STEP;
    const emptied = DRAINING_FROM + i * DRAIN_STEP;
    return `@keyframes dlc-wp-fill-${i}{
0%${poured ? `,${pct(poured)}%` : ''}{transform:scale(0)}
${pct(poured + POP * POP_PEAK)}%{transform:scale(1.25)}
${pct(poured + POP)}%,${pct(emptied)}%{transform:scale(1)}
${pct(emptied + DRAIN)}%,100%{transform:scale(0)}}`;
}).join('');

const CSS = `
${WELL_FILLS}
@keyframes dlc-wp-head{${HEAD_STOPS}${pct(FILLED_AT)}%{transform:translate(${at(WELLS - 1)[0]}px,${at(WELLS - 1)[1]}px);opacity:0;animation-timing-function:step-end}100%{opacity:0}}
.dlc-wp-liquid{transform-box:fill-box;transform-origin:center;transform:scale(0)}
.dlc-wp-head{opacity:0}
`;

if (typeof document !== 'undefined' && !document.getElementById('dlc-wellplate-style')) {
    const style = document.createElement('style');
    style.id = 'dlc-wellplate-style';
    style.textContent = CSS;
    document.head.appendChild(style);
}

// Plate outline with its A1 corner cut off.
const OUTLINE = `M${CHAMFER} 0H${PLATE_W - CORNER}a${CORNER} ${CORNER} 0 0 1 ${CORNER} ${CORNER}V${PLATE_H - CORNER}`
    + `a${CORNER} ${CORNER} 0 0 1 -${CORNER} ${CORNER}H${CORNER}a${CORNER} ${CORNER} 0 0 1 -${CORNER} -${CORNER}V${CHAMFER}Z`;

// A pipette: grip, shaft and tip, its point on the origin and so on the well
// it is filling.
const PIPETTE = 'M-2.4 -16H2.4V-9.5H1.3V-2.6L0.5 0H-0.5L-1.3 -2.6V-9.5H-2.4Z';

const WELL_CELLS = Array.from({length: WELLS}, (_, i) => at(i));

/**
 * LabWellPlate — a 96-well microplate (8 rows by 12 columns, A1 corner
 * cut off) that a pipette fills well by well, row after row, until it is full.
 * It then empties in the same order, and the pipette only comes back once every
 * well is empty. Drawn as SVG
 * and CSS; dlc.flicker.WellPlate is the 7x7 dot-matrix take on it.
 */
const LabWellPlate = (props) => {
    const {id, className, style, size, color, on_opacity, off_color, off_opacity, rate, playing, aria_label} = props;
    const speed = rate > 0 ? rate : 1;
    const period = PERIOD / speed;
    const base = color || 'currentColor';
    const px = size ?? DEFAULT_SIZE;
    const run = `${period}s linear infinite`;
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            <svg width={px} height={(px * (PLATE_H + HEAD)) / PLATE_W} viewBox={VIEWBOX} role="img"
                aria-label={aria_label || 'Loading'} style={{display: 'block'}}>
                <path d={OUTLINE} fill="none" stroke={base} strokeOpacity={PLATE_OPACITY} strokeWidth={1.2} />
                {WELL_CELLS.map(([cx, cy], i) => (
                    <g key={i}>
                        <circle cx={cx} cy={cy} r={WELL_R} fill={off_color || base} fillOpacity={off_opacity ?? OFF_OPACITY} />
                        <circle className="dlc-wp-liquid" cx={cx} cy={cy} r={WELL_R} fill={base} fillOpacity={on_opacity ?? 1}
                            style={{animation: `dlc-wp-fill-${i} ${run}`}} />
                    </g>
                ))}
                <g className="dlc-wp-head" style={{animation: `dlc-wp-head ${run}`}}>
                    {/* The halo is the page's own background, so the pipette stays readable over wells already full. */}
                    <path d={PIPETTE} fill={base} fillOpacity={on_opacity ?? 1} stroke="Canvas" strokeWidth={HALO}
                        strokeLinejoin="round" paintOrder="stroke" transform="translate(0 -3.6)" />
                </g>
            </svg>
        </div>
    );
};

LabWellPlate.defaultProps = {};

LabWellPlate.propTypes = {
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
     * CSS pixel width (default 64); the height follows the plate.
     */
    size: PropTypes.number,
    /**
     * Color of the liquid, the pipette and the plate outline (default currentColor).
     */
    color: PropTypes.string,
    /**
     * Opacity of the liquid, 0 to 1 (default 1).
     */
    on_opacity: PropTypes.number,
    /**
     * Color of an empty well, drawn at `off_opacity` (default `color`).
     */
    off_color: PropTypes.string,
    /**
     * Opacity of the empty wells, 0 to 1 (default 0.16).
     */
    off_opacity: PropTypes.number,
    /**
     * Accessible name, announced to assistive technology (default "Loading").
     */
    aria_label: PropTypes.string,
    /**
     * Relative tempo: 1.0 is this spinner's own tempo (a plate in about 13
     * seconds), 2.0 twice as fast, 0.5 half.
     */
    rate: PropTypes.number,
    /**
     * Set to False to pause the animation.
     */
    playing: PropTypes.bool,
};

export default LabWellPlate;
