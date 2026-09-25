import React, {useRef} from 'react';
import PropTypes from 'prop-types';
import {contract, usePlaying, wrapperClass} from '../../contract';
import { Oval as Upstream } from 'react-loader-spinner';

/**
 * LoaderSpinnerOval — Dash wrapper for upstream spinner.
 */
const LoaderSpinnerOval = (props) => {
    const {id, className, style, size, height, width, color, secondary_color, radius, aria_label, visible, stroke_width, stroke_width_secondary, animation_duration, rate, playing} = props;
    const root = useRef(null);
    usePlaying(root, playing);
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style} ref={root}>
            <Upstream height={height ?? size} width={width ?? size} color={color} secondaryColor={secondary_color} ariaLabel={aria_label} visible={visible} strokeWidth={stroke_width} strokeWidthSecondary={stroke_width_secondary} animationDuration={animation_duration} {...contract('loader_spinner', 'Oval', props)} />
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
     * Height and width in pixels, unless either is given on its own.
     */
    size: PropTypes.number,
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
    secondary_color: PropTypes.string,
    /**
     * Radius where applicable.
     */
    radius: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Aria label.
     */
    aria_label: PropTypes.string,
    /**
     * Visibility.
     */
    visible: PropTypes.bool,
    /**
     * Stroke width.
     */
    stroke_width: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Stroke width of the background circle.
     */
    stroke_width_secondary: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Rotation duration in seconds.
     */
    animation_duration: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
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

export default LoaderSpinnerOval;
