import React from 'react';
import PropTypes from 'prop-types';
import { Atom as Upstream } from 'loading-dev';

/**
 * LoadingDevAtom — Dash wrapper for upstream spinner.
 */
const LoadingDevAtom = (props) => {
    const {id, className, style, setProps, size, color, duration, playState} = props;
    return (
        <div id={id} className={className} style={style}>
            <Upstream size={size} color={color} duration={duration} playState={playState} />
        </div>
    );
};

LoadingDevAtom.defaultProps = {};

LoadingDevAtom.propTypes = {
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
};

export default LoadingDevAtom;
