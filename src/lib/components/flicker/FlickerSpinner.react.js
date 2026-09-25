import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import { FlickerSpinner as Upstream } from 'flicker-dot';

const ROWS = 7;
const CELLS = ROWS * ROWS;

/**
 * Upstream wants each frame as 49 booleans. Python is friendlier with rows,
 * so a frame may also be 7 lists of 7 or 7 strings with '#' for a lit dot.
 * Anything else returns null: upstream would throw on it.
 */
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

/**
 * FlickerSpinner — Dash wrapper for flicker-dot's player. The named presets
 * in dlc.flicker are this component with their frames filled in.
 */
const FlickerSpinner = (props) => {
    const {id, className, style, grids, size, color, off_color, variant, reverse, speed, aria_label, playing} = props;
    const frames = toFrames(grids);
    if (!frames) {
        // eslint-disable-next-line no-console
        console.error('dlc.flicker.Spinner: grids must be a non-empty list of frames, each 49 values, 7 rows of 7, or 7 strings of 7.');
    }
    // Off dots default to a faint tint of the on color rather than upstream's
    // fixed light grey, so one `color` reads on light and dark pages alike.
    const on = color || 'currentColor';
    const off = off_color || `color-mix(in srgb, ${on} 16%, transparent)`;
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            {frames && (
                <Upstream grids={frames} size={size} onColor={on} offColor={off} variant={variant}
                    reverse={reverse} speed={speed} title={aria_label} playing={playing}
                    style={{display: 'block'}} {...contract('flicker', 'Spinner', props)} />
            )}
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
     * Color of an unlit dot (default a faint tint of `color`).
     */
    off_color: PropTypes.string,
    /**
     * The full 7x7 grid, or its inner 5x5.
     */
    variant: PropTypes.oneOf(['7x7', '5x5']),
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
