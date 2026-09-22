import React from 'react';
import PropTypes from 'prop-types';
import { Hourglass as Upstream } from 'ldrs/react';
import 'ldrs/react/Hourglass.css';

/**
 * LdrsHourglass — Dash wrapper for upstream spinner.
 */
const LdrsHourglass = (props) => {
    const {id, className, style, setProps, size, color, speed, stroke, bgOpacity} = props;
    return (
        <div id={id} className={className} style={style}>
            <Upstream size={size} color={color} speed={speed} stroke={stroke} bgOpacity={bgOpacity} />
        </div>
    );
};

LdrsHourglass.defaultProps = {};

LdrsHourglass.propTypes = {
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
     * Background opacity (0–1).
     */
    bgOpacity: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
};

export default LdrsHourglass;
