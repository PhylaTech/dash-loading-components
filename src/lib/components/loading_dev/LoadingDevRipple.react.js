import React from 'react';
import PropTypes from 'prop-types';
import { Ripple as Upstream } from 'loading-dev';

/**
 * LoadingDevRipple — Dash wrapper for upstream spinner.
 */
const LoadingDevRipple = (props) => {
    const {id, className, style, setProps, size, color, duration, playState, direction} = props;
    return (
        <div id={id} style={style}>
            <Upstream size={size} color={color} duration={duration} playState={playState} direction={direction} className={className} />
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
     * Dash-assigned callback that should be called to report property changes.
     */
    setProps: PropTypes.func,
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
    playState: PropTypes.oneOf(["paused", "running"]),
    /**
     * Motion direction: out (default) spreads from center; in draws inward.
     */
    direction: PropTypes.oneOf(["in", "out"]),
};

export default LoadingDevRipple;
