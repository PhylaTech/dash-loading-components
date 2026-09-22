import React from 'react';
import PropTypes from 'prop-types';
import { SpringSpinner as Upstream } from 'react-epic-spinners';

/**
 * EpicSpringSpinner — Dash wrapper for upstream spinner.
 */
const EpicSpringSpinner = (props) => {
    const {id, className, style, setProps, size, color, animationDuration} = props;
    return (
        <div id={id} className={className} style={style}>
            <Upstream size={size} color={color} animationDuration={animationDuration} />
        </div>
    );
};

EpicSpringSpinner.defaultProps = {};

EpicSpringSpinner.propTypes = {
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
     * Animation duration in ms.
     */
    animationDuration: PropTypes.number,
};

export default EpicSpringSpinner;
