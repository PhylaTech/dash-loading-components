import React from 'react';
import PropTypes from 'prop-types';
import {contract, wrapperClass} from '../../contract';
import { SpinnerRoundFilled as Upstream } from 'spinners-react';

/**
 * SpinnersReactSpinnerRoundFilled — Dash wrapper for upstream spinner.
 */
const SpinnersReactSpinnerRoundFilled = (props) => {
    const {id, className, style, size, color, secondary_color, thickness, speed, enabled, still, playing} = props;
    return (
        <div id={id} className={wrapperClass(className, playing)} style={style}>
            <Upstream size={size} color={color} secondaryColor={secondary_color} thickness={thickness} speed={speed} enabled={enabled} still={still} {...contract('spinners_react', 'SpinnerRoundFilled', props)} />
        </div>
    );
};

SpinnersReactSpinnerRoundFilled.defaultProps = {};

SpinnersReactSpinnerRoundFilled.propTypes = {
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
    secondary_color: PropTypes.string,
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
    /**
     * Disable animation while keeping the spinner visible.
     */
    still: PropTypes.bool,
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

export default SpinnersReactSpinnerRoundFilled;
