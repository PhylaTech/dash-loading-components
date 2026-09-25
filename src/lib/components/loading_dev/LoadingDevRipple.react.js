import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import { Ripple as Upstream } from 'loading-dev';

/**
 * LoadingDevRipple — Dash wrapper for upstream spinner.
 */
const LoadingDevRipple = (props) => {
    const {id, className, style, size, color, duration, play_state, direction, playing} = props;
    return (
        <div id={id} style={style}>
            <Upstream size={size} color={color} duration={duration} playState={play_state} direction={direction} className={wrapperClass(className, playing)} {...contract('loading_dev', 'Ripple', props)} />
        </div>
    );
};

LoadingDevRipple.defaultProps = {};

LoadingDevRipple.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,
    /**
     * Extra class names merged onto the spinner root (loading.dev).
     */
    className: PropTypes.string,
    /**
     * Inline styles applied to the outer wrapper.
     */
    style: PropTypes.object,
    /**
     * Width/height in pixels. Defaults to 20.
     */
    size: PropTypes.number,
    /**
     * Any CSS color.
     */
    color: PropTypes.string,
    /**
     * Animation cycle length in milliseconds.
     */
    duration: PropTypes.number,
    /**
     * Whether the animation runs.
     */
    play_state: PropTypes.oneOf(["paused", "running"]),
    /**
     * Motion direction: out (default) spreads from center; in draws inward.
     */
    direction: PropTypes.oneOf(["in", "out"]),
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

export default LoadingDevRipple;
