import React from 'react';
import PropTypes from 'prop-types';
import { Atom as Upstream } from 'react-loading-indicators';

/**
 * IndicatorsAtom — Dash wrapper for upstream spinner.
 */
const IndicatorsAtom = (props) => {
    const {id, className, style, setProps, size, color, text, textColor, speedPlus, variant} = props;
    return (
        <div id={id} className={className} style={style}>
            <Upstream size={size} color={color} text={text} textColor={textColor} speedPlus={speedPlus} variant={variant} />
        </div>
    );
};

IndicatorsAtom.defaultProps = {};

IndicatorsAtom.propTypes = {
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
    textColor: PropTypes.string,
    /**
     * Speed adjustment.
     */
    speedPlus: PropTypes.number,
    /**
     * Variant where supported (OrbitProgress, ThreeDot).
     */
    variant: PropTypes.string,
};

export default IndicatorsAtom;
