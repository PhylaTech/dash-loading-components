import React from 'react';
import PropTypes from 'prop-types';
import { Oval as Upstream } from 'react-loader-spinner';

/**
 * LoaderSpinnerOval — Dash wrapper for upstream spinner.
 */
const LoaderSpinnerOval = (props) => {
    const {id, className, style, setProps, height, width, color, secondaryColor, radius, ariaLabel, visible, strokeWidth, strokeWidthSecondary, animationDuration} = props;
    return (
        <div id={id} className={className} style={style}>
            <Upstream height={height} width={width} color={color} secondaryColor={secondaryColor} ariaLabel={ariaLabel} visible={visible} strokeWidth={strokeWidth} strokeWidthSecondary={strokeWidthSecondary} animationDuration={animationDuration} />
        </div>
    );
};

LoaderSpinnerOval.defaultProps = {};

LoaderSpinnerOval.propTypes = {
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
    /**
     * Stroke width of the background circle.
     */
    strokeWidthSecondary: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Rotation duration in seconds.
     */
    animationDuration: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
};

export default LoaderSpinnerOval;
