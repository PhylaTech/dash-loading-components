import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import { Ring as Upstream } from 'ldrs/react';
import 'ldrs/react/Ring.css';

/**
 * LdrsRing — Dash wrapper for upstream spinner.
 */
const LdrsRing = (props) => {
    const {id, className, style, size, color, speed, stroke, bg_opacity, rate, playing} = props;
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            <Upstream size={size} color={color} speed={speed} stroke={stroke} bgOpacity={bg_opacity} {...contract('ldrs', 'Ring', props)} />
        </div>
    );
};

LdrsRing.defaultProps = {};

LdrsRing.propTypes = {
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
     * Size in px.
     */
    size: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Color.
     */
    color: PropTypes.string,
    /**
     * Animation speed.
     */
    speed: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Stroke width where applicable.
     */
    stroke: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Background opacity for the ring track (0–1).
     */
    bg_opacity: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
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

export default LdrsRing;
