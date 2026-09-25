import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import Upstream from 'react-spinners/ScaleLoader';

/**
 * SpinnersScaleLoader — Dash wrapper for upstream spinner.
 */
const SpinnersScaleLoader = (props) => {
    const {id, className, style, size, color, loading, speed_multiplier, height, width, margin, radius, bar_count, rate, playing} = props;
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            <Upstream color={color} loading={loading} speedMultiplier={speed_multiplier} height={height} width={width} margin={margin} radius={radius} barCount={bar_count} {...contract('spinners', 'ScaleLoader', props)} />
        </div>
    );
};

SpinnersScaleLoader.defaultProps = {};

SpinnersScaleLoader.propTypes = {
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
     * Bar corner radius.
     */
    radius: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Number of bars.
     */
    bar_count: PropTypes.number,
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

export default SpinnersScaleLoader;
