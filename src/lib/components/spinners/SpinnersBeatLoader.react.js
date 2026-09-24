import React from 'react';
import PropTypes from 'prop-types';
import Upstream from 'react-spinners/BeatLoader';

/**
 * SpinnersBeatLoader — Dash wrapper for upstream spinner.
 */
const SpinnersBeatLoader = (props) => {
    const {id, className, style, setProps, size, color, loading, speedMultiplier, height, width, margin} = props;
    return (
        <div id={id} className={className} style={style}>
            <Upstream size={size} color={color} loading={loading} speedMultiplier={speedMultiplier} height={height} width={width} margin={margin} />
        </div>
    );
};

SpinnersBeatLoader.defaultProps = {};

SpinnersBeatLoader.propTypes = {
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
};

export default SpinnersBeatLoader;
