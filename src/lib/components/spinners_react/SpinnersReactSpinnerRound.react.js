import React from 'react';
import PropTypes from 'prop-types';
import { SpinnerRound as Upstream } from 'spinners-react';

/**
 * SpinnersReactSpinnerRound — Dash wrapper for upstream spinner.
 */
const SpinnersReactSpinnerRound = (props) => {
    const {id, className, style, setProps, size, color, secondaryColor, thickness, speed, enabled} = props;
    return (
        <div id={id} className={className} style={style}>
            <Upstream size={size} color={color} secondaryColor={secondaryColor} thickness={thickness} speed={speed} enabled={enabled} />
        </div>
    );
};

SpinnersReactSpinnerRound.defaultProps = {};

SpinnersReactSpinnerRound.propTypes = {
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
     * Size.
     */
    size: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
    /**
     * Primary color.
     */
    color: PropTypes.string,
    /**
     * Secondary color.
     */
    secondaryColor: PropTypes.string,
    /**
     * Thickness.
     */
    thickness: PropTypes.number,
    /**
     * Speed.
     */
    speed: PropTypes.number,
    /**
     * Whether enabled.
     */
    enabled: PropTypes.bool,
};

export default SpinnersReactSpinnerRound;
