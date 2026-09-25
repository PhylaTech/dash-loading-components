import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import { FlickerSpinner as Upstream, DOT_R, OFFSET, PITCH, SIZE_FULL, VIEWBOX_FULL } from 'flicker-dot';

const ROWS = 7;
// Unlit dots are the on color at this opacity unless told otherwise.
const OFF_OPACITY = 0.16;
const CELLS = ROWS * ROWS;

/**
 * Upstream wants each frame as 49 booleans. Python is friendlier with rows,
 * so a frame may also be 7 lists of 7 or 7 strings with '#' for a lit dot.
 * Anything else returns null: upstream would throw on it.
 */
/** `base` at `opacity` (clamped to 0-1), as a CSS color. */
function withOpacity(base, opacity) {
    const alpha = Math.min(1, Math.max(0, opacity));
    return alpha === 1 ? base : `color-mix(in srgb, ${base} ${Number((alpha * 100).toFixed(1))}%, transparent)`;
}

function toFrames(grids) {
    if (!Array.isArray(grids) || !grids.length) {
        return null;
    }
    const frames = grids.map((frame) => {
        if (!Array.isArray(frame)) {
            return null;
        }
        const cells = frame.length === ROWS
            ? frame.flatMap((row) => (typeof row === 'string' ? [...row].map((ch) => ch === '#') : row))
            : frame;
        return Array.isArray(cells) && cells.length === CELLS ? cells.map(Boolean) : null;
    });
    return frames.every(Boolean) ? frames : null;
}

// 9x9 is the 7x7 with one more ring of unlit dots round it: same pitch and
// radius as upstream's grid, so the dots come out smaller at the same size.
const PADDED = VIEWBOX_FULL + 2 * PITCH;
const RING = [];
for (let r = 0; r < ROWS + 2; r++) {
    for (let c = 0; c < ROWS + 2; c++) {
        if (r % (ROWS + 1) === 0 || c % (ROWS + 1) === 0) {
            RING.push([OFFSET + PITCH * c, OFFSET + PITCH * r]);
        }
    }
}

/**
 * FlickerSpinner — Dash wrapper for flicker-dot's player. The named presets
 * in dlc.flicker are this component with their frames filled in.
 */
const FlickerSpinner = (props) => {
    const {id, className, style, grids, size, color, on_opacity, off_color, off_opacity, variant, reverse, speed, aria_label, playing} = props;
    const frames = toFrames(grids);
    if (!frames) {
        // eslint-disable-next-line no-console
        console.error('dlc.flicker.Spinner: grids must be a non-empty list of frames, each 49 values, 7 rows of 7, or 7 strings of 7.');
    }
    // Lit dots are `color` at on_opacity; unlit dots are off_color (default
    // `color`) at off_opacity rather than upstream's fixed light grey, so one
    // `color` reads on light and dark pages alike.
    const base = color || 'currentColor';
    const on = withOpacity(base, on_opacity ?? 1);
    const off = withOpacity(off_color || base, off_opacity ?? OFF_OPACITY);
    const padded = variant === '9x9';
    const player = frames && (
        <Upstream grids={frames} size={padded ? VIEWBOX_FULL : size} onColor={on} offColor={off}
            variant={padded ? '7x7' : variant} reverse={reverse} speed={speed} title={aria_label}
            playing={playing} style={{display: 'block'}} {...contract('flicker', 'Spinner', props)} />
    );
    const px = size ?? SIZE_FULL;
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            {player && padded ? (
                <svg width={px} height={px} viewBox={`0 0 ${PADDED} ${PADDED}`} role="presentation"
                    style={{display: 'block'}}>
                    {RING.map(([cx, cy]) => <circle key={`${cx},${cy}`} cx={cx} cy={cy} r={DOT_R} fill={off} />)}
                    <g transform={`translate(${PITCH} ${PITCH})`}>{player}</g>
                </svg>
            ) : player}
        </div>
    );
};

FlickerSpinner.defaultProps = {};

FlickerSpinner.propTypes = {
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
     * The frames to play, in order, one every 150ms at rate 1.0. Each frame
     * is the 7x7 grid as 49 values, as 7 rows of 7, or as 7 strings of 7
     * characters where '#' is a lit dot. The named presets fill this in.
     */
    grids: PropTypes.arrayOf(
        PropTypes.arrayOf(
            PropTypes.oneOfType([PropTypes.bool, PropTypes.number, PropTypes.string, PropTypes.array])
        )
    ).isRequired,
    /**
     * CSS pixel size (default 28, or 16 for the 5x5 variant).
     */
    size: PropTypes.number,
    /**
     * Color of a lit dot (default currentColor).
     */
    color: PropTypes.string,
    /**
     * Opacity of the lit dots, 0 to 1 (default 1).
     */
    on_opacity: PropTypes.number,
    /**
     * Color of an unlit dot, drawn at `off_opacity` (default `color`).
     */
    off_color: PropTypes.string,
    /**
     * Opacity of the unlit dots, 0 to 1 (default 0.16). 0 leaves only the
     * lit dots; 1 paints `off_color` solid.
     */
    off_opacity: PropTypes.number,
    /**
     * The grid: the full 7x7, its inner 5x5 (bigger dots), or the 7x7 padded
     * to 9x9 with a ring of unlit dots (smaller dots).
     */
    variant: PropTypes.oneOf(['7x7', '5x5', '9x9']),
    /**
     * Play the frames backwards.
     */
    reverse: PropTypes.bool,
    /**
     * Playback multiplier: 2 plays twice as fast.
     */
    speed: PropTypes.number,
    /**
     * Accessible name, announced to assistive technology (default "Loading").
     */
    aria_label: PropTypes.string,
    /**
     * Relative tempo: 1.0 is this spinner's own tempo, 2.0 twice as fast,
     * 0.5 half. Leave unset to keep the upstream tempo.
     */
    rate: PropTypes.number,
    /**
     * Set to False to pause the animation.
     */
    playing: PropTypes.bool,
};

export default FlickerSpinner;
