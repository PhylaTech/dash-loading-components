import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import { RadarSpinner as Upstream } from 'react-epic-spinners';

/**
 * EpicRadarSpinner — Dash wrapper for upstream spinner.
 */
const EpicRadarSpinner = (props) => {
    const {id, className, style, size, color, animation_duration, rate, playing} = props;
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            <Upstream size={size} color={color} animationDuration={animation_duration} {...contract('epic', 'RadarSpinner', props)} />
        </div>
    );
};

EpicRadarSpinner.defaultProps = {};

EpicRadarSpinner.propTypes = {
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
     * Animation duration in ms.
     */
    animation_duration: PropTypes.number,
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

export default EpicRadarSpinner;
