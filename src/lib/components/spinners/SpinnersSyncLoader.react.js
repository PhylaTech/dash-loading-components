import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import Upstream from 'react-spinners/SyncLoader';

/**
 * SpinnersSyncLoader — Dash wrapper for upstream spinner.
 */
const SpinnersSyncLoader = (props) => {
    const {id, className, style, size, color, loading, speed_multiplier, height, width, margin, rate, playing} = props;
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            <Upstream size={size} color={color} loading={loading} speedMultiplier={speed_multiplier} height={height} width={width} margin={margin} {...contract('spinners', 'SyncLoader', props)} />
        </div>
    );
};

SpinnersSyncLoader.defaultProps = {};

SpinnersSyncLoader.propTypes = {
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
     * Size in pixels.
     */
    size: PropTypes.number,
    /**
     * Color.
     */
    color: PropTypes.string,
    /**
     * Whether to show the spinner.
     */
    loading: PropTypes.bool,
    /**
     * Speed multiplier.
     */
    speed_multiplier: PropTypes.number,
    /**
     * Height where applicable.
     */
    height: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Width where applicable.
     */
    width: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Margin between elements.
     */
    margin: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
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

export default SpinnersSyncLoader;
