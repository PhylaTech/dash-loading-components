import React from 'react';
import PropTypes from 'prop-types';
import { ThreeDots as Upstream } from 'react-loader-spinner';

/**
 * LoaderSpinnerThreeDots — Dash wrapper for upstream spinner.
 */
const LoaderSpinnerThreeDots = (props) => {
    const {id, className, style, setProps, height, width, color, secondaryColor, radius, ariaLabel, visible, strokeWidth} = props;
    return (
        <div id={id} className={className} style={style}>
            <Upstream height={height} width={width} color={color} secondaryColor={secondaryColor} radius={radius} ariaLabel={ariaLabel} visible={visible} strokeWidth={strokeWidth} />
        </div>
    );
};

LoaderSpinnerThreeDots.defaultProps = {};

LoaderSpinnerThreeDots.propTypes = {
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
     * Height.
     */
    height: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Width.
     */
    width: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Color.
     */
    color: PropTypes.string,
    /**
     * Secondary color.
     */
    secondaryColor: PropTypes.string,
    /**
     * Radius where applicable.
     */
    radius: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Aria label.
     */
    ariaLabel: PropTypes.string,
    /**
     * Visibility.
     */
    visible: PropTypes.bool,
    /**
     * Stroke width.
     */
    strokeWidth: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
};

export default LoaderSpinnerThreeDots;
