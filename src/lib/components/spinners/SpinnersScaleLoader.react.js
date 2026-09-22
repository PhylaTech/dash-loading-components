import React from 'react';
import PropTypes from 'prop-types';
import Upstream from 'react-spinners/ScaleLoader';

/**
 * SpinnersScaleLoader — Dash wrapper for upstream spinner.
 */
const SpinnersScaleLoader = (props) => {
    const {id, className, style, setProps, size, color, loading, speedMultiplier, height, width, margin, radius, barCount} = props;
    return (
        <div id={id} className={className} style={style}>
            <Upstream color={color} loading={loading} speedMultiplier={speedMultiplier} height={height} width={width} margin={margin} radius={radius} barCount={barCount} />
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
     * Dash-assigned callback that should be called to report property changes.
     */
    setProps: PropTypes.func,
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
    speedMultiplier: PropTypes.number,
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
    barCount: PropTypes.number,
};

export default SpinnersScaleLoader;
