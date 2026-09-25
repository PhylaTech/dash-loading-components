import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import { OrbitProgress as Upstream } from 'react-loading-indicators';

/**
 * IndicatorsOrbitProgress — Dash wrapper for upstream spinner.
 */
const IndicatorsOrbitProgress = (props) => {
    const {id, className, style, size, color, text, text_color, speed_plus, variant, easing, dense, rate, playing} = props;
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            <Upstream size={size} color={color} text={text} textColor={text_color} speedPlus={speed_plus} variant={variant} easing={easing} dense={dense} {...contract('indicators', 'OrbitProgress', props)} />
        </div>
    );
};

IndicatorsOrbitProgress.defaultProps = {};

IndicatorsOrbitProgress.propTypes = {
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
     * Size (small/medium/large or number).
     */
    size: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    /**
     * Color or color array.
     */
    color: PropTypes.oneOfType([PropTypes.string, PropTypes.arrayOf(PropTypes.string)]),
    /**
     * Optional text.
     */
    text: PropTypes.string,
    /**
     * Text color.
     */
    text_color: PropTypes.string,
    /**
     * Speed adjustment.
     */
    speed_plus: PropTypes.number,
    /**
     * Variant where supported (OrbitProgress, ThreeDot).
     */
    variant: PropTypes.string,
    /**
     * CSS animation easing function (e.g. linear, ease-in, ease-out).
     */
    easing: PropTypes.string,
    /**
     * Make the OrbitProgress animation more bold/compact.
     */
    dense: PropTypes.bool,
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

export default IndicatorsOrbitProgress;
